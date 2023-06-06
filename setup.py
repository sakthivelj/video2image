from setuptools import setup, find_packages

setup(
    name='video2image',
    version='1.3.0',
    author='Sakthivel J',
    author_email='sakthivel1023@gmail.com',
    description='A Python script to extract frames from video files.',
    url='https://github.com/sakthivelj/video2image',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
    ],
    entry_points={
        'console_scripts': [
            'video2image = video2image.__init__:main'
        ]
    }
)
