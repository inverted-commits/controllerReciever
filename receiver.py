import socket
import sys
from pynput.keyboard import Controller, Key

# Initialize virtual keyboard
keyboard = Controller()

# Map controller buttons to keyboard keys for Pokemon emulators
KEY_MAP = {
    "UP": Key.up,
    "DOWN": Key.down,
    "LEFT": Key.left,
    "RIGHT": Key.right,
    "A": 'z',         # 'Z' is standard for 'A' in GBA/DS emulators
    "B": 'x',         # 'X' is standard for 'B' (running / cancel)
    "START": Key.enter,
    "SELECT": Key.shift,
    "L": 'a',
    "R": 's',
    "TURBO": Key.space # Fast forward toggle in emulators
}

UDP_IP = "0.0.0.0"
UDP_PORT = 8000

def get_local_ip():
    """Attempt to discover the host's LAN IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Does not actually connect, used to find routing interface
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def main():
    local_ip = get_local_ip()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((UDP_IP, UDP_PORT))
    except Exception as e:
        print(f"Error binding to {UDP_IP}:{UDP_PORT}: {e}")
        sys.exit(1)

    print("=" * 60)
    print("🎮 Pokemon Controller Receiver (Cross-Platform)")
    print("=" * 60)
    print(f"📡 Listening on Port: {UDP_PORT}")
    print(f"📍 Your PC Local IP is likely: {local_ip}")
    print("   Enter this IP in your Android controller app.")
    print("=" * 60)
    print("Waiting for controller signals... (Ctrl+C to stop)\n")

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = data.decode('utf-8', errors='ignore').strip()

            # Handle Auto-Discovery ping from Android phone
            if message == "DISCOVER":
                sock.sendto(b"DISCOVER_ACK", addr)
                print(f"✨ Auto-discovery ping from phone at {addr[0]} -> Responded!")
                continue

            if ":" in message:
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
        except KeyboardInterrupt:
            print("\nShutting down receiver.")
            break
        except Exception as e:
            print(f"Error handling packet: {e}")

if __name__ == "__main__":
    main()
