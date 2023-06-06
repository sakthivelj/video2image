from setuptools import setup, find_packages

setup(
    name='video2images',
    version='1.0.0',
    author='Sakthivel J',
    author_email='sakthivel1023@gmail.com',
    description='A Python script to extract frames from video files.',
    url='https://github.com/sakthivelj/video2images',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        
    ],
)