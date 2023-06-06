import os
import cv2
import shutil
from tqdm import tqdm

def extract_frames(video_path, output_folder, include_parent=False, image_format="jpg"):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get the video file name without extension
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    if include_parent:
        # Include the parent directory in the output folder path
        parent_folder = os.path.dirname(video_path)
        frame_folder = os.path.join(output_folder, os.path.basename(parent_folder), video_name)
    else:
        # Create a folder for the video frames directly in the output folder
        frame_folder = os.path.join(output_folder, video_name)

    if os.path.exists(frame_folder):
        # If the folder already exists, remove it and create again
        shutil.rmtree(frame_folder)
    os.makedirs(frame_folder)

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Check if video file opened successfully
    if not video.isOpened():
        print(f"Error opening video file: {video_path}")
        return

    # Get video details
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video_format = video.get(cv2.CAP_PROP_FORMAT)
    video_size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    print(f"Video Details:")
    print(f"  Format: {video_format}")
    print(f"  Size: {video_size}")
    print(f"  FPS: {fps}")
    print(f"  Frame Count: {frame_count}")

    # Set up progress bar
    progress_bar = tqdm(total=frame_count, desc="Extracting Frames", unit="frame")

    while True:
        # Read the next frame from the video
        ret, frame = video.read()

        # If frame reading was not successful, break the loop
        if not ret:
            break

        # Save the frame as an image
        frame_path = os.path.join(frame_folder, f"frame_{frame_count:04d}.{image_format}")
        cv2.imwrite(frame_path, frame)

        # Update progress bar
        progress_bar.update(1)

        # Decrement frame count
        frame_count -= 1

    # Release the video object
    video.release()

    # Close progress bar
    progress_bar.close()
