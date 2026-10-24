# controllerReciever

A lightweight, cross-platform UDP receiver that listens to gamepad signals from your Android phone and emulates native keyboard presses for Pokémon games and PC emulators (mGBA, DeSmuME, OpenEmu, Ryujinx, etc.).

## Features
- **Cross-Platform**: Works on macOS, Windows, and Linux.
- **Ultra-Low Latency**: Uses lightweight UDP packets over local Wi-Fi.
- **Automatic IP Detection**: Displays your PC's local IP address on startup so you can easily enter it in your Android app.
- **Configurable Controls**: Pre-configured for standard Pokémon emulator controls (GBA/NDS).

---

## Setup & Installation

### 1. Requirements
- Python 3.8+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Run the Receiver
```bash
python receiver.py
```

> **macOS Note**: When running for the first time, macOS may ask to grant Accessibility permissions to Terminal / Python in **System Settings > Privacy & Security > Accessibility** so it can simulate keyboard presses.

---

## Default Button Mappings

| Controller Button | Emulator Key | Typical Pokémon Action |
|:-----------------|:-------------|:-----------------------|
| `UP`             | Arrow Up     | Move Up                |
| `DOWN`           | Arrow Down   | Move Down              |
| `LEFT`           | Arrow Left   | Move Left              |
| `RIGHT`          | Arrow Right  | Move Right             |
| `A`              | `Z`          | Confirm / Talk         |
| `B`              | `X`          | Cancel / Run           |
| `START`          | Enter        | In-game Menu           |
| `SELECT`         | Shift        | Bag / Registered Item  |
| `L`              | `A`          | Left Shoulder          |
| `R`              | `S`          | Right Shoulder         |
| `TURBO`          | Space        | Fast-Forward Toggle    |
