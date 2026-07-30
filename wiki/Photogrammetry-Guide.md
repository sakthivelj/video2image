# Photogrammetry Guide

## What is Photogrammetry?

Photogrammetry is the process of creating 3D models from photographs. Software like Meshroom, COLMAP, and Reality Capture analyzes overlapping images to reconstruct 3D geometry.

**Video → Frames → 3D Model**

video2image bridges the gap between video capture and photogrammetry software by extracting the right frames from your videos.

## Why Extract Frames from Video?

| Method | Pros | Cons |
|--------|------|------|
| **Photos** | Higher quality, controlled exposure | Slow capture, easy to miss angles |
| **Video → Frames** | Fast capture, continuous coverage | Redundant frames, motion blur |

video2image solves the "redundant frames" problem by intelligently selecting only the frames that matter.

## Recommended Settings

### Walking / Handheld Video

```
Frame step: 5-10
Key Frame Extraction: ✓ ON
Format: PNG
```

Walking videos produce many similar frames. A frame step of 5-10 combined with key frame extraction gives excellent coverage without redundancy.

### Drone / Aerial Footage

```
Frame step: 2-3
Scene Detection: ✓ ON (threshold: 25)
Format: PNG
```

Drone footage typically has faster movement. Use a lower frame step and scene detection to capture terrain changes.

### Turntable / Object Scanning

```
Frame step: 1-3
Remove Duplicates: ✓ ON
Format: PNG
Quality: Keep original resolution
```

For turntable scans, you want dense coverage. Use a low frame step with duplicate removal to eliminate frames where the object hasn't rotated enough.

### Indoor / Room Scanning

```
Key Frame Extraction: ✓ ON
Frame step: 3-5
Format: PNG
```

Indoor scans benefit most from key frame extraction, which captures each distinct viewpoint as you move through the space.

## Understanding the Extraction Features

### Key Frame Extraction (Recommended)

This is the **best option for photogrammetry**. When enabled, it:
1. Activates scene detection to find visually distinct frames
2. Removes duplicate/near-identical frames
3. Uses optimized thresholds for photogrammetry

Result: Only frames that represent unique viewpoints are extracted.

### Scene Detection

Compares consecutive frames and extracts only when a significant visual change occurs.

- **Low threshold (10-20):** More sensitive, captures subtle changes → more frames
- **Medium threshold (25-40):** Balanced — good default
- **High threshold (50+):** Only major scene changes → fewer frames

### Motion-based Extraction

Measures optical flow between frames. Extracts frames where the camera or objects are moving significantly.

- Useful for: surveillance footage, action sequences
- Less useful for: photogrammetry (use scene detection instead)

### Remove Duplicates

Hashes each frame and skips frames that are visually identical to previously extracted frames. Catches cases where the camera is stationary.

## Output Format Recommendations

| Format | Use Case |
|--------|----------|
| **PNG** | Best quality, lossless. Recommended for photogrammetry. |
| **JPG (quality 95)** | Good quality, smaller files. Use when storage is limited. |
| **JPG (quality 80)** | Acceptable for preview/testing, not recommended for final reconstruction. |

## Compatible Photogrammetry Software

| Software | Free? | Notes |
|----------|-------|-------|
| [Meshroom](https://alicevision.org/#meshroom) | ✅ Yes | Open-source, GPU required (CUDA) |
| [COLMAP](https://colmap.github.io/) | ✅ Yes | Open-source, very accurate |
| [Reality Capture](https://www.capturingreality.com/) | ❌ Paid | Fastest, best results |
| [Agisoft Metashape](https://www.agisoft.com/) | ❌ Paid | Industry standard |
| [3DF Zephyr](https://www.3dflow.net/) | 🟡 Free tier | Good for beginners |
| [Polycam](https://poly.cam/) | 🟡 Free tier | Mobile + desktop |

## Workflow Example

### From Video to 3D Model

1. **Capture video** — Walk slowly around your subject, maintaining overlap between views
2. **Import to video2image** — Open your video file
3. **Enable Key Frame Extraction** — This selects optimal frames
4. **Set output to PNG** — Lossless quality for best reconstruction
5. **Extract frames** — Click "Extract Frames"
6. **Import frames to photogrammetry software** — Open the output folder in Meshroom, COLMAP, etc.

### Tips for Better Results

- **Overlap:** Ensure 60-80% overlap between consecutive extracted frames
- **Lighting:** Consistent, diffused lighting produces best results
- **Motion blur:** Avoid fast camera movements; video2image can't fix blurry frames
- **Resolution:** Keep original resolution unless your software struggles with large images
- **Frame count:** Aim for 50-300 frames per object/scene, depending on complexity
