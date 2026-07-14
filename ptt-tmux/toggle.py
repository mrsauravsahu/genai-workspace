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
import sys
import os

SOCK_PATH = os.path.expanduser("~/.ptt-tmux.sock")


def list_devices():
    import sounddevice as sd

    print(sd.query_devices())


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

    msg = f"toggle {pane}"
    if device is not None:
        msg += f" {device}"

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(SOCK_PATH)
        sock.sendall(msg.encode())


if __name__ == "__main__":
    main()
