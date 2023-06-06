# video2images
Video2Images is a Python script that allows you to extract frames from a video file or multiple video files and save them as individual images. It provides a simple and convenient way to convert videos into a series of images, which can be useful for various applications such as computer vision, machine learning, data analysis, and more.


Certainly! Here's a README.md template with an easy-to-copy script format:

```markdown
# Video to Images Converter

This script allows you to extract frames from a video file or multiple video files and save them as individual images.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/video-to-images-converter.git
   ```

2. Navigate to the project directory:

   ```shell
   cd video-to-images-converter
   ```

3. Create and activate a virtual environment (optional but recommended):

   ```shell
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

## Usage

To extract frames from a video file:

```shell
python script.py -i /path/to/video.mp4 -o /path/to/output/folder
```

To extract frames from a directory of video files:

```shell
python script.py -i /path/to/video/directory -o /path/to/output/folder
```

Options:
- `-i`, `--input`: Path to the input video file or directory.
- `-o`, `--output`: Path to the output directory (default: create a directory with the same name as the input video in the input directory).
- `-p`, `--parent`: Include the parent directory of the video in the output directory path.
- `-h`, `--help`: Show the help message.
