import argparse
import os
import glob

from .converter import extract_frames

def main():
    parser = argparse.ArgumentParser(description="Extract frames from video file(s)")
    parser.add_argument("-i", "--input", required=True, help="Path to the input video file or directory")
    parser.add_argument("-o", "--output", default="", help="Path to the output directory\n"
                                                           "(default: create a directory with the same name as the input video in the input directory)")
    parser.add_argument("-p", "--parent", action="store_true", help="Include the parent directory of the video in the output directory path")
    parser.add_argument("-H", "--show-help", action="help", help="Show this help message and exit")
    parser.add_argument("-f", "--format", default="jpg", choices=["jpg", "png"], help="Image format for extracted frames (default: jpg)")
    args = parser.parse_args()
    
    # Use input video directory as output if -o is empty
    if args.output == "":
        args.output = os.path.dirname(args.input)
    
    # Handle single video file
    if os.path.isfile(args.input):
        extract_frames(args.input, args.output, args.parent, args.format)
    
    # Handle directory with multiple video files
    elif os.path.isdir(args.input):
        video_files = glob.glob(os.path.join(args.input, "*.mp4"))
        if len(video_files) == 0:
            print("No video files found in the input directory")
        else:
            for video_file in video_files:
                extract_frames(video_file, args.output, args.parent, args.format)
    
    else:
        print("Invalid input: not a file or directory")


if __name__ == "__main__":
    main()
