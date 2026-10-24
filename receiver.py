import os
import shutil
import socket
import subprocess
import sys
import threading
from pynput.keyboard import Controller, Key

# Initialize virtual keyboard
keyboard = Controller()

# Map controller buttons to keyboard keys for Pokemon emulators
KEY_MAP = {
    "UP": Key.up,
    "DOWN": Key.down,
    "LEFT": Key.left,
    "RIGHT": Key.right,
    "A": 'z',          # 'Z' for A
    "B": 'x',          # 'X' for B
    "X": 's',          # 'S' for X (NDS menu)
    "Y": 'a',          # 'A' for Y (NDS registered item)
    "START": Key.enter,
    "SELECT": Key.shift,
    "L": 'q',          # 'Q' for L shoulder
    "R": 'w'           # 'W' for R shoulder
}

HOST_IP = "0.0.0.0"
PORT = 8000

def auto_setup_adb_reverse():
    """Automatically configures ADB reverse for USB Cable mode if a phone is plugged in."""
    adb_bin = shutil.which("adb")
    
    if not adb_bin:
        candidates = [
            os.path.expanduser("~/Library/Android/sdk/platform-tools/adb"),
            os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe")
        ]
        for c in candidates:
            if os.path.exists(c):
                adb_bin = c
                break

    if adb_bin:
        try:
            res = subprocess.run([adb_bin, "reverse", f"tcp:{PORT}", f"tcp:{PORT}"],
                                 capture_output=True, text=True, timeout=2)
            if res.returncode == 0:
                print("⚡ [Auto-Config] USB Cable 0ms Bridge connected via ADB!")
                return True
        except Exception:
            pass
    return False

def handle_command(message):
    message = message.strip()
    if not message or ":" not in message:
        return
    try:
        action, button = message.split(":", 1)
        button = button.upper()
        key = KEY_MAP.get(button)

        if key is not None:
            if action == "PRESS":
                keyboard.press(key)
                print(f"⬇️  Pressed:  [{button}] -> key '{key}'")
            elif action == "RELEASE":
                keyboard.release(key)
                print(f"⬆️  Released: [{button}] -> key '{key}'")
        else:
            print(f"⚠️  Unknown button: {button}")
    except Exception as e:
        print(f"Command error: {e}")

def run_udp_server():
    """Listens for Wi-Fi UDP controller packets."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST_IP, PORT))
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            msg = data.decode('utf-8', errors='ignore').strip()
            handle_command(msg)
        except Exception as e:
            print(f"UDP error: {e}")

def run_tcp_server():
    """Listens for USB Cable (ADB Reverse) TCP streams with 0ms latency."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST_IP, PORT))
    server.listen(5)

    while True:
        try:
            client, addr = server.accept()
            client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            print(f"🔌 USB Cable connection established from {addr}!")
            
            # Buffer stream processor
            buffer = ""
            while True:
                chunk = client.recv(1024).decode('utf-8', errors='ignore')
                if not chunk:
                    break
                buffer += chunk
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    handle_command(line)
            print("🔌 USB Cable disconnected.")
        except Exception as e:
            print(f"TCP error: {e}")

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def main():
    local_ip = get_local_ip()
    print("=" * 60)
    print("🎮 Pokemon Controller Dual Receiver (Wi-Fi + USB Cable)")
    print("=" * 60)
    print(f"📡 Port: {PORT}")
    print(f"🌐 Wi-Fi IP: {local_ip}")
    
    # Auto-configure USB Cable mode if a phone is plugged in
    usb_active = auto_setup_adb_reverse()
    if not usb_active:
        print("💡 Tip: Plug in phone via USB for instant 0ms Cable mode.")
    
    print("=" * 60)
    print("Ready for controller inputs... (Ctrl+C to stop)\n")

    # Start Wi-Fi (UDP) thread
    threading.Thread(target=run_udp_server, daemon=True).start()
    
    # Start USB Cable (TCP) server
    run_tcp_server()

if __name__ == "__main__":
    main()

