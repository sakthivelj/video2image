# video2images
Video2Images is a Python script that extracts frames from a video file or a set of video files and saves them as individual images. It provides a simple and convenient way to convert videos into a series of images. This can be useful for various applications such as computer vision, machine learning, data analysis, and more.

# Video to Images Converter

The package allows for frames to be extracted and saved individually from video files.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/sakthivelj/video2images.git
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
