from setuptools import setup
from pathlib import Path

setup(
    name='YTSage',
    version='3.5.0',
    author='oop7',
    author_email='oop7_support@proton.me',
    description=' Modern YouTube downloader with a clean PySide6 interface. Download videos in any quality, extract audio, fetch subtitles (including auto-generated), and view video metadata. Built with yt-dlp for reliable performance.',
    long_description=Path('README.md').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    url='https://github.com/oop7/YTSage',
    packages=['YTSage'],  # Explicitly list the package directory
    package_data={'YTSage': ['YTSage.py']}, # Include the Python file within the package
    install_requires=[
        'yt-dlp',
        'PySide6',
        'requests',
        'Pillow',
        'packaging'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'YTSage=YTSage.YTSage:main', # Correct entry point
        ],
    },
)