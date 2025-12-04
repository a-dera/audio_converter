# 🎵 Audio Converter

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FFmpeg Required](https://img.shields.io/badge/FFmpeg-required-red.svg)](https://ffmpeg.org/)

**Python toolkit suite for audio/video conversion and download**

Professional CLI scripts collection for:
- 🎬 Converting MP4 to high-quality MP3 (parallel processing)
- 🔍 Searching YouTube videos from file names
- ⬇️ Downloading MP3 from YouTube in batch mode

---

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Convert MP4 → MP3](#1-convert-mp4--mp3)
  - [Search on YouTube](#2-search-on-youtube)
  - [Download from YouTube](#3-download-from-youtube)
- [Complete Workflow](#-complete-workflow)
- [Advanced Configuration](#-advanced-configuration)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🎬 **audio_converter.py** - MP4 → MP3 Conversion
- ✅ High-quality batch conversion (320 kbps default)
- ✅ Ultra-fast parallel processing (up to 50 threads)
- ✅ Metadata preservation
- ✅ Intelligent error handling
- ✅ Intuitive CLI interface

### 🔍 **youtube_search.py** - YouTube Search
- ✅ Automatic search from MP4 file names
- ✅ Intelligent name cleanup (emojis, special characters)
- ✅ Link file generation
- ✅ Detailed report (found/not found)
- ✅ Built-in rate limiting

### ⬇️ **download_mp3.py** - YouTube Download
- ✅ Batch download from link file
- ✅ Best available audio quality
- ✅ Automatic failure handling
- ✅ Failed links backup
- ✅ Multi-format YouTube support

---

## 🔧 Prerequisites

### Supported Systems
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 20.04+, Debian, Fedora, Arch)

### System Dependencies

#### **FFmpeg** (required for audio_converter.py)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
1. Download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract and add to system PATH
3. Verify: `ffmpeg -version`

**Fedora:**
```bash
sudo dnf install ffmpeg
```

**Arch Linux:**
```bash
sudo pacman -S ffmpeg
```

#### **Python 3.8+** (required)
Check your version:
```bash
python --version
# or
python3 --version
```

---

## 📦 Installation

### Quick Install

```bash
# Clone the repo
git clone https://github.com/a-dera/audio_converter.git
cd audio-converter

# Install Python dependencies
pip install -r requirements.txt

# Verify FFmpeg
ffmpeg -version
```

### Python Dependencies Only

```bash
pip install yt-dlp
```

---

## 🚀 Usage

### 1. Convert MP4 → MP3

**Basic conversion:**
```bash
python audio_converter.py /path/to/videos
```

**Conversion with options:**
```bash
# Custom output folder
python audio_converter.py /videos -o /music

# Custom bitrate (256 kbps)
python audio_converter.py /videos -b 256k

# Sample rate 48kHz
python audio_converter.py /videos -r 48000

# Sequential mode (disable parallel)
python audio_converter.py /videos --sequential
```

**Parameters:**
- `input_folder` : Folder containing MP4 files (required)
- `-o, --output` : Output folder (default: `input_folder/mp3_output`)
- `-b, --bitrate` : Audio bitrate (default: `320k`)
- `-r, --sample-rate` : Sample rate (default: `44100`)
- `-s, --sequential` : Disable parallel processing

**Example output:**
```
==================================================
🎬 MP4 to MP3 Converter - High Quality
==================================================
✅ FFmpeg detected

📂 Source folder: D:\Videos
📁 Output folder: D:\Videos\mp3_output
🎵 Files to convert: 25
🎚️  Quality: 320k @ 44100Hz
⚡ Parallel mode
--------------------------------------------------
✅ video1.mp4 → video1.mp3
✅ video2.mp4 → video2.mp3
...

==================================================
📊 SUMMARY
==================================================
   Total:     25 file(s)
   Succeeded: 25 ✅
   Failed:    0 ❌

✨ Conversion completed successfully!
```

---

### 2. Search on YouTube

**Search from MP4 file names:**
```bash
python youtube_search.py /path/to/videos
```

**With custom output file:**
```bash
python youtube_search.py /path/to/videos my_links.txt
```

**Parameters:**
- `dossier_mp4` : Folder containing MP4 files (required)
- `fichier_sortie.txt` : Output file name (default: `youtube_links.txt`)

**Example output:**
```
============================================================
🔍 YouTube Search from MP4 file names
============================================================

📂 Folder: D:\Downloads\videos\leger
🎵 Files found: 15
📄 Output file: youtube_links.txt
------------------------------------------------------------

[1/15] 🔎 Searching: Livre audio - Le Petit Prince.mp4...
    Query: Livre audio Le Petit Prince...
    ✅ Found: https://www.youtube.com/watch?v=xxxxx

[2/15] 🔎 Searching: Audio - Les Misérables.mp4...
    Query: Audio Les Misérables...
    ✅ Found: https://www.youtube.com/watch?v=yyyyy

...

============================================================
📊 SUMMARY
============================================================
   Total files:   15
   Links found:   13 ✅
   Not found:     2 ❌

✅ Complete file: youtube_links.txt
✅ Links only: youtube_links_links_only.txt
```

**Generated files:**
- `youtube_links.txt` : All results (with comments for not found)
- `youtube_links_links_only.txt` : Valid links only

---

### 3. Download from YouTube

**Download from link file:**
```bash
python download_mp3.py youtube_links.txt
```

**With custom output folder:**
```bash
python download_mp3.py youtube_links.txt D:/Downloads/mp3
```

**Parameters:**
- `fichier_liens.txt` : File containing YouTube links (required)
- `dossier_sortie` : Destination folder (default: `./mp3_downloads`)

**Link file format:**
```txt
# My YouTube videos
https://www.youtube.com/watch?v=xxxxx
https://www.youtube.com/watch?v=yyyyy
# Comments are ignored
https://www.youtube.com/watch?v=zzzzz
```

**Example output:**
```
============================================================
🎵 YouTube Download → MP3
============================================================

📄 Source file: youtube_links.txt
📁 Output folder: D:\Downloads\mp3
🔗 Links to download: 10
------------------------------------------------------------

[1/10] ⬇️  Downloading...
    URL: https://www.youtube.com/watch?v=xxxxx
    ✅ Success!

[2/10] ⬇️  Downloading...
    URL: https://www.youtube.com/watch?v=yyyyy
    ✅ Success!

...

============================================================
📊 SUMMARY
============================================================
   Total:     10
   Succeeded: 9 ✅
   Failed:    1 ❌

📁 MP3 files in: D:\Downloads\mp3

💾 Failed links saved in: failed_downloads.txt

✨ Download complete!
```

---

## 🔄 Complete Workflow

**Use case: You have local MP4 files and want to find YouTube sources to re-download in better quality**

```bash
# 1. Search for matching YouTube videos
python youtube_search.py D:/Videos/livres_audio youtube_links.txt

# 2. Download MP3 from YouTube (better quality)
python download_mp3.py youtube_links_links_only.txt D:/Music/audiobooks

# 3. (Optional) Convert other local MP4 files
python audio_converter.py D:/Videos/autres -o D:/Music/converted
```

**Use case: Simple batch conversion**

```bash
# Convert all your MP4 files to 320kbps MP3
python audio_converter.py D:/Downloads/videos
```

---

## ⚙️ Advanced Configuration

### Parallelization

By default, `audio_converter.py` uses **50 workers** in parallel.

**Modify in code:**
```python
# audio_converter.py, line 19
MAX_WORKERS = 20  # Reduce for less powerful machines
```

**Or disable:**
```bash
python audio_converter.py /videos --sequential
```

### Audio Quality

**Recommended bitrates:**
- `128k` : Acceptable quality, lightweight files
- `192k` : Good quality
- `256k` : Very good quality
- `320k` : Maximum MP3 quality (default)

**Common sample rates:**
- `44100` : CD standard (default)
- `48000` : Professional standard
- `96000` : Hi-Res audio (large files)

### YouTube Rate Limiting

`youtube_search.py` includes a **1 second** pause between requests to avoid blocking.

**Modify in code:**
```python
# youtube_search.py, line 134
time.sleep(1)  # Increase if necessary
```

---

## 🐛 Troubleshooting

### Error: "FFmpeg is not installed"
**Solution:** Install FFmpeg (see [Prerequisites](#-prerequisites))

### Error: "yt-dlp is not installed"
**Solution:**
```bash
pip install yt-dlp
```

### Error: "Cannot read property of undefined" or weird characters
**Solution:** The script already handles UTF-8, but on Windows:
```bash
chcp 65001  # Enable UTF-8 in PowerShell
python download_mp3.py ...
```

### YouTube download fails (429 Too Many Requests)
**Solution:** Wait a few minutes, then restart with the `failed_downloads.txt` file

### Conversion very slow
**Solution:** 
- Verify that parallel mode is active (no `--sequential`)
- Reduce `MAX_WORKERS` if CPU is overloaded
- Check available disk space

---

## 🤝 Contributing

Contributions are welcome! 

**Process:**
1. Fork the project
2. Create a branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

**Guidelines:**
- Python 3.8+ code with type hints
- Docstrings for all public functions
- Unit tests for new features
- Follow PEP 8 (formatting with `black`)

---

## 📄 License

Distributed under **MIT** license. See [LICENSE](LICENSE) for more information.

---

## 👨‍💻 Author

**[A. DERA](https://github.com/a-dera)**

---

## 🙏 Acknowledgments

- [FFmpeg](https://ffmpeg.org/) - The Swiss Army knife of multimedia
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Enhanced fork of youtube-dl
- Python open-source community

---

## 📊 Statistics

![GitHub stars](https://img.shields.io/github/stars/a-dera/audio_converter?style=social)
![GitHub forks](https://img.shields.io/github/forks/a-dera/audio_converter?style=social)
![GitHub issues](https://img.shields.io/github/issues/a-dera/audio_converter)

---

**⭐ If this project helps you, feel free to give it a star!**
