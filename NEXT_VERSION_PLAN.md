# Next Version Release Plan (v1.4.0)

## Overview
This document outlines planned features and improvements for the next major release of **video2image**. The current version (1.3.3) provides basic frame extraction functionality. This release plan focuses on enhancing usability, adding advanced features, and improving the overall user experience.

---

## 🎯 Planned Features

### 1. Frame Extraction Control ⭐ HIGH PRIORITY
**Description:** Allow users to control which frames are extracted instead of extracting every single frame.

**Features:**
- **Frame interval/skip option**: Extract every Nth frame (e.g., `--interval 5` extracts every 5th frame)
- **Start/End frame selection**: Extract only frames within a specific range (e.g., `--start-frame 100 --end-frame 500`)
- **Time-based extraction**: Extract frames at specific time intervals (e.g., `--every-seconds 2` extracts a frame every 2 seconds)
- **FPS-based extraction**: Extract frames at a target FPS rate (e.g., `--target-fps 1` extracts 1 frame per second)

**CLI Examples:**
```bash
# Extract every 10th frame
video2image -i video.mp4 -o output --interval 10

# Extract frames 100 to 500
video2image -i video.mp4 -o output --start-frame 100 --end-frame 500

# Extract one frame every 5 seconds
video2image -i video.mp4 -o output --every-seconds 5

# Extract at 2 FPS regardless of original video FPS
video2image -i video.mp4 -o output --target-fps 2
```

---

### 2. Output File Naming Customization ⭐ HIGH PRIORITY
**Description:** Provide flexible naming conventions for extracted frames.

**Features:**
- **Custom naming patterns**: Support patterns like `{video_name}_frame_{number}`, `{timestamp}_{number}`, etc.
- **Timestamp-based naming**: Name files with actual timestamps from the video (e.g., `frame_00h01m23s.jpg`)
- **Zero-padding control**: Allow users to specify padding (e.g., `--padding 6` produces `frame_000001.jpg`)
- **Prefix/Suffix options**: Add custom prefixes or suffixes to filenames

**CLI Examples:**
```bash
# Custom pattern
video2image -i video.mp4 -o output --name-pattern "{video}_f{num:05d}"

# Timestamp-based naming
video2image -i video.mp4 -o output --timestamp-names

# Custom prefix
video2image -i video.mp4 -o output --prefix "scene1_"
```

---

### 3. Image Quality & Compression Control ⭐ MEDIUM PRIORITY
**Description:** Give users control over output image quality and compression settings.

**Features:**
- **JPEG quality setting**: Adjust JPEG compression quality (1-100)
- **PNG compression level**: Control PNG compression (0-9)
- **Image resizing**: Resize frames during extraction (e.g., `--resize 1920x1080` or `--scale 0.5`)
- **Color space conversion**: Option to convert to grayscale, BGR, RGB, etc.

**CLI Examples:**
```bash
# High-quality JPEG
video2image -i video.mp4 -o output --jpeg-quality 95

# Compress PNG
video2image -i video.mp4 -o output --png-compression 9

# Resize to 50% of original
video2image -i video.mp4 -o output --scale 0.5

# Convert to grayscale
video2image -i video.mp4 -o output --grayscale
```

---

### 4. Video Information & Preview ⭐ MEDIUM PRIORITY
**Description:** Enhanced video information display and preview capabilities.

**Features:**
- **Detailed video info command**: Show comprehensive video metadata without extraction
- **Sample frame preview**: Extract and display a few sample frames before full extraction
- **Duration display**: Show video duration in human-readable format
- **Codec information**: Display video codec details

**CLI Examples:**
```bash
# Show video info only
video2image --info video.mp4

# Preview first 5 frames
video2image -i video.mp4 --preview --preview-count 5
```

---

### 5. Batch Processing Enhancements ⭐ HIGH PRIORITY
**Description:** Improve batch processing capabilities for large-scale operations.

**Features:**
- **Recursive directory scanning**: Process videos in subdirectories (`--recursive`)
- **File pattern matching**: Use glob patterns to select specific videos (`--pattern "*.mp4"`)
- **Exclude patterns**: Exclude certain files or directories (`--exclude "*temp*"`)
- **Parallel processing**: Process multiple videos simultaneously (`--workers 4`)
- **Batch summary report**: Generate a summary after batch processing completes

**CLI Examples:**
```bash
# Recursive processing
video2image -i ./videos -o ./output --recursive

# Parallel processing with 4 workers
video2image -i ./videos -o ./output --workers 4

# Specific pattern matching
video2image -i ./videos -o ./output --pattern "*2024*.mp4"
```

---

### 6. Configuration File Support ⭐ MEDIUM PRIORITY
**Description:** Allow users to save default settings in a configuration file.

**Features:**
- **Config file generation**: Create default config file with `--init-config`
- **Persistent settings**: Store commonly used options (format, quality, naming, etc.)
- **Profile support**: Multiple configuration profiles for different use cases
- **Environment variable overrides**: Allow config via environment variables

**CLI Examples:**
```bash
# Generate default config
video2image --init-config

# Use specific config profile
video2image -i video.mp4 -o output --config-profile "high-quality"
```

**Config File Example (~/.video2image/config.yaml):**
```yaml
default_format: png
jpeg_quality: 90
png_compression: 6
naming_pattern: "{video}_frame_{num:05d}"
include_parent: false
parallel_workers: 2
```

---

### 7. Progress & Logging Improvements ⭐ LOW PRIORITY
**Description:** Enhanced progress tracking and logging capabilities.

**Features:**
- **Verbose mode**: Detailed logging for debugging (`--verbose`)
- **Log file output**: Save logs to file (`--log-file output.log`)
- **Progress bar styles**: Different progress bar formats (`--progress-style "simple"`)
- **ETA display**: Show estimated time remaining
- **Silent mode**: Suppress all output except errors (`--quiet`)

---

### 8. Format Extensions ⭐ LOW PRIORITY
**Description:** Support additional output formats beyond JPG and PNG.

**Features:**
- **WebP support**: Modern web-friendly format with better compression
- **TIFF support**: Lossless format for professional use
- **BMP support**: Uncompressed bitmap format
- **HEIC support**: Apple's efficient image format

**CLI Examples:**
```bash
video2image -i video.mp4 -o output -f webp --webp-quality 80
video2image -i video.mp4 -o output -f tiff
```

---

### 9. Smart Extraction Features ⭐ MEDIUM PRIORITY
**Description:** Intelligent frame selection based on content analysis.

**Features:**
- **Scene detection**: Automatically detect scene changes and extract keyframes
- **Motion-based extraction**: Extract frames with significant motion changes
- **Quality filtering**: Skip blurry or low-quality frames
- **Duplicate detection**: Avoid extracting nearly identical frames

**CLI Examples:**
```bash
# Extract only scene change frames
video2image -i video.mp4 -o output --scene-detection

# Skip blurry frames
video2image -i video.mp4 -o output --skip-blurry

# Remove duplicate frames (threshold-based)
video2image -i video.mp4 -o output --remove-duplicates --threshold 0.95
```

---

### 10. API & Library Usage ⭐ MEDIUM PRIORITY
**Description:** Improve programmatic usage of video2image as a library.

**Features:**
- **Python API documentation**: Comprehensive docs for library usage
- **Callback support**: Allow callbacks for progress, completion, errors
- **Async support**: Asynchronous frame extraction for GUI apps
- **Return values**: Better return types with metadata about extraction

**Python API Example:**
```python
from video2image import VideoConverter

converter = VideoConverter(
    output_format="png",
    jpeg_quality=90,
    on_progress=lambda current, total: print(f"{current}/{total}"),
    on_complete=lambda path: print(f"Done: {path}")
)

result = converter.extract(
    video_path="video.mp4",
    output_dir="./frames",
    interval=5
)

print(f"Extracted {result.frame_count} frames")
```

---

### 11. Testing & CI/CD Enhancements ⭐ HIGH PRIORITY
**Description:** Strengthen testing infrastructure and deployment pipeline.

**Features:**
- **Unit tests**: Comprehensive test suite for all functions
- **Integration tests**: End-to-end testing with sample videos
- **Test coverage reporting**: Track code coverage (target: >80%)
- **Multi-platform testing**: Test on Windows, macOS, Linux
- **Automated PyPI deployment**: CI/CD pipeline for releases
- **Pre-commit hooks**: Code quality checks before commits

---

### 12. Documentation Improvements ⭐ HIGH PRIORITY
**Description:** Enhance user documentation and examples.

**Features:**
- **Tutorial section**: Step-by-step guides for common use cases
- **API reference**: Complete function/method documentation
- **FAQ section**: Common questions and troubleshooting
- **Video tutorials**: Link to demonstration videos
- **Comparison table**: Feature comparison with alternatives
- **Contributing guide**: Clear guidelines for contributors

---

## 📋 Version Roadmap

### v1.4.0 (Next Minor Release)
- ✅ Frame interval/skip option
- ✅ Start/End frame selection
- ✅ Time-based extraction
- ✅ JPEG quality setting
- ✅ Image resizing
- ✅ Verbose/Quiet modes
- ✅ Basic unit tests

### v1.5.0
- ✅ Custom naming patterns
- ✅ Timestamp-based naming
- ✅ Scene detection
- ✅ Configuration file support
- ✅ WebP format support
- ✅ Python API improvements

### v1.6.0
- ✅ Recursive directory scanning
- ✅ Parallel processing
- ✅ Motion-based extraction
- ✅ Duplicate detection
- ✅ Comprehensive test suite
- ✅ Enhanced documentation

### v2.0.0 (Major Release)
- ✅ Complete API redesign
- ✅ Async support
- ✅ All smart extraction features
- ✅ Multi-platform GUI (optional)
- ✅ Plugin architecture

---

## 🔧 Technical Debt & Refactoring

### Current Issues to Address:
1. **Hard-coded video extensions**: Make extension list configurable
2. **No error handling for cv2.imwrite**: Add try-catch and error reporting
3. **Memory management**: Ensure proper resource cleanup for large videos
4. **Path validation**: Validate input/output paths before processing
5. **Unicode path support**: Test and ensure Unicode paths work correctly
6. **Large file handling**: Optimize for very long videos (>2 hours)

---

## 📊 Success Metrics

- [ ] Increase test coverage from 0% to >80%
- [ ] Reduce frame extraction time by 20% with optimizations
- [ ] Support 5+ additional output formats
- [ ] Achieve 100% type hint coverage
- [ ] Document all public APIs
- [ ] Add 10+ real-world usage examples
- [ ] Support parallel processing with 90% efficiency
- [ ] Implement 5+ smart extraction algorithms

---

## 🤝 Community Feedback

We welcome feedback on these planned features! Please contribute by:
- Opening issues with feature requests
- Voting on existing feature requests
- Submitting pull requests
- Sharing use cases and workflows

**Repository:** https://github.com/sakthivelj/video2image  
**Issues:** https://github.com/sakthivelj/video2image/issues

---

## 📝 Notes

- Priority levels: ⭐ HIGH | ⭐⭐ MEDIUM | ⭐⭐⭐ LOW
- Features may be adjusted based on community feedback
- Timeline estimates are subject to change
- Breaking changes will be clearly documented in release notes

---

*Last Updated: 2024*
*Version: 1.3.3 → Next: 1.4.0*
