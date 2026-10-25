---
name: friday-ave-editor
description: Edit videos in AVE (automated-video-editing) using a local Qwen 27B MLX model. Understands the AVE clip JSON format, cuts from transcripts, syncs talking-head and screencast sources, and can request transitions, animations, LUTs and crops.
argument-hint: "<project-name>: <edit request>"
---

# friday-ave-editor — AVE video editing with a local MLX model

Use this skill when the user wants an AI-driven edit in AVE
(`repos/friday/automated-video-editing`) and the model is a local Qwen 27B MLX
copy served by `mlx-lm.server` or an OpenAI-compatible endpoint.

## What AVE expects

AVE stores edits in `projects/<name>/ave.json`. The editor timeline is an array
of clips under `state.clips` (or `clips` for an incremental edit). Each clip:

```json
{
  "id": "clip-0",
  "source": "634.mp4",
  "inTime": 0,
  "outTime": 11.848,
  "label": "the hook line",
  "filters": [
    { "type": "crop", "aspectRatio": "4:3", "stretch": false },
    { "type": "lut", "lut": "SamsungLog_to_Blockbuster_Neutral_Rec709.cube" }
  ]
}
```

Rules:
- `source` must be a filename that already exists in the project's `public/` dir.
- `inTime` / `outTime` are seconds inside that source, `outTime > inTime`.
- `label` is optional on-screen text for the clip.
- `filters` are optional and applied in order.

## Supported filters

The renderer currently applies these; anything else is ignored:

- `lut` — `lut` is a filename under `luts/` or `assets/luts/`. Use the LUT
  library names returned by the AVE API.
- `crop` — `aspectRatio` one of `9:16`, `4:5`, `1:1`, `4:3`, `16:9`.
  `stretch: true` squeezes the frame; `false` (default) centre-crops.

Reserved for future renderer support (emit them; AVE will store them):

- `transition` — `{ "type": "transition", "kind": "cut|fade|crossfade", "duration": 0.3 }`
- `animation` — `{ "type": "animation", "kind": "zoom-in|zoom-out|pan-left|pan-right", "start": 0, "end": 1 }`

## Editing workflow

1. Read the project status from `GET /api/projects/<name>/status`.
2. Read the editor state from `GET /api/projects/<name>/editor`.
3. Read transcripts from the project `public/` SRT files or `__ingestion/` JSON.
4. Build a cut list from the transcript:
   - remove dead air, false starts, repeated takes, "ums" and tangents;
   - keep the through-line and the strongest moments;
   - cut on speech, not on silence;
   - for talking-head + screencast pairs, keep the talking head on the hook and
     explanation, switch to the screencast for the demo, and cut back to the
     speaker for the takeaway.
5. Post the edit:
   - `POST /api/projects/<name>/editor` for an incremental timeline change;
   - `POST /api/projects/<name>/ave-edits` for a named saved edit.

## Talking head + screencast sync

When the project has two sources and one is clearly a screen recording:

- Identify the speaker source and the screen source by name / resolution / transcript.
- Use the transcript timestamps to line up the narration with the screen action.
- Typical pattern:
  1. Speaker opens with the problem (3-5 s).
  2. Cut to screencast for the demo, narrated by the speaker audio.
  3. Cut back to speaker for the conclusion / CTA.

If only the speaker source has audio, carry that audio across screencast clips
by setting `clip.muted = false` on all clips (default). Do not extract or invent
audio.

## Short-form edits

For Reels / Shorts / TikTok:
- Open with the strongest moment in the first 1-3 seconds.
- Keep vertical framing (`9:16` or `4:5`) unless the request says otherwise.
- Add a title overlay in the first 1-3 seconds.
- Total length defaults to the request; if none given, keep it under 60 seconds.

## Model backend

The genai-editor service uses `GENAI_BACKEND=mlx` and talks to an OpenAI-compatible
chat endpoint. Set `MLX_BASE_URL` (default `http://localhost:8080`) and
`GENAI_MODEL` to the model served by `mlx-lm.server`.

Example:

```bash
GENAI_BACKEND=mlx \
MLX_BASE_URL=http://localhost:8080 \
GENAI_MODEL=qwen2.5-27b-instruct-mlx \
node services/genai-editor/server.js
```
