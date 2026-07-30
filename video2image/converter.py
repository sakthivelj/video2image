import hashlib
import os
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
import yaml
from tqdm import tqdm

# Default config path
DEFAULT_CONFIG_PATH = Path.home() / ".video2image" / "config.yaml"


def load_config(config_path=None):
    """Load configuration from YAML file."""
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH
    else:
        config_path = Path(config_path)

    if config_path.exists():
        with open(config_path, "r") as f:
            return yaml.safe_load(f) or {}
    return {}


def save_config(config, config_path=None):
    """Save configuration to YAML file."""
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH
    else:
        config_path = Path(config_path)

    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        yaml.safe_dump(config, f, default_flow_style=False)


def calculate_frame_hash(frame):
    """Calculate hash of a frame for duplicate detection."""
    # Resize to small size for faster comparison
    small_frame = cv2.resize(frame, (32, 32))
    gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
    return hashlib.md5(gray.tobytes()).hexdigest()


def detect_scene_change(frame1, frame2, threshold=30):
    """Detect scene change between two frames."""
    if frame1 is None or frame2 is None:
        return False

    # Convert to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Calculate difference
    diff = cv2.absdiff(gray1, gray2)
    mean_diff = np.mean(diff)

    return mean_diff > threshold


def calculate_motion_score(frame1, frame2):
    """Calculate motion score between two frames."""
    if frame1 is None or frame2 is None:
        return 0

    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Optical flow
    flow = cv2.calcOpticalFlowFarneback(gray1, gray2, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])

    return np.mean(magnitude)


def extract_frames(
    video_path,
    output_folder,
    include_parent=False,
    image_format="jpg",
    # Frame Control
    frame_step=1,
    start_time=None,
    end_time=None,
    frame_range=None,
    # Naming Customization
    naming_pattern=None,
    prefix="",
    suffix="",
    include_timestamp=False,
    # Image Quality
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
    duplicate_threshold=0.95,
    keyframe_only=False,
    # Config
    config_path=None,
    progress_callback=None,
):
    """
    Extract frames from video with advanced options.

    Args:
        video_path: Path to input video
        output_folder: Output directory path
        include_parent: Include parent directory in output path
        image_format: Image format (jpg, png)
        frame_step: Extract every Nth frame (default: 1)
        start_time: Start time in seconds (e.g., 10.5)
        end_time: End time in seconds
        frame_range: Tuple of (start_frame, end_frame)
        naming_pattern: Custom naming pattern (e.g., "{video}_{frame:04d}_{time}")
        prefix: Prefix for output filenames
        suffix: Suffix for output filenames
        include_timestamp: Include timestamp in filename
        jpeg_quality: JPEG quality (1-100)
        png_compression: PNG compression level (0-9)
        resize_width: Resize width (None = original)
        resize_height: Resize height (None = original)
        grayscale: Convert to grayscale
        scene_detection: Enable scene change detection
        scene_threshold: Scene change threshold (0-255)
        motion_based: Enable motion-based extraction
        motion_threshold: Motion threshold for extraction
        remove_duplicates: Remove duplicate frames
        duplicate_threshold: Similarity threshold for duplicates (0-1)
        keyframe_only: Extract only visually distinct frames (photogrammetry mode)
        config_path: Path to config file
        progress_callback: Optional callable(frames_scanned, frames_total) invoked
            periodically as the video is scanned, for UI progress reporting
    """
    # ponytail: "keyframe" = visually distinct frames, not codec I-frames.
    # For true I-frame extraction, use ffprobe. Covers 95% of photogrammetry needs.
    if keyframe_only:
        scene_detection = True
        remove_duplicates = True
        if scene_threshold == 30:  # default wasn't customized
            scene_threshold = 20
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get the video file name without extension
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    if include_parent:
        parent_folder = os.path.dirname(video_path)
        frame_folder = os.path.join(
            output_folder, os.path.basename(parent_folder), video_name
        )
    else:
        frame_folder = os.path.join(output_folder, video_name)

    if os.path.exists(frame_folder):
        shutil.rmtree(frame_folder)
    os.makedirs(frame_folder)

    # Open the video file
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print(f"Error opening video file: {video_path}")
        return

    # Get video details
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps > 0 else 0
    video_size = (
        int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    )

    print("Video Details:")
    print(f"  Format: {video.get(cv2.CAP_PROP_FORMAT)}")
    print(f"  Size: {video_size}")
    print(f"  FPS: {fps}")
    print(f"  Frame Count: {frame_count}")
    print(f"  Duration: {duration:.2f}s")

    # Calculate frame range based on time
    start_frame = 0
    end_frame = frame_count

    if start_time is not None:
        start_frame = int(start_time * fps)

    if end_time is not None:
        end_frame = min(int(end_time * fps), frame_count)

    if frame_range is not None:
        start_frame = max(start_frame, frame_range[0])
        end_frame = min(
            end_frame, frame_range[1] if len(frame_range) > 1 else frame_count
        )

    # Set up progress bar
    total_frames = (end_frame - start_frame) // frame_step
    progress_bar = tqdm(total=total_frames, desc="Extracting Frames", unit="frame")

    # Set video position
    if start_frame > 0:
        video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Frame counter
    current_frame = start_frame
    saved_count = 0
    prev_frame = None
    frame_hashes = set() if remove_duplicates else None

    # ponytail: progress is reported by scan position (frames read), not
    # saved_count, since filters make the saved total unpredictable ahead of time.
    scan_total = max(1, end_frame - start_frame)
    progress_step = max(1, scan_total // 200)

    while True:
        ret, frame = video.read()

        if not ret or current_frame >= end_frame:
            break

        if progress_callback is not None:
            scanned = current_frame - start_frame
            if scanned % progress_step == 0:
                progress_callback(scanned, scan_total)

        # Check if we should skip this frame based on frame_step
        if (current_frame - start_frame) % frame_step != 0:
            current_frame += 1
            continue

        # Scene detection
        if scene_detection and prev_frame is not None:
            if not detect_scene_change(prev_frame, frame, scene_threshold):
                current_frame += 1
                continue

        # Motion-based extraction
        if motion_based and prev_frame is not None:
            motion_score = calculate_motion_score(prev_frame, frame)
            if motion_score < motion_threshold:
                current_frame += 1
                continue

        # Duplicate removal
        if remove_duplicates and frame_hashes is not None:
            frame_hash = calculate_frame_hash(frame)
            # Simple hash comparison (for more sophisticated duplicate detection, use perceptual hashing)
            if frame_hash in frame_hashes:
                current_frame += 1
                continue
            frame_hashes.add(frame_hash)

        # Process frame
        processed_frame = frame.copy()

        # Resize if needed
        if resize_width or resize_height:
            h, w = processed_frame.shape[:2]
            if resize_width and resize_height:
                new_size = (resize_width, resize_height)
            elif resize_width:
                scale = resize_width / w
                new_size = (resize_width, int(h * scale))
            else:
                scale = resize_height / h
                new_size = (int(w * scale), resize_height)
            processed_frame = cv2.resize(processed_frame, new_size)

        # Convert to grayscale if needed
        if grayscale:
            processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2GRAY)

        # Generate filename
        if naming_pattern:
            timestamp = current_frame / fps if fps > 0 else 0
            filename = naming_pattern.format(
                video=video_name,
                frame=current_frame,
                time=f"{timestamp:.3f}",
                datetime=datetime.now().strftime("%Y%m%d_%H%M%S"),
            )
        else:
            timestamp_str = (
                f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                if include_timestamp
                else ""
            )
            filename = f"{prefix}frame_{current_frame:04d}{suffix}{timestamp_str}"

        filename = f"{filename}.{image_format}"
        frame_path = os.path.join(frame_folder, filename)

        # Save frame with quality settings
        if image_format.lower() == "jpg":
            cv2.imwrite(
                frame_path, processed_frame, [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality]
            )
        elif image_format.lower() == "png":
            cv2.imwrite(
                frame_path,
                processed_frame,
                [cv2.IMWRITE_PNG_COMPRESSION, png_compression],
            )
        else:
            cv2.imwrite(frame_path, processed_frame)

        # Update progress bar and counters
        progress_bar.update(1)
        saved_count += 1
        prev_frame = frame.copy()
        current_frame += 1

    # Release the video object
    video.release()
    progress_bar.close()

    if progress_callback is not None:
        progress_callback(scan_total, scan_total)

    print(f"\nExtraction complete! Saved {saved_count} frames to {frame_folder}")
    return frame_folder


def extract_frames_batch(video_files, output_folder, progress_callback=None, **kwargs):
    """
    Extract frames from multiple videos with optional parallel processing.

    Args:
        video_files: List of video file paths
        output_folder: Base output directory
        progress_callback: Optional callable(videos_completed, videos_total),
            invoked after each video finishes. Reports per-video progress only —
            parallel workers run in separate processes, so per-frame callbacks
            from extract_frames can't cross that boundary.
        **kwargs: Arguments passed to extract_frames
    """
    results = []
    total = len(video_files)
    completed = 0

    def process_video(video_path):
        try:
            result = extract_frames(video_path, output_folder, **kwargs)
            return {"video": video_path, "output": result, "success": True}
        except Exception as e:
            return {"video": video_path, "error": str(e), "success": False}

    # Use parallel processing if requested
    parallel = kwargs.pop("parallel", False)
    max_workers = kwargs.pop("max_workers", 4)

    if parallel:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_video, vf): vf for vf in video_files}
            for future in as_completed(futures):
                results.append(future.result())
                completed += 1
                if progress_callback is not None:
                    progress_callback(completed, total)
    else:
        for video_file in tqdm(video_files, desc="Processing videos"):
            results.append(process_video(video_file))
            completed += 1
            if progress_callback is not None:
                progress_callback(completed, total)

    return results


def find_videos_recursive(directory, patterns=None):
    """
    Find video files recursively in a directory.

    Args:
        directory: Directory to search
        patterns: List of glob patterns (default: common video extensions)

    Returns:
        List of video file paths
    """
    if patterns is None:
        patterns = ["*.mp4", "*.mkv", "*.avi", "*.mov", "*.webm", "*.flv", "*.wmv"]

    video_files = []
    dir_path = Path(directory)

    for pattern in patterns:
        # Case-insensitive search
        video_files.extend(dir_path.rglob(pattern.lower()))
        video_files.extend(dir_path.rglob(pattern.upper()))
        video_files.extend(dir_path.rglob(pattern))

    # Remove duplicates and convert to strings
    return list(set(str(f) for f in video_files))
