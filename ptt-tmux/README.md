# ptt-tmux

Push-to-talk (toggle-to-talk) voice input for tmux. Speak into a terminal
pane and have your words typed in live as you say them, powered by
[Parakeet](https://github.com/senstella/parakeet-mlx) running locally via MLX.

## How it works

- `daemon.py` loads the Parakeet model once and listens on a unix socket
  (`~/.ptt-tmux.sock`). While recording is active it re-transcribes the
  audio-so-far roughly once a second and types only the newly recognized
  words into the target tmux pane via `tmux send-keys`.
- `toggle.py` is a tiny client: it sends `toggle <pane-id>` to the daemon.
  First call starts recording, second call stops it.

## Setup

Dependencies are already installed in `.venv` (`parakeet-mlx`,
`sounddevice`, `numpy`). If you need to reinstall:

```bash
cd ptt-tmux
python3 -m venv .venv
.venv/bin/pip install parakeet-mlx sounddevice numpy
```

## Try it out

1. Start the daemon (first run downloads the model, then loads it — takes
   a bit):

   ```bash
   cd ptt-tmux
   .venv/bin/python daemon.py
   ```

   Leave this running in its own terminal/pane and watch its log output
   (`[ptt] ...`) for status.

2. In another pane, find your pane id:

   ```bash
   tmux display-message -p '#{pane_id}'
   ```

3. Toggle recording on, targeting that pane:

   ```bash
   .venv/bin/python toggle.py %<pane-id>
   ```

   Start speaking. Words should appear typed into the target pane within
   about a second of saying them.

4. Run the same command again to stop recording:

   ```bash
   .venv/bin/python toggle.py %<pane-id>
   ```

### Selecting an input device

By default recording uses the system default microphone. To use a
different input device, list available devices and pass one along when
toggling on:

```bash
.venv/bin/python toggle.py --list-devices
.venv/bin/python toggle.py %<pane-id> 2          # by index
.venv/bin/python toggle.py %<pane-id> "MacBook Pro Microphone"  # by name
```

The device only needs to be specified on the toggle-on call; toggle-off
just needs the pane id.

## Wiring up a tmux key binding

Add to `~/.tmux.conf` so a single key toggles recording for whichever pane
is focused (example binds it to `prefix + v`):

```tmux
bind-key v run-shell "~/GenAI/genai-workspace/ptt-tmux/.venv/bin/python ~/GenAI/genai-workspace/ptt-tmux/toggle.py #{pane_id}"
```

Reload with `tmux source-file ~/.tmux.conf`, then press `prefix + v` to
start/stop recording in the active pane.

## Notes / current limitations

- This is a first working pass, not optimized: transcription re-runs on
  the full audio buffer every poll interval (~1s), so latency and CPU
  usage grow with utterance length. Fine for short dictation; a longer
  session would want proper streaming/chunked decoding.
- Only one recording session at a time (single global daemon state).
- The daemon must already be running before you call `toggle.py`
  (`ping` command exists for a basic liveness check if needed).
