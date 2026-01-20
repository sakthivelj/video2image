# video2image

[![PyPI version](https://badge.fury.io/py/video2image.svg)](https://pypi.org/project/video2image/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/sakthivelj/video2image/actions/workflows/python-publish.yml/badge.svg)](https://github.com/sakthivelj/video2image/actions/workflows/python-publish.yml)
[![GitHub stars](https://img.shields.io/github/stars/sakthivelj/video2image?style=social)](https://github.com/sakthivelj/video2image/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/sakthivelj/video2image?style=social)](https://github.com/sakthivelj/video2image/network/members)

Video2Image is a Python command-line tool that extracts frames from video files and saves them as individual images. It supports batch processing of multiple video files and provides a progress bar for tracking extraction status.

**Features:**
- Extract frames from single video or batch process entire directories
- Support for multiple video formats (MP4, MKV, AVI, MOV)
- Output in JPG or PNG format
- Progress bar with frame count display
- Automatic output folder creation

## Installation

```bash
pip install video2image
```

## Usage

### Extract frames from a single video

```bash
video2image -i /path/to/video.mp4 -o /path/to/output/folder
```

### Extract frames from all videos in a directory

```bash
video2image -i /path/to/video/directory -o /path/to/output/folder
```

### Command-line options

| Option | Description |
|--------|-------------|
| `-i, --input` | Path to input video file or directory (required) |
| `-o, --output` | Path to output directory (default: same as input) |
| `-p, --parent` | Include parent directory in output path |
| `-f, --format` | Image format: `jpg` or `png` (default: jpg) |
| `-H, --show-help` | Show help message |

### Examples

```bash
# Extract frames as PNG
video2image -i video.mp4 -o ./frames -f png

# Extract with parent directory structure
video2image -i /videos/project1/clip.mp4 -o /output -p

# Process all videos in current directory
video2image -i . -o ./extracted_frames
```

## Building from Source

```bash
# Clone the repository
git clone https://github.com/sakthivelj/video2image.git
cd video2image

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install in development mode
pip install -e .
```

## Requirements

- Python 3.8+
- opencv-python
- tqdm

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

**Sakthivel J** - [sakthivel1023@gmail.com](mailto:sakthivel1023@gmail.com)

## Links

- [PyPI Package](https://pypi.org/project/video2image/)
- [GitHub Repository](https://github.com/sakthivelj/video2image)
- [Report Issues](https://github.com/sakthivelj/video2image/issues)
