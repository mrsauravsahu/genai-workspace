#!/usr/bin/env python3
"""Client: sends a toggle command to the ptt-tmux daemon for the given pane.

Usage:
    toggle.py <tmux-pane-id> [device]
    toggle.py --list-devices

`device` may be a sounddevice index (e.g. 2) or a substring of the
device name (e.g. "MacBook Pro Microphone"). Omit it to use the system
default input device.
"""
import socket
import subprocess
import sys
import os

SOCK_PATH = os.path.expanduser("~/.ptt-tmux.sock")


def list_devices():
    import sounddevice as sd

    print(sd.query_devices())


def input_devices():
    import sounddevice as sd

    return [
        (i, d["name"])
        for i, d in enumerate(sd.query_devices())
        if d["max_input_channels"] > 0
    ]


def send(msg):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(SOCK_PATH)
        sock.sendall(msg.encode())


def query_status():
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(SOCK_PATH)
        sock.sendall(b"status")
        return sock.recv(64).decode()


def toggle(pane, device=None):
    msg = f"toggle {pane}"
    if device is not None:
        msg += f" {device}"
    send(msg)


def show_device_menu(pane):
    """Pop up a tmux menu of input devices; selecting one starts recording
    on `pane` with that device. Requires running inside tmux."""
    script = os.path.abspath(__file__)
    python = sys.executable
    args = ["tmux", "display-menu", "-T", "ptt input device"]
    args += ["Default", "d", f"run-shell '{python} {script} {pane}'"]
    for index, name in input_devices():
        key = str((index + 1) % 10)  # 1-9 then 0, best effort
        label = name.replace("'", "")
        args += [label, key, f"run-shell '{python} {script} {pane} {index}'"]
    subprocess.run(args, check=True)


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "--list-devices":
        list_devices()
        return

    if len(sys.argv) not in (2, 3):
        print("usage: toggle.py <tmux-pane-id> [device]", file=sys.stderr)
        print("       toggle.py --list-devices", file=sys.stderr)
        sys.exit(1)

    pane = sys.argv[1]
    device = sys.argv[2] if len(sys.argv) == 3 else None

    if device is not None:
        toggle(pane, device)
        return

    # No device given: if we're about to start recording, let the user
    # pick an input device via a tmux menu. If we're stopping, just stop.
    status = query_status()
    if status == "recording":
        toggle(pane)
    else:
        show_device_menu(pane)


if __name__ == "__main__":
    main()
