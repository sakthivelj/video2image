# video2image
Video2Image is a Python script that extracts frames from a video file or a set of video files and saves them as individual images. It provides a simple and convenient way to convert videos into a series of images. This can be useful for various applications such as computer vision, machine learning, data analysis, and more.

## Installation

You can install Video2Image using `pip`. Here are the steps to install it:

1. Open a terminal or command prompt.

2. Run the following command to install the package:
   ```
   pip install video2image
   ```

## Usage

To use Video2Image, follow these steps:

1. Open a terminal or command prompt.

2. Run the `video2image` command followed by the required arguments:

   ```
   video2image -i /path/to/video.mp4 -o /path/to/output/folder
   ```

   Replace `/path/to/video.mp4` with the actual path to your video file, and `/path/to/output/folder` with the desired output folder path.

   The frames will be extracted from the video and saved as individual images in the specified output folder.

   You can also provide additional command-line arguments such as `-p` to include the parent directory in the output path or `-h` to display the help message.

3. If you want to extract frames from multiple video files in a directory, specify the input directory instead of a single video file:

   ```
   video2image -i /path/to/video/directory -o /path/to/output/folder
   ```

   The script will process all the video files in the input directory and save the extracted frames in the output folder.

That's it! You have successfully extracted frames from video files using Video2Image.

## Building from Source

If you want to build the package from source and install it locally, you can follow these steps:

1. Clone the repository:

   ```shell
   git clone https://github.com/sakthivelj/video2image.git
   ```

2. Navigate to the project directory:

   ```shell
   cd video2image
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

5. Run the following command to build and install the package:

   ```shell
   python setup.py install
   ```

   This will install the `video2image` package on your system.

Now you can use the `video2image` command as described in the "Usage" section.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/sakthivelj/video2image/blob/main/LICENSE) file for more information.
