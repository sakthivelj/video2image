import argparse
import os
import glob
from .converter import (
    extract_frames,
    extract_frames_batch,
    find_videos_recursive,
    load_config,
    save_config,
    DEFAULT_CONFIG_PATH,
)


def parse_frame_range(value):
    """Parse frame range argument (e.g., '100-200' or '100')."""
    if "-" in value:
        parts = value.split("-")
        return (int(parts[0]), int(parts[1]))
    else:
        return (int(value), None)


def main():
    parser = argparse.ArgumentParser(
        description="Extract frames from video file(s) with advanced options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  video2image -i video.mp4 -o output/
  # Extract every 5th frame
  video2image -i video.mp4 --frame-step 5
  # Extract frames from 10s to 30s
  video2image -i video.mp4 --start-time 10 --end-time 30
  # Custom naming pattern
  video2image -i video.mp4 --naming-pattern "{video}_frame{frame:04d}_t{time}"
  # Resize and convert to grayscale
  video2image -i video.mp4 --resize-width 1920 --grayscale
  # Scene detection mode
  video2image -i video.mp4 --scene-detection --scene-threshold 40
  # Process directory recursively
  video2image -i ./videos/ --recursive --parallel
  # Save default config
  video2image --save-config --jpeg-quality 90 --frame-step 3
        """,
    )
    # Input/Output
    parser.add_argument(
        "-i", "--input", help="Path to the input video file or directory"
    )
    parser.add_argument(
        "-o",
        "--output",
        default="",
        help="Path to the output directory (default: same as input)",
    )
    parser.add_argument(
        "-p",
        "--parent",
        action="store_true",
        help="Include the parent directory in the output path",
    )
    # Frame Control
    frame_group = parser.add_argument_group("Frame Control")
    frame_group.add_argument(
        "--frame-step", type=int, default=1, help="Extract every Nth frame (default: 1)"
    )
    frame_group.add_argument(
        "--start-time", type=float, help="Start time in seconds (e.g., 10.5)"
    )
    frame_group.add_argument("--end-time", type=float, help="End time in seconds")
    frame_group.add_argument(
        "--frame-range",
        type=parse_frame_range,
        help="Frame range (e.g., '100-200' or '100')",
    )
    # Naming Customization
    naming_group = parser.add_argument_group("Naming Customization")
    naming_group.add_argument(
        "--naming-pattern",
        help="Custom naming pattern (e.g., '{video}_{frame:04d}_{time}')",
    )
    naming_group.add_argument(
        "--prefix", default="", help="Prefix for output filenames"
    )
    naming_group.add_argument(
        "--suffix", default="", help="Suffix for output filenames"
    )
    naming_group.add_argument(
        "--include-timestamp", action="store_true", help="Include timestamp in filename"
    )
    # Image Quality
    quality_group = parser.add_argument_group("Image Quality")
    quality_group.add_argument(
        "-f",
        "--format",
        default="jpg",
        choices=["jpg", "png"],
        help="Image format (default: jpg)",
    )
    quality_group.add_argument(
        "--jpeg-quality", type=int, default=95, help="JPEG quality 1-100 (default: 95)"
    )
    quality_group.add_argument(
        "--png-compression",
        type=int,
        default=6,
        help="PNG compression 0-9 (default: 6)",
    )
    quality_group.add_argument(
        "--resize-width",
        type=int,
        help="Resize width (maintains aspect ratio if height not specified)",
    )
    quality_group.add_argument(
        "--resize-height",
        type=int,
        help="Resize height (maintains aspect ratio if width not specified)",
    )
    quality_group.add_argument(
        "--grayscale", action="store_true", help="Convert frames to grayscale"
    )
    # Smart Features
    smart_group = parser.add_argument_group("Smart Features")
    smart_group.add_argument(
        "--scene-detection", action="store_true", help="Enable scene change detection"
    )
    smart_group.add_argument(
        "--scene-threshold",
        type=float,
        default=30,
        help="Scene change threshold 0-255 (default: 30)",
    )
    smart_group.add_argument(
        "--motion-based", action="store_true", help="Enable motion-based extraction"
    )
    smart_group.add_argument(
        "--motion-threshold",
        type=float,
        default=5,
        help="Motion threshold (default: 5)",
    )
    smart_group.add_argument(
        "--remove-duplicates", action="store_true", help="Remove duplicate frames"
    )
    # Batch Processing
    batch_group = parser.add_argument_group("Batch Processing")
    batch_group.add_argument(
        "--recursive",
        action="store_true",
        help="Search for videos recursively in directory",
    )
    batch_group.add_argument(
        "--patterns", nargs="+", help="Custom file patterns (e.g., '*.mp4 *.mkv')"
    )
    batch_group.add_argument(
        "--parallel", action="store_true", help="Process multiple videos in parallel"
    )
    batch_group.add_argument(
        "--max-workers", type=int, default=4, help="Max parallel workers (default: 4)"
    )
    # Config
    config_group = parser.add_argument_group("Configuration")
    config_group.add_argument(
        "--config", type=str, help=f"Config file path (default: {DEFAULT_CONFIG_PATH})"
    )
    config_group.add_argument(
        "--save-config",
        action="store_true",
        help="Save current settings as default config",
    )
    config_group.add_argument(
        "--show-config", action="store_true", help="Show current config and exit"
    )
    # Help
    parser.add_argument(
        "-H", "--show-help", action="help", help="Show this help message and exit"
    )
    args = parser.parse_args()
    # Handle config operations (don't require input for these)
    if args.show_config:
        config = load_config(args.config)
        print(f"Current configuration ({DEFAULT_CONFIG_PATH}):")
        if config:
            for key, value in config.items():
                print(f"  {key}: {value}")
        else:
            print("  No configuration found.")
        return
    if args.save_config:
        if not args.input:
            print(
                "Error: --input is required when saving config with video-specific settings"
            )
            return
        config = {
            "frame_step": args.frame_step,
            "jpeg_quality": args.jpeg_quality,
            "png_compression": args.png_compression,
            "image_format": args.format,
        }
        if args.start_time:
            config["start_time"] = args.start_time
        if args.end_time:
            config["end_time"] = args.end_time
        if args.scene_detection:
            config["scene_detection"] = True
            config["scene_threshold"] = args.scene_threshold
        if args.motion_based:
            config["motion_based"] = True
            config["motion_threshold"] = args.motion_threshold
        if args.remove_duplicates:
            config["remove_duplicates"] = True
        if args.resize_width:
            config["resize_width"] = args.resize_width
        if args.resize_height:
            config["resize_height"] = args.resize_height
        if args.grayscale:
            config["grayscale"] = True
        if args.naming_pattern:
            config["naming_pattern"] = args.naming_pattern
        save_config(config, args.config)
        config_path = args.config or DEFAULT_CONFIG_PATH
        print(f"Configuration saved to {config_path}")
        return
    # Use input video directory as output if -o is empty
    if not args.input:
        print("Error: -i/--input is required")
        parser.print_help()
        return
    if args.output == "":
        args.output = os.path.dirname(args.input) or "."
    # Prepare keyword arguments for extract_frames
    kwargs = {
        "include_parent": args.parent,
        "image_format": args.format,
        "frame_step": args.frame_step,
        "start_time": args.start_time,
        "end_time": args.end_time,
        "frame_range": args.frame_range,
        "naming_pattern": args.naming_pattern,
        "prefix": args.prefix,
        "suffix": args.suffix,
        "include_timestamp": args.include_timestamp,
        "jpeg_quality": args.jpeg_quality,
        "png_compression": args.png_compression,
        "resize_width": args.resize_width,
        "resize_height": args.resize_height,
        "grayscale": args.grayscale,
        "scene_detection": args.scene_detection,
        "scene_threshold": args.scene_threshold,
        "motion_based": args.motion_based,
        "motion_threshold": args.motion_threshold,
        "remove_duplicates": args.remove_duplicates,
        "config_path": args.config,
    }

    # Handle single video file
    if os.path.isfile(args.input):
        extract_frames(args.input, args.output, **kwargs)

    # Handle directory with multiple video files
    elif os.path.isdir(args.input):
        if args.recursive:
            video_files = find_videos_recursive(args.input, args.patterns)
        else:
            # Search for common video extensions (case-insensitive)
            patterns = args.patterns or [
                "*.mp4",
                "*.mkv",
                "*.avi",
                "*.mov",
                "*.MP4",
                "*.MKV",
                "*.AVI",
                "*.MOV",
            ]
            video_files = []
            for ext in patterns:
                video_files.extend(glob.glob(os.path.join(args.input, ext)))

        if len(video_files) == 0:
            print("No video files found in the input directory")
        else:
            print(f"Found {len(video_files)} video file(s)")

            if args.parallel or len(video_files) > 1:
                kwargs["parallel"] = args.parallel
                kwargs["max_workers"] = args.max_workers
                results = extract_frames_batch(video_files, args.output, **kwargs)

                # Print summary
                success_count = sum(1 for r in results if r["success"])
                print(
                    f"\nBatch processing complete: {success_count}/{len(results)} succeeded"
                )
            else:
                for video_file in video_files:
                    extract_frames(video_file, args.output, **kwargs)
    else:
        print("Invalid input: not a file or directory")


if __name__ == "__main__":
    main()
