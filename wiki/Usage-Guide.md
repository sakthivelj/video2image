# Usage Guide

## Launching the Application

- **Executable:** Double-click `video2image-gui.exe`
- **From source:** Run `python main.py`

## Interface Overview

The application has a single-page layout with these sections:

### Menu Bar

| Menu | Items |
|------|-------|
| **File** | Open Video, Open Folder, Exit |
| **Export** | Recursive Scan, Parallel Processing, Max Workers |
| **Help** | Photogrammetry Tips, About |

### Input / Output

- **Video** — Select a single video file (📁 File) or a folder of videos (📂 Folder)
- **Output** — Choose where extracted frames are saved (defaults to same location as input)

### Video Info

When a video file is selected, this panel automatically shows:
- Duration, FPS, total frame count, resolution

### Extraction Settings

| Setting | Description | Default |
|---------|-------------|---------|
| **Frame step** | Extract every Nth frame (1 = all frames) | 1 |
| **Start / End time** | Time range in seconds | Full video |
| **Frame range** | Specific frame numbers (e.g., 100-500) | All frames |
| **Key Frame Extraction** | Extract only visually distinct frames | Off |
| **Scene Detection** | Capture at visual changes (threshold: 0-255) | Off / 30 |
| **Motion-based** | Capture frames with motion (threshold: 0-1000) | Off / 5 |
| **Remove Duplicates** | Skip near-identical frames | Off |

### Output Settings

| Setting | Description | Default |
|---------|-------------|---------|
| **Format** | JPG or PNG | JPG |
| **JPEG quality** | Compression quality 1-100 | 95 |
| **PNG compression** | Compression level 0-9 | 6 |
| **Resize** | Width × Height (0 = original) | Original |
| **Grayscale** | Convert to black and white | Off |
| **Naming pattern** | Custom filename template | Default |
| **Prefix / Suffix** | Add text before/after frame number | Empty |
| **Include timestamp** | Add timestamp to filename | Off |
| **Include parent dir** | Include parent folder in output path | Off |

## Step-by-Step Workflow

### 1. Select Input

Click **📁 File** to select a single video, or **📂 Folder** to select a directory of videos.

Supported formats: MP4, MKV, AVI, MOV, WebM, FLV, WMV

### 2. Configure Extraction

Choose your extraction settings. For most use cases:

- **General use:** Default settings (extracts all frames)
- **Photogrammetry:** Enable "Key Frame Extraction"
- **Time-lapse:** Set Frame step to 30 (one frame per second for 30fps video)
- **Specific segment:** Set Start/End time

### 3. Choose Output

Select an output folder, or leave blank to save alongside the input video.

### 4. Extract

Click **▶ Extract Frames**. Progress is shown in the progress bar.

### 5. Cancel (if needed)

Click **Cancel** to stop extraction at any time.

## Batch Processing

To process multiple videos at once:

1. Select a **folder** instead of a single file
2. Open the **Export** menu to configure:
   - ☐ **Recursive Folder Scan** — include videos in subdirectories
   - ☐ **Parallel Processing** — process multiple videos at the same time
   - **Max Workers** — number of parallel threads (1-16)

## Naming Patterns

The naming pattern field supports these variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `{video}` | Video filename (without extension) | `myvideo` |
| `{frame}` | Frame number (use `{frame:04d}` for padding) | `0042` |
| `{time}` | Timestamp in seconds | `1.234` |
| `{datetime}` | Current date/time | `20240101_120000` |

Example pattern: `{video}_frame_{frame:04d}` → `myvideo_frame_0042.jpg`
