# 💡 Audio Converter - Code Examples & Use Cases

## Table of Contents

- [Getting Started](#getting-started)
- [MP4 to MP3 Conversion Examples](#mp4-to-mp3-conversion-examples)
- [YouTube Search Examples](#youtube-search-examples)
- [YouTube Download Examples](#youtube-download-examples)
- [Complete Workflows](#complete-workflows)
- [Advanced Usage](#advanced-usage)
- [Integration Examples](#integration-examples)
- [Troubleshooting Examples](#troubleshooting-examples)

---

## Getting Started

### Basic Setup

```bash
# Clone the repository
git clone https://github.com/a-dera/audio_converter.git
cd audio_converter

# Install Python dependencies
pip install -r requirements.txt

# Verify FFmpeg installation
ffmpeg -version

# Test basic conversion
python audio_converter.py examples/ -o test_output/
```

### Directory Structure Example

```
my_project/
├── videos/
│   ├── lecture1.mp4
│   ├── lecture2.mp4
│   └── lecture3.mp4
├── music/
│   └── (output folder)
└── audio_converter/
    ├── audio_converter.py
    ├── youtube_search.py
    └── download_mp3.py
```

---

## MP4 to MP3 Conversion Examples

### Example 1: Basic Conversion

**Scenario**: Convert all MP4 files in a folder using default settings (320kbps, 44100Hz).

```bash
python audio_converter.py D:/Videos/lectures
```

**Expected Output:**
```
==================================================
🎬 MP4 to MP3 Converter - High Quality
==================================================
✅ FFmpeg detected

📂 Source folder: D:\Videos\lectures
📁 Output folder: D:\Videos\lectures\mp3_output
🎵 Files to convert: 3
🎚️  Quality: 320k @ 44100Hz
⚡ Parallel mode
--------------------------------------------------
✅ lecture1.mp4 → lecture1.mp3
✅ lecture2.mp4 → lecture2.mp3
✅ lecture3.mp4 → lecture3.mp3

==================================================
📊 SUMMARY
==================================================
   Total:     3 file(s)
   Succeeded: 3 ✅
   Failed:    0 ❌

✨ Conversion completed successfully!
```

**Result:**
```
lectures/
├── lecture1.mp4
├── lecture2.mp4
├── lecture3.mp4
└── mp3_output/
    ├── lecture1.mp3  (320kbps, 44100Hz)
    ├── lecture2.mp3
    └── lecture3.mp3
```

---

### Example 2: Custom Output Folder

**Scenario**: Convert videos and save MP3 files to a different location.

```bash
python audio_converter.py D:/Videos/lectures -o D:/Music/podcasts
```

**Result:**
```
D:/Music/podcasts/
├── lecture1.mp3
├── lecture2.mp3
└── lecture3.mp3
```

**Python Script Equivalent:**
```python
from pathlib import Path
from audio_converter import convert_batch

result = convert_batch(
    input_folder="D:/Videos/lectures",
    output_folder="D:/Music/podcasts"
)

print(f"Converted {result['success']} files")
```

---

### Example 3: Lower Quality for Mobile

**Scenario**: Convert to 128kbps MP3 for mobile devices (smaller file size).

```bash
python audio_converter.py D:/Videos -o D:/Mobile/music -b 128k
```

**File Size Comparison:**
```
Original MP4:    25 MB
MP3 (320kbps):   7.5 MB
MP3 (128kbps):   3.0 MB  ← Mobile-friendly
```

---

### Example 4: Hi-Res Audio (48kHz)

**Scenario**: Convert to 48kHz sample rate for professional audio work.

```bash
python audio_converter.py D:/Videos/studio -b 320k -r 48000
```

**Quality Settings:**
- **CD Quality**: 44100 Hz (default)
- **Professional**: 48000 Hz
- **Hi-Res**: 96000 Hz (large files)

---

### Example 5: Sequential Processing

**Scenario**: Disable parallel processing for resource-constrained systems.

```bash
python audio_converter.py D:/Videos --sequential
```

**Use Cases:**
- Low-end CPU (2 cores or less)
- Limited RAM
- Background processing
- Debugging issues

---

### Example 6: Batch Script (Windows)

**Scenario**: Convert multiple folders automatically.

**`convert_all.bat`:**
```batch
@echo off
echo Converting lecture folders...

python audio_converter.py "D:/Videos/Week1" -o "D:/Music/Week1"
python audio_converter.py "D:/Videos/Week2" -o "D:/Music/Week2"
python audio_converter.py "D:/Videos/Week3" -o "D:/Music/Week3"

echo All conversions complete!
pause
```

---

### Example 7: Python Integration

**Scenario**: Integrate conversion into a larger Python application.

```python
import sys
from pathlib import Path
from audio_converter import check_ffmpeg, convert_batch

def process_video_archive(archive_path: str):
    """Process an entire video archive."""
    
    # Validate FFmpeg
    try:
        check_ffmpeg()
    except SystemExit:
        print("Please install FFmpeg first")
        return False
    
    # Convert each subdirectory
    archive = Path(archive_path)
    for subfolder in archive.iterdir():
        if subfolder.is_dir():
            print(f"\n📂 Processing {subfolder.name}...")
            
            output = archive / "converted" / subfolder.name
            result = convert_batch(
                input_folder=str(subfolder),
                output_folder=str(output),
                bitrate="256k",
                parallel=True
            )
            
            print(f"✅ {result['success']}/{result['total']} files converted")
    
    return True

# Usage
if __name__ == "__main__":
    process_video_archive("D:/VideoArchive")
```

---

## YouTube Search Examples

### Example 8: Basic YouTube Search

**Scenario**: Find YouTube URLs for local MP4 files.

```bash
python youtube_search.py D:/Videos/audiobooks
```

**Input Files:**
```
audiobooks/
├── Le Petit Prince.mp4
├── Les Misérables - Tome 1.mp4
└── 1984 by George Orwell.mp4
```

**Output (`youtube_links.txt`):**
```txt
# Le Petit Prince.mp4
https://www.youtube.com/watch?v=abc123

# Les Misérables - Tome 1.mp4
https://www.youtube.com/watch?v=def456

# 1984 by George Orwell.mp4
https://www.youtube.com/watch?v=ghi789
```

**Output (`youtube_links_links_only.txt`):**
```txt
https://www.youtube.com/watch?v=abc123
https://www.youtube.com/watch?v=def456
https://www.youtube.com/watch?v=ghi789
```

---

### Example 9: Custom Output Filename

**Scenario**: Save search results to a specific file.

```bash
python youtube_search.py D:/Videos/music my_music_links.txt
```

**Result:**
- `my_music_links.txt` (full results)
- `my_music_links_links_only.txt` (URLs only)

---

### Example 10: Handling Special Characters

**Scenario**: Files with emojis, underscores, and special characters.

**Input Files:**
```
videos/
├── 🎵_Song_Name_-_Artist.mp4
├── [Official] Music Video (HD).mp4
└── Track__01___Intro.mp4
```

**Cleaned Queries:**
```
"Song Name Artist"
"Official Music Video HD"
"Track 01 Intro"
```

**Python Example:**
```python
from youtube_search import clean_filename_for_search

filenames = [
    "🎵_Song_Name_-_Artist.mp4",
    "[Official] Music Video (HD).mp4",
    "Track__01___Intro.mp4"
]

for filename in filenames:
    query = clean_filename_for_search(filename)
    print(f"{filename:40} → {query}")
```

**Output:**
```
🎵_Song_Name_-_Artist.mp4                → Song Name Artist
[Official] Music Video (HD).mp4         → Official Music Video HD
Track__01___Intro.mp4                   → Track 01 Intro
```

---

### Example 11: Failed Search Handling

**Scenario**: Some files don't match any YouTube videos.

**Input:**
```
videos/
├── Common Video.mp4          ✅ Found
├── Super Rare Video.mp4      ❌ Not found
└── Another Common Video.mp4  ✅ Found
```

**Output (`youtube_links.txt`):**
```txt
# Common Video.mp4
https://www.youtube.com/watch?v=abc123

# Super Rare Video.mp4 - NOT FOUND

# Another Common Video.mp4
https://www.youtube.com/watch?v=def456
```

**Output (`youtube_links_links_only.txt`):**
```txt
https://www.youtube.com/watch?v=abc123
https://www.youtube.com/watch?v=def456
```

**Console Output:**
```
============================================================
📊 SUMMARY
============================================================
   Total files:   3
   Links found:   2 ✅
   Not found:     1 ❌

✅ Complete file: youtube_links.txt
✅ Links only: youtube_links_links_only.txt
```

---

### Example 12: Rate Limiting Demonstration

**Scenario**: Processing many files with rate limiting.

```python
import time
from pathlib import Path
from youtube_search import clean_filename_for_search, search_youtube

def search_with_rate_limit(files: list[Path], delay: float = 1.0):
    """Search YouTube with custom rate limiting."""
    results = []
    
    for i, file in enumerate(files, 1):
        print(f"[{i}/{len(files)}] Searching: {file.name}")
        
        query = clean_filename_for_search(file.name)
        url = search_youtube(query)
        
        if url:
            results.append((file.name, url))
            print(f"    ✅ Found")
        else:
            print(f"    ❌ Not found")
        
        # Rate limiting (avoid YouTube throttling)
        if i < len(files):
            time.sleep(delay)
    
    return results

# Usage
files = list(Path("D:/Videos").glob("*.mp4"))
results = search_with_rate_limit(files, delay=1.5)  # 1.5 seconds between requests
```

---

## YouTube Download Examples

### Example 13: Basic Download

**Scenario**: Download MP3 from a list of YouTube URLs.

**`links.txt`:**
```txt
https://www.youtube.com/watch?v=abc123
https://www.youtube.com/watch?v=def456
https://www.youtube.com/watch?v=ghi789
```

**Command:**
```bash
python download_mp3.py links.txt
```

**Result:**
```
mp3_downloads/
├── Video Title 1.mp3
├── Video Title 2.mp3
└── Video Title 3.mp3
```

---

### Example 14: Custom Output Folder

**Scenario**: Download to a specific directory.

```bash
python download_mp3.py youtube_links.txt D:/Music/youtube_audio
```

**Result:**
```
D:/Music/youtube_audio/
├── Song Name 1.mp3
├── Song Name 2.mp3
└── Song Name 3.mp3
```

---

### Example 15: Link File with Comments

**Scenario**: Organize links with comments and categories.

**`organized_links.txt`:**
```txt
# ============================================
# Classical Music
# ============================================
https://www.youtube.com/watch?v=classical1
https://www.youtube.com/watch?v=classical2

# ============================================
# Jazz Music
# ============================================
https://www.youtube.com/watch?v=jazz1
https://www.youtube.com/watch?v=jazz2

# This link is broken - skip
# https://www.youtube.com/watch?v=broken

# ============================================
# Rock Music
# ============================================
https://www.youtube.com/watch?v=rock1
```

**Command:**
```bash
python download_mp3.py organized_links.txt D:/Music/genres
```

**Notes:**
- Comments (lines starting with `#`) are ignored
- Only lines containing `youtube.com/watch` or `youtu.be/` are processed
- Blank lines are skipped

---

### Example 16: Handling Failed Downloads

**Scenario**: Some downloads fail due to unavailable videos.

**Input (`links.txt`):**
```txt
https://www.youtube.com/watch?v=valid1
https://www.youtube.com/watch?v=deleted_video
https://www.youtube.com/watch?v=valid2
https://www.youtube.com/watch?v=private_video
https://www.youtube.com/watch?v=valid3
```

**Console Output:**
```
[1/5] ⬇️  Downloading...
    URL: https://www.youtube.com/watch?v=valid1
    ✅ Success!

[2/5] ⬇️  Downloading...
    URL: https://www.youtube.com/watch?v=deleted_video
    ❌ Failed: ERROR: Video unavailable

[3/5] ⬇️  Downloading...
    URL: https://www.youtube.com/watch?v=valid2
    ✅ Success!

...

============================================================
📊 SUMMARY
============================================================
   Total:     5
   Succeeded: 3 ✅
   Failed:    2 ❌

💾 Failed links saved in: failed_downloads.txt
```

**`failed_downloads.txt`:**
```txt
https://www.youtube.com/watch?v=deleted_video
https://www.youtube.com/watch?v=private_video
```

**Retry Failed Downloads:**
```bash
# Retry only failed links
python download_mp3.py failed_downloads.txt D:/Music/retry
```

---

### Example 17: Batch Download Script

**Scenario**: Download multiple playlists to separate folders.

**`download_all.sh` (Linux/macOS):**
```bash
#!/bin/bash

# Playlist 1
python download_mp3.py playlist1_links.txt ~/Music/Playlist1

# Playlist 2
python download_mp3.py playlist2_links.txt ~/Music/Playlist2

# Playlist 3
python download_mp3.py playlist3_links.txt ~/Music/Playlist3

echo "All downloads complete!"
```

**`download_all.bat` (Windows):**
```batch
@echo off

python download_mp3.py playlist1_links.txt "D:/Music/Playlist1"
python download_mp3.py playlist2_links.txt "D:/Music/Playlist2"
python download_mp3.py playlist3_links.txt "D:/Music/Playlist3"

echo All downloads complete!
pause
```

---

## Complete Workflows

### Example 18: Full Workflow - Local to YouTube

**Scenario**: You have local MP4 files, want to find YouTube sources, and download better quality.

**Step 1: Search YouTube**
```bash
python youtube_search.py D:/Videos/audiobooks audiobook_links.txt
```

**Step 2: Review Results**
```bash
# Open audiobook_links.txt to verify results
notepad audiobook_links.txt  # Windows
cat audiobook_links.txt      # Linux/macOS
```

**Step 3: Download MP3 from YouTube**
```bash
python download_mp3.py audiobook_links_links_only.txt D:/Music/audiobooks_yt
```

**Step 4: Convert Remaining Local Files**
```bash
# For files not found on YouTube, convert local copies
python audio_converter.py D:/Videos/audiobooks -o D:/Music/audiobooks_local
```

**Final Structure:**
```
D:/Music/
├── audiobooks_yt/      (YouTube downloads - best quality)
│   ├── Book1.mp3
│   └── Book2.mp3
└── audiobooks_local/   (Local conversions)
    └── Book3.mp3       (not found on YouTube)
```

---

### Example 19: Podcast Archive Workflow

**Scenario**: Archive podcast videos as MP3 files.

**`archive_podcasts.py`:**
```python
#!/usr/bin/env python3
"""
Podcast archiving workflow:
1. Find YouTube URLs from local MP4 files
2. Download best quality from YouTube
3. Convert remaining local files
"""

import subprocess
from pathlib import Path

def archive_podcasts(local_folder: str, output_folder: str):
    """Complete podcast archiving workflow."""
    
    local_path = Path(local_folder)
    output_path = Path(output_folder)
    
    # Create output directories
    yt_folder = output_path / "youtube"
    local_mp3_folder = output_path / "local"
    yt_folder.mkdir(parents=True, exist_ok=True)
    local_mp3_folder.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("📻 Podcast Archiving Workflow")
    print("=" * 60)
    
    # Step 1: Search YouTube
    print("\n🔍 Step 1: Searching YouTube...")
    subprocess.run([
        "python", "youtube_search.py",
        str(local_path),
        "podcast_links.txt"
    ])
    
    # Step 2: Download from YouTube
    print("\n⬇️  Step 2: Downloading from YouTube...")
    subprocess.run([
        "python", "download_mp3.py",
        "podcast_links_links_only.txt",
        str(yt_folder)
    ])
    
    # Step 3: Convert local files
    print("\n🎬 Step 3: Converting local MP4 files...")
    subprocess.run([
        "python", "audio_converter.py",
        str(local_path),
        "-o", str(local_mp3_folder)
    ])
    
    print("\n" + "=" * 60)
    print("✨ Archiving complete!")
    print(f"📁 YouTube MP3: {yt_folder}")
    print(f"📁 Local MP3:   {local_mp3_folder}")
    print("=" * 60)

# Usage
if __name__ == "__main__":
    archive_podcasts(
        local_folder="D:/Videos/podcasts",
        output_folder="D:/Music/podcast_archive"
    )
```

**Run:**
```bash
python archive_podcasts.py
```

---

### Example 20: Music Collection Migration

**Scenario**: Migrate music collection from MP4 to MP3 format.

**`migrate_music.sh`:**
```bash
#!/bin/bash

INPUT_DIR="$HOME/Videos/MusicVideos"
OUTPUT_DIR="$HOME/Music/Converted"

echo "🎵 Music Collection Migration"
echo "=============================="
echo "Input:  $INPUT_DIR"
echo "Output: $OUTPUT_DIR"
echo ""

# Count files
file_count=$(find "$INPUT_DIR" -name "*.mp4" | wc -l)
echo "Found $file_count MP4 files"
echo ""

# Convert with high quality settings
python audio_converter.py "$INPUT_DIR" \
    -o "$OUTPUT_DIR" \
    -b 320k \
    -r 48000

echo ""
echo "✅ Migration complete!"
echo "MP3 files saved to: $OUTPUT_DIR"
```

---

## Advanced Usage

### Example 21: Quality Comparison Script

**Scenario**: Compare output quality at different bitrates.

**`compare_quality.py`:**
```python
#!/usr/bin/env python3
"""Compare MP3 quality at different bitrates."""

import subprocess
from pathlib import Path

def compare_bitrates(input_file: str):
    """Convert same file at different bitrates for comparison."""
    
    input_path = Path(input_file)
    output_base = Path("quality_comparison")
    output_base.mkdir(exist_ok=True)
    
    bitrates = ["128k", "192k", "256k", "320k"]
    
    print("🎚️  Quality Comparison")
    print("=" * 60)
    print(f"Input: {input_path.name}")
    print("")
    
    for bitrate in bitrates:
        output_file = output_base / f"{input_path.stem}_{bitrate}.mp3"
        
        print(f"Converting at {bitrate}...")
        
        cmd = [
            "ffmpeg",
            "-i", str(input_path),
            "-vn",
            "-acodec", "libmp3lame",
            "-ab", bitrate,
            "-y",
            str(output_file)
        ]
        
        subprocess.run(cmd, capture_output=True)
        
        # Get file size
        size_mb = output_file.stat().st_size / (1024 * 1024)
        print(f"    {bitrate}: {size_mb:.2f} MB")
    
    print("")
    print("✅ Comparison files created in: quality_comparison/")
    print("Listen to each file to compare quality vs file size")

# Usage
if __name__ == "__main__":
    compare_bitrates("sample_video.mp4")
```

**Output:**
```
🎚️  Quality Comparison
============================================================
Input: sample_video.mp4

Converting at 128k...
    128k: 3.2 MB
Converting at 192k...
    192k: 4.8 MB
Converting at 256k...
    256k: 6.4 MB
Converting at 320k...
    320k: 8.0 MB

✅ Comparison files created in: quality_comparison/
```

---

### Example 22: Parallel Processing Benchmark

**Scenario**: Measure performance improvement with parallel processing.

**`benchmark.py`:**
```python
#!/usr/bin/env python3
"""Benchmark parallel vs sequential conversion."""

import time
from pathlib import Path
from audio_converter import convert_batch

def benchmark(folder: str):
    """Compare parallel vs sequential processing times."""
    
    print("⚡ Performance Benchmark")
    print("=" * 60)
    
    # Parallel processing
    print("\n🔄 Parallel mode (50 workers)...")
    start = time.time()
    result_parallel = convert_batch(
        input_folder=folder,
        output_folder=f"{folder}/benchmark_parallel",
        parallel=True
    )
    parallel_time = time.time() - start
    
    # Sequential processing
    print("\n🐌 Sequential mode...")
    start = time.time()
    result_sequential = convert_batch(
        input_folder=folder,
        output_folder=f"{folder}/benchmark_sequential",
        parallel=False
    )
    sequential_time = time.time() - start
    
    # Results
    print("\n" + "=" * 60)
    print("📊 Results")
    print("=" * 60)
    print(f"Files processed: {result_parallel['total']}")
    print(f"Parallel time:   {parallel_time:.2f}s")
    print(f"Sequential time: {sequential_time:.2f}s")
    print(f"Speedup:         {sequential_time / parallel_time:.2f}x")
    print("=" * 60)

# Usage
if __name__ == "__main__":
    benchmark("D:/Videos/test_batch")
```

---

### Example 23: Custom Metadata Extraction

**Scenario**: Extract and preserve video metadata during conversion.

**`convert_with_metadata.py`:**
```python
#!/usr/bin/env python3
"""Convert MP4 to MP3 while preserving metadata."""

import subprocess
import json
from pathlib import Path

def extract_metadata(video_file: Path) -> dict:
    """Extract metadata from video using ffprobe."""
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        str(video_file)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return data.get("format", {}).get("tags", {})

def convert_with_metadata(input_file: Path, output_folder: Path):
    """Convert MP4 to MP3 and preserve metadata tags."""
    
    # Extract metadata
    metadata = extract_metadata(input_file)
    
    output_file = output_folder / f"{input_file.stem}.mp3"
    
    # Build FFmpeg command with metadata
    cmd = [
        "ffmpeg",
        "-i", str(input_file),
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "320k",
    ]
    
    # Add metadata tags
    if "title" in metadata:
        cmd.extend(["-metadata", f"title={metadata['title']}"])
    if "artist" in metadata:
        cmd.extend(["-metadata", f"artist={metadata['artist']}"])
    if "album" in metadata:
        cmd.extend(["-metadata", f"album={metadata['album']}"])
    if "date" in metadata:
        cmd.extend(["-metadata", f"date={metadata['date']}"])
    
    cmd.extend(["-y", str(output_file)])
    
    # Execute conversion
    subprocess.run(cmd, capture_output=True)
    
    print(f"✅ {input_file.name} → {output_file.name}")
    if metadata:
        print(f"    Metadata: {', '.join(metadata.keys())}")

# Usage
if __name__ == "__main__":
    input_folder = Path("D:/Videos")
    output_folder = Path("D:/Music")
    output_folder.mkdir(exist_ok=True)
    
    for video in input_folder.glob("*.mp4"):
        convert_with_metadata(video, output_folder)
```

---

## Integration Examples

### Example 24: Flask Web API

**Scenario**: Create a web API for on-demand conversion.

**`web_api.py`:**
```python
from flask import Flask, request, jsonify, send_file
from pathlib import Path
import tempfile
from audio_converter import convert_mp4_to_mp3

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_endpoint():
    """API endpoint for MP4 to MP3 conversion."""
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if not file.filename.endswith('.mp4'):
        return jsonify({'error': 'Only MP4 files allowed'}), 400
    
    # Save uploaded file
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        input_file = tmp_path / file.filename
        output_folder = tmp_path / "output"
        output_folder.mkdir()
        
        file.save(input_file)
        
        # Convert
        success, filename, message = convert_mp4_to_mp3(
            input_file,
            output_folder
        )
        
        if success:
            output_file = output_folder / f"{input_file.stem}.mp3"
            return send_file(
                output_file,
                as_attachment=True,
                download_name=output_file.name
            )
        else:
            return jsonify({'error': message}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Usage:**
```bash
# Start server
python web_api.py

# Upload and convert
curl -X POST -F "file=@video.mp4" http://localhost:5000/convert -o output.mp3
```

---

### Example 25: Discord Bot Integration

**Scenario**: Discord bot that converts YouTube links to MP3.

**`discord_bot.py`:**
```python
import discord
from discord.ext import commands
from download_mp3 import download_mp3
from pathlib import Path
import tempfile

bot = commands.Bot(command_prefix='!')

@bot.command()
async def convert(ctx, url: str):
    """Convert YouTube video to MP3.
    
    Usage: !convert https://www.youtube.com/watch?v=xxxxx
    """
    
    if 'youtube.com' not in url and 'youtu.be' not in url:
        await ctx.send("❌ Please provide a valid YouTube URL")
        return
    
    await ctx.send("⬇️  Downloading and converting...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Download
        success, message = download_mp3(url, tmp_path)
        
        if success:
            # Find the downloaded file
            mp3_files = list(tmp_path.glob("*.mp3"))
            if mp3_files:
                mp3_file = mp3_files[0]
                
                # Check file size (Discord limit: 8MB)
                size_mb = mp3_file.stat().st_size / (1024 * 1024)
                
                if size_mb <= 8:
                    await ctx.send("✅ Conversion complete!", file=discord.File(mp3_file))
                else:
                    await ctx.send(f"❌ File too large ({size_mb:.1f} MB). Discord limit is 8MB.")
            else:
                await ctx.send("❌ Conversion failed: No output file")
        else:
            await ctx.send(f"❌ Download failed: {message}")

bot.run('YOUR_BOT_TOKEN')
```

---

## Troubleshooting Examples

### Example 26: Verify FFmpeg Installation

```python
#!/usr/bin/env python3
"""Verify FFmpeg installation and capabilities."""

import shutil
import subprocess

def verify_ffmpeg():
    """Check FFmpeg installation and supported codecs."""
    
    print("🔍 FFmpeg Installation Check")
    print("=" * 60)
    
    # Check if FFmpeg is in PATH
    ffmpeg_path = shutil.which("ffmpeg")
    
    if ffmpeg_path:
        print(f"✅ FFmpeg found: {ffmpeg_path}")
    else:
        print("❌ FFmpeg not found in PATH")
        return False
    
    # Get version
    result = subprocess.run(
        ["ffmpeg", "-version"],
        capture_output=True,
        text=True
    )
    
    version_line = result.stdout.split('\n')[0]
    print(f"📌 {version_line}")
    
    # Check MP3 codec
    result = subprocess.run(
        ["ffmpeg", "-codecs"],
        capture_output=True,
        text=True
    )
    
    if "libmp3lame" in result.stdout:
        print("✅ MP3 codec (libmp3lame) available")
    else:
        print("⚠️  MP3 codec (libmp3lame) not available")
    
    print("=" * 60)
    return True

if __name__ == "__main__":
    verify_ffmpeg()
```

---

### Example 27: Debug Failed Conversions

```python
#!/usr/bin/env python3
"""Debug conversion failures with detailed logging."""

import subprocess
from pathlib import Path

def debug_conversion(input_file: str):
    """Run conversion with verbose output for debugging."""
    
    input_path = Path(input_file)
    output_file = input_path.with_suffix('.mp3')
    
    print(f"🐛 Debugging conversion: {input_path.name}")
    print("=" * 60)
    
    cmd = [
        "ffmpeg",
        "-i", str(input_path),
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "320k",
        "-ar", "44100",
        "-ac", "2",
        "-y",
        str(output_file)
    ]
    
    print("Command:")
    print(" ".join(cmd))
    print("\nOutput:")
    print("-" * 60)
    
    # Run with real-time output
    result = subprocess.run(cmd, capture_output=False)
    
    print("-" * 60)
    
    if result.returncode == 0:
        print("\n✅ Conversion successful")
        print(f"Output: {output_file}")
    else:
        print(f"\n❌ Conversion failed (exit code: {result.returncode})")

# Usage
if __name__ == "__main__":
    debug_conversion("problematic_video.mp4")
```

---

### Example 28: UTF-8 Encoding Test

**Scenario**: Test Unicode filename handling.

```python
#!/usr/bin/env python3
"""Test UTF-8 filename handling."""

from pathlib import Path
from audio_converter import get_mp4_files, convert_mp4_to_mp3

def test_unicode_filenames():
    """Test conversion with various Unicode filenames."""
    
    test_cases = [
        "Regular File.mp4",
        "Français - Été.mp4",
        "日本語.mp4",
        "Русский язык.mp4",
        "Emoji 🎵 Test.mp4",
        "Mixed_中文_English.mp4"
    ]
    
    print("🌍 Unicode Filename Test")
    print("=" * 60)
    
    output_folder = Path("unicode_test_output")
    output_folder.mkdir(exist_ok=True)
    
    for filename in test_cases:
        print(f"\nTesting: {filename}")
        
        # Note: For this test, you would need actual files
        # This is示范 示范 the handling
        try:
            # Test filename encoding
            encoded = filename.encode('utf-8')
            decoded = encoded.decode('utf-8')
            
            if decoded == filename:
                print("    ✅ UTF-8 encoding OK")
            else:
                print("    ❌ Encoding mismatch")
        except Exception as e:
            print(f"    ❌ Error: {e}")

if __name__ == "__main__":
    test_unicode_filenames()
```

---

## Performance Tips

### Optimization Checklist

```python
"""
Performance Optimization Guide:

1. **Parallel Processing**
   - Use default parallel mode for batch conversions
   - Adjust MAX_WORKERS based on CPU cores
   - Disable for debugging or low-memory systems

2. **Bitrate Selection**
   - 128k: Mobile devices, podcasts
   - 192k: General use
   - 256k: High quality
   - 320k: Maximum quality (default)

3. **Sample Rate**
   - 44100 Hz: CD quality (default)
   - 48000 Hz: Professional audio
   - 96000 Hz: Only if source quality justifies it

4. **Disk I/O**
   - Use SSD for input/output when possible
   - Avoid network drives for intensive operations
   - Ensure sufficient free space

5. **Network**
   - Respect rate limits (1 sec between YouTube searches)
   - Use wired connection for large downloads
   - Consider local caching for repeated operations
"""
```

---

**Version**: 1.0.0  
**Last Updated**: December 2025  
**Author**: A. DERA  
**License**: MIT
