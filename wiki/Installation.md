# Installation

## Option 1: Download the Executable (Recommended)

1. Go to the [Releases page](https://github.com/sakthivelj/video2image/releases/latest)
2. Download `video2image-gui.exe`
3. Place it anywhere on your computer
4. Double-click to run — no installation required

> **Note:** Windows SmartScreen may show a warning the first time you run the app. Click "More info" → "Run anyway" to proceed. This happens because the executable is not code-signed.

## Option 2: Run from Source

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Steps

```bash
# Clone the repository
git clone https://github.com/sakthivelj/video2image.git
cd video2image

# Switch to the develop branch
git checkout develop

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Dependencies

| Package | Purpose |
|---------|---------|
| `opencv-python` | Video reading and frame processing |
| `tqdm` | Progress bars (CLI fallback) |
| `pyyaml` | Configuration file support |
| `numpy` | Image processing |
| `PyQt6` | GUI framework |

## Building the Executable

To build your own `.exe` from source:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name video2image-gui main.py
```

The executable will be created in the `dist/` folder.

### Reducing Build Size

If your Python environment has heavy packages installed (torch, matplotlib, etc.), exclude them:

```bash
pyinstaller --onefile --windowed --name video2image-gui --exclude-module torch --exclude-module matplotlib --exclude-module scipy main.py
```
