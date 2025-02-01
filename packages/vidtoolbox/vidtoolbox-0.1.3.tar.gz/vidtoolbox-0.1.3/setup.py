from setuptools import setup, find_packages

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vidtoolbox",
    version="0.1.3",
    author="nkliu1772",
    description="A Python toolbox for managing and processing videos efficiently.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nkliu1772/vidtoolbox",
    packages=find_packages(),
    install_requires=[
        "ffmpeg-python",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Video",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "vid-info=vidtoolbox.video_info:main",
            "vid-merge=vidtoolbox.merge_videos:main",
            "vid-timestamps=vidtoolbox.generate_timestamps:main",
        ],
    },
)
