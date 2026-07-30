# video2image

**Photogrammetry-focused video frame extractor** — A desktop GUI application to extract frames from video files for 3D reconstruction, photogrammetry, and computer vision workflows.

[![Release](https://img.shields.io/github/v/release/sakthivelj/video2image)](https://github.com/sakthivelj/video2image/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Download

**[⬇ Download video2image-gui.exe](https://github.com/sakthivelj/video2image/releases/latest)** (Windows)

## Features

- **Key Frame Extraction** — Extract only visually distinct frames, ideal for photogrammetry
- **Scene Detection** — Automatically capture frames at significant visual changes
- **Motion-based Extraction** — Extract frames with significant motion
- **Duplicate Removal** — Skip near-identical frames
- **Frame Control** — Step interval, time range, frame range
- **Output Control** — JPG/PNG, quality sliders, resize, grayscale, custom naming
- **Batch Processing** — Process entire folders, recursive scan, parallel execution
- **Video Info** — Auto-displays duration, FPS, frame count, resolution
- **Dark Theme** — Modern Catppuccin-inspired interface

## Screenshot

*Coming soon — run the app to see the interface*

## Quick Start

### Option 1: Download the `.exe` (Recommended)

1. Go to [Releases](https://github.com/sakthivelj/video2image/releases/latest)
2. Download `video2image-gui.exe`
3. Double-click to run — no installation required

### Option 2: Run from Source

```bash
git clone https://github.com/sakthivelj/video2image.git
cd video2image
git checkout develop
pip install -r requirements.txt
python main.py
```

## Usage

1. **Select a video** — Click "📁 File" or drag a video file
2. **Configure extraction** — Set frame step, enable key frame mode, etc.
3. **Click "Extract Frames"** — Frames are saved to the output folder

### For Photogrammetry

Enable **Key Frame Extraction** for best results. This combines scene detection with duplicate removal to extract only unique viewpoints — exactly what photogrammetry software needs.

**Compatible with:** Meshroom, COLMAP, Reality Capture, Agisoft Metashape, 3DF Zephyr

## Batch Processing

Use the **Export** menu to configure:
- **Recursive Folder Scan** — Process videos in subdirectories
- **Parallel Processing** — Process multiple videos simultaneously
- **Max Workers** — Control parallel threads (1–16)

## Documentation

See the [Wiki](https://github.com/sakthivelj/video2image/wiki) for:
- [Installation Guide](https://github.com/sakthivelj/video2image/wiki/Installation)
- [Usage Guide](https://github.com/sakthivelj/video2image/wiki/Usage-Guide)
- [Photogrammetry Guide](https://github.com/sakthivelj/video2image/wiki/Photogrammetry-Guide)

## Build from Source

```bash
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name video2image-gui main.py
```

The `.exe` will be in the `dist/` folder.

## License

[MIT License](LICENSE) — © 2024 Sakthivel J
