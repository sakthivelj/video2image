from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='video2image',
    version='1.3.3',
    author='Sakthivel J',
    author_email='sakthivel1023@gmail.com',
    description='A Python script to extract frames from video files.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sakthivelj/video2image',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Multimedia :: Video',
    ],
    python_requires='>=3.8',
    install_requires=[
        'opencv-python',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'video2image = video2image.__init__:main'
        ]
    }
)
