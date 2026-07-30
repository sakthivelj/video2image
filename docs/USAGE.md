# Video2Image Documentation

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Command Line Usage](#command-line-usage)
- [API Reference](#api-reference)
- [Tutorials](#tutorials)
- [FAQ](#faq)
- [Configuration](#configuration)

## Overview

Video2Image is a powerful Python tool for extracting frames from video files. Version 1.4.0 introduces advanced features including:

- **Frame Control**: Extract specific frames by step, time range, or frame numbers
- **Naming Customization**: Custom filename patterns with variables
- **Image Quality**: JPEG/PNG quality control, resizing, grayscale conversion
- **Batch Processing**: Recursive directory scanning, parallel processing
- **Smart Features**: Scene detection, motion-based extraction, duplicate removal
- **Configuration Files**: Save and load default settings

## Installation

### From PyPI
```bash
pip install video2image
```

### From Source
```bash
git clone https://github.com/sakthivelj/video2image.git
cd video2image
pip install -e .
```

### Requirements
- Python 3.8+
- OpenCV (opencv-python)
- tqdm
- PyYAML
- NumPy

## Quick Start

### Basic Usage
```bash
# Extract all frames from a video
video2image -i video.mp4 -o output/

# Extract frames as PNG
video2image -i video.mp4 -o output/ -f png
```

### Advanced Examples
```bash
# Extract every 5th frame
video2image -i video.mp4 --frame-step 5

# Extract frames from 10s to 30s
video2image -i video.mp4 --start-time 10 --end-time 30

# Resize and convert to grayscale
video2image -i video.mp4 --resize-width 1920 --grayscale

# Enable scene detection
video2image -i video.mp4 --scene-detection

# Process directory recursively with parallel processing
video2image -i ./videos/ --recursive --parallel
```

## Command Line Usage

### Input/Output Options
```
-i, --input          Path to input video file or directory (required)
-o, --output         Path to output directory (default: same as input)
-p, --parent         Include parent directory in output path
```

### Frame Control
```
--frame-step N       Extract every Nth frame (default: 1)
--start-time SEC     Start extraction at time in seconds
--end-time SEC       End extraction at time in seconds
--frame-range RANGE  Frame range (e.g., '100-200' or '100')
```

### Naming Customization
```
--naming-pattern PAT Custom naming pattern
--prefix TEXT        Prefix for filenames
--suffix TEXT        Suffix for filenames
--include-timestamp  Include timestamp in filename
```

**Pattern Variables:**
- `{video}` - Video filename without extension
- `{frame}` - Frame number
- `{time}` - Timestamp in seconds
- `{datetime}` - Current datetime

### Image Quality
```
-f, --format         Image format: jpg, png (default: jpg)
--jpeg-quality N     JPEG quality 1-100 (default: 95)
--png-compression N  PNG compression 0-9 (default: 6)
--resize-width PX    Resize width (maintains aspect ratio)
--resize-height PX   Resize height (maintains aspect ratio)
--grayscale          Convert to grayscale
```

### Smart Features
```
--scene-detection    Enable scene change detection
--scene-threshold N  Scene change threshold 0-255 (default: 30)
--motion-based       Enable motion-based extraction
--motion-threshold N Motion threshold (default: 5)
--remove-duplicates  Remove duplicate frames
```

### Batch Processing
```
--recursive          Search directories recursively
--patterns PATTERNS  Custom file patterns
--parallel           Process videos in parallel
--max-workers N      Max parallel workers (default: 4)
```

### Configuration
```
--config PATH        Config file path
--save-config        Save current settings as default
--show-config        Show current config and exit
```

## API Reference

### extract_frames()

Extract frames from a single video file.

```python
from video2image.converter import extract_frames

extract_frames(
    video_path='video.mp4',
    output_folder='output/',
    
    # Frame Control
    frame_step=1,
    start_time=None,
    end_time=None,
    frame_range=None,
    
    # Naming
    naming_pattern=None,
    prefix='',
    suffix='',
    include_timestamp=False,
    
    # Quality
    image_format='jpg',
    jpeg_quality=95,
    png_compression=6,
    resize_width=None,
    resize_height=None,
    grayscale=False,
    
    # Smart Features
    scene_detection=False,
    scene_threshold=30,
    motion_based=False,
    motion_threshold=5,
    remove_duplicates=False,
    
    # Config
    config_path=None
)
```

### extract_frames_batch()

Process multiple videos with optional parallel execution.

```python
from video2image.converter import extract_frames_batch

results = extract_frames_batch(
    video_files=['video1.mp4', 'video2.mp4'],
    output_folder='output/',
    parallel=True,
    max_workers=4,
    frame_step=2
)
```

### find_videos_recursive()

Find all video files in a directory tree.

```python
from video2image.converter import find_videos_recursive

videos = find_videos_recursive('./videos/')
videos_custom = find_videos_recursive('./videos/', patterns=['*.mkv', '*.avi'])
```

### load_config() / save_config()

Manage configuration files.

```python
from video2image.converter import load_config, save_config

# Load config
config = load_config()  # Uses default path
config = load_config('/path/to/config.yaml')

# Save config
save_config({'frame_step': 5, 'jpeg_quality': 90})
```

## Tutorials

### Tutorial 1: Basic Frame Extraction

**Goal**: Extract all frames from a video file.

```bash
video2image -i my_video.mp4 -o frames/
```

This creates a folder `frames/my_video/` with all frames named `frame_0001.jpg`, `frame_0002.jpg`, etc.

### Tutorial 2: Extract Key Moments

**Goal**: Extract only important scenes using scene detection.

```bash
video2image -i movie.mp4 --scene-detection --scene-threshold 40
```

This extracts frames only when significant scene changes occur.

### Tutorial 3: Create Thumbnail Strip

**Goal**: Extract resized frames for a contact sheet.

```bash
video2image -i video.mp4 \
  --frame-step 30 \
  --resize-width 320 \
  --prefix thumb_ \
  --grayscale
```

This extracts every 30th frame, resizes to 320px width, and converts to grayscale.

### Tutorial 4: Time-Based Extraction

**Goal**: Extract frames from specific time ranges.

```bash
# Extract frames from 0:10 to 0:30
video2image -i video.mp4 --start-time 10 --end-time 30

# Extract first 5 seconds
video2image -i video.mp4 --end-time 5
```

### Tutorial 5: Batch Processing Multiple Videos

**Goal**: Process an entire video library.

```bash
# Process all videos in directory tree
video2image -i ~/Videos/ --recursive --parallel --max-workers 8

# Process only MP4 and MKV files
video2image -i ~/Videos/ --recursive --patterns "*.mp4" "*.mkv"
```

### Tutorial 6: Save Default Settings

**Goal**: Configure default extraction settings.

```bash
# Save your preferred settings
video2image --save-config \
  --frame-step 3 \
  --jpeg-quality 90 \
  --resize-width 1920

# Now these settings are used by default
video2image -i video.mp4
```

## FAQ

### Q: How do I extract exactly one frame per second?
**A**: Use `--frame-step` with your video's FPS, or calculate: `--frame-step $(fps)`

For a 30fps video:
```bash
video2image -i video.mp4 --frame-step 30
```

### Q: Can I extract frames from specific timestamps?
**A**: Yes! Use `--start-time` and `--end-time`:
```bash
video2image -i video.mp4 --start-time 60 --end-time 120
```

### Q: How do I reduce file size of extracted frames?
**A**: Lower JPEG quality or use PNG compression:
```bash
video2image -i video.mp4 --jpeg-quality 70
# or
video2image -i video.mp4 -f png --png-compression 9
```

### Q: My output folder is huge. How can I reduce the number of frames?
**A**: Use multiple strategies:
```bash
video2image -i video.mp4 \
  --frame-step 5 \
  --scene-detection \
  --remove-duplicates
```

### Q: How do I create custom filenames?
**A**: Use `--naming-pattern`:
```bash
video2image -i video.mp4 \
  --naming-pattern "{video}_scene{frame:04d}_t{time}"
```

Output: `myvideo_scene0001_t0.033.jpg`

### Q: Can I process videos in subdirectories automatically?
**A**: Yes, use `--recursive`:
```bash
video2image -i ./all_videos/ --recursive --parallel
```

### Q: Where is the config file stored?
**A**: Default location is `~/.video2image/config.yaml`

### Q: How do I reset to default settings?
**A**: Delete the config file:
```bash
rm ~/.video2image/config.yaml
```

## Configuration

### Config File Location
Default: `~/.video2image/config.yaml`

### Example Config
```yaml
frame_step: 3
jpeg_quality: 90
png_compression: 6
image_format: jpg
scene_detection: true
scene_threshold: 35
resize_width: 1920
grayscale: false
naming_pattern: "{video}_{frame:04d}"
```

### Setting Config via CLI
```bash
# Save current options as defaults
video2image --save-config --frame-step 5 --jpeg-quality 85

# View current config
video2image --show-config

# Use custom config file
video2image -i video.mp4 --config /path/to/custom.yaml
```

---

For more information, visit: https://github.com/sakthivelj/video2image
