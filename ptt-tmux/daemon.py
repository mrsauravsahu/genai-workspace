#!/usr/bin/env python3
"""Push-to-talk daemon: loads Parakeet once, listens on a unix socket for
toggle commands, records mic audio while active, and periodically
transcribes the audio-so-far, typing only newly-spoken words into the
requesting tmux pane via `tmux send-keys` as they're recognized.

All model inference happens on the main thread (MLX streams are
thread-local and the model isn't safe to call from a worker thread), so
the accept loop uses a socket timeout to interleave polling for new
toggle commands with periodic re-transcription while recording.
"""
import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
import wave

import mlx.core as mx
import numpy as np
import sounddevice as sd
from parakeet_mlx import from_pretrained

SOCK_PATH = os.path.expanduser("~/.ptt-tmux.sock")
SAMPLE_RATE = 16000
POLL_INTERVAL = 1.0  # seconds between incremental re-transcriptions

state_lock = threading.Lock()
recording = False
frames = []
stream = None
target_pane = None
typed_words = []  # words already sent to the pane for the current utterance


def log(msg):
    print(f"[ptt] {msg}", flush=True)


def audio_callback(indata, frames_count, time_info, status):
    if status:
        log(f"audio status: {status}")
    with state_lock:
        if recording:
            frames.append(indata.copy())


def inject(pane, text):
    try:
        subprocess.run(["tmux", "send-keys", "-t", pane, "-l", text], check=True)
    except subprocess.CalledProcessError as e:
        log(f"tmux send-keys failed: {e}")


def transcribe_current(model):
    """Transcribe whatever audio has been captured so far and type any
    words not already typed for this utterance. Must run on the main
    thread (the thread the model was loaded on)."""
    global typed_words
    with state_lock:
        chunks = frames.copy()
        pane = target_pane
    if not chunks:
        return
    audio = np.concatenate(chunks, axis=0).flatten()
    if len(audio) < SAMPLE_RATE // 4:
        return  # too little audio yet to bother
    pcm16 = np.clip(audio * 32767, -32768, 32767).astype(np.int16)
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        with wave.open(f.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(pcm16.tobytes())
        result = model.transcribe(f.name)
    mx.clear_cache()
    words = result.text.strip().split()
    if not words:
        return
    # words[:len(typed_words)] should match what we already typed; only
    # type the new suffix. If the re-transcription revised earlier words
    # too, just fall back to appending whatever is new by length.
    new_words = words[len(typed_words):]
    if not new_words:
        return
    prefix = " " if typed_words else ""
    inject(pane, prefix + " ".join(new_words))
    typed_words = words
    log(f"typed: {new_words!r}")


def start_recording(pane, device=None):
    global recording, frames, stream, target_pane, typed_words
    with state_lock:
        recording = True
        frames = []
        target_pane = pane
        typed_words = []
    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=device,
        callback=audio_callback,
    )
    stream.start()
    log(f"recording started (pane={pane}, device={device!r})")


def stop_recording(model):
    global recording, stream
    with state_lock:
        recording = False
    if stream is not None:
        stream.stop()
        stream.close()
    # final pass to catch any trailing words missed since the last poll
    transcribe_current(model)
    log("recording stopped")


def main():
    if os.path.exists(SOCK_PATH):
        os.remove(SOCK_PATH)

    log("loading parakeet model (this happens once)...")
    model = from_pretrained("mlx-community/parakeet-tdt-0.6b-v2")
    log("model loaded")

    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    srv.bind(SOCK_PATH)
    srv.listen(1)
    log(f"listening on {SOCK_PATH}")

    last_poll = time.monotonic()
    while True:
        with state_lock:
            active = recording
        srv.settimeout(POLL_INTERVAL if active else None)
        try:
            conn, _ = srv.accept()
        except socket.timeout:
            transcribe_current(model)
            last_poll = time.monotonic()
            continue

        with conn:
            data = conn.recv(256).decode().strip()
            if not data:
                continue
            parts = data.split(" ")
            cmd = parts[0]
            if cmd == "toggle":
                pane = parts[1] if len(parts) > 1 else None
                device_raw = " ".join(parts[2:]) if len(parts) > 2 else None
                device = int(device_raw) if device_raw and device_raw.isdigit() else device_raw
                with state_lock:
                    is_recording = recording
                if is_recording:
                    stop_recording(model)
                else:
                    start_recording(pane, device=device)
                    last_poll = time.monotonic()
            elif cmd == "ping":
                conn.sendall(b"ok")

        # if a request came in before the poll interval elapsed while
        # recording, catch up on transcription now
        with state_lock:
            active = recording
        if active and time.monotonic() - last_poll >= POLL_INTERVAL:
            transcribe_current(model)
            last_poll = time.monotonic()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
