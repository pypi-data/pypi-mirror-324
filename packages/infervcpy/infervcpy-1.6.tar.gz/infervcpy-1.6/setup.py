import os
import platform
import pkg_resources
from setuptools import find_packages, setup

setup(
    name="infervcpy",
    version="1.6",
    description="Python wrapper for fast inference with rvc",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    readme="README.md",
    python_requires=">=3.10",
    author="Neofr",
    url="https://github.com/thatneos/python-rvc-inference.git",
    license="MIT",
    packages=find_packages(),
    package_data={'': ['*.txt', '*.rep', '*.pickle']},
    install_requires=[
        "torch",
        "torchaudio",
        "gradio==4.40.0",
        "praat-parselmouth>=0.4.3",
        "pyworld==0.3.2",
        "faiss-cpu==1.7.3",
        "torchcrepe==0.0.20",
        "ffmpeg-python>=0.2.0",
        "fairseq==0.12.2",
        "typeguard==4.2.0",
        "soundfile",
        "yt-dlp",
        "audio-separator[gpu]",
        "librosa",
        "numpy",
    ],
    include_package_data=True,
    extras_require={"all": [
        "scipy",
        "numba==0.56.4",
        "edge-tts"
        ]},
)
