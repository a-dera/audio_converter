j# 📚 Audio Converter - API Reference

## Table of Contents

- [audio_converter.py](#audio_converterpy)
- [youtube_search.py](#youtube_searchpy)
- [download_mp3.py](#download_mp3py)
- [Common Patterns](#common-patterns)
- [Type Definitions](#type-definitions)

---

## audio_converter.py

### Functions

#### `check_ffmpeg()`

Validates that FFmpeg is installed and accessible in the system PATH.

**Signature:**
```python
def check_ffmpeg() -> None
```

**Parameters:**
- None

**Returns:**
- None

**Raises:**
- `SystemExit`: If FFmpeg is not found (exit code 1)

**Example:**
```python
check_ffmpeg()
# Output: ✅ FFmpeg detected
```

**Implementation Details:**
- Uses `shutil.which("ffmpeg")` to locate binary
- Prints OS-specific installation instructions on failure
- Should be called before any conversion operations

---

#### `get_mp4_files()`

Discovers all MP4 files in the specified directory.

**Signature:**
```python
def get_mp4_files(input_folder: Path) -> list[Path]
```

**Parameters:**
- `input_folder` (Path): Directory to scan for MP4 files

**Returns:**
- `list[Path]`: List of Path objects for discovered MP4 files

**Example:**
```python
from pathlib import Path

folder = Path("D:/Videos")
files = get_mp4_files(folder)
print(f"Found {len(files)} MP4 files")

for file in files:
    print(f"  - {file.name}")
```

**Implementation Details:**
- Case-insensitive search (*.mp4 and *.MP4)
- Non-recursive (only scans specified directory)
- Returns empty list if no files found

---

#### `convert_mp4_to_mp3()`

Converts a single MP4 file to MP3 using FFmpeg.

**Signature:**
```python
def convert_mp4_to_mp3(
    input_file: Path,
    output_folder: Path,
    bitrate: str = DEFAULT_BITRATE,
    sample_rate: int = DEFAULT_SAMPLE_RATE
) -> tuple[bool, str, str]
```

**Parameters:**
- `input_file` (Path): Source MP4 file
- `output_folder` (Path): Destination directory for MP3 output
- `bitrate` (str, optional): Audio bitrate (default: "320k")
  - Valid values: "128k", "192k", "256k", "320k"
- `sample_rate` (int, optional): Sample rate in Hz (default: 44100)
  - Common values: 44100 (CD), 48000 (pro), 96000 (hi-res)

**Returns:**
- `tuple[bool, str, str]`:
  - `success` (bool): Whether conversion succeeded
  - `filename` (str): Name of input file
  - `message` (str): Success message or error details

**Example:**
```python
from pathlib import Path

input_file = Path("video.mp4")
output_folder = Path("./mp3_output")
output_folder.mkdir(exist_ok=True)

success, filename, message = convert_mp4_to_mp3(
    input_file, 
    output_folder,
    bitrate="256k",
    sample_rate=48000
)

if success:
    print(f"✅ {filename} {message}")
else:
    print(f"❌ {filename}: {message}")
```

**FFmpeg Command Generated:**
```bash
ffmpeg -i input.mp4 \
       -vn \                    # No video
       -acodec libmp3lame \     # MP3 codec
       -ab 320k \               # Bitrate
       -ar 44100 \              # Sample rate
       -ac 2 \                  # Stereo
       -q:a 0 \                 # Best VBR quality
       -y \                     # Overwrite
       output.mp3
```

**Error Handling:**
- Catches `subprocess.CalledProcessError` for FFmpeg failures
- Returns truncated error message (max 100 chars)
- Does not halt execution on failure

---

#### `convert_batch()`

Converts all MP4 files in a folder to MP3, with optional parallel processing.

**Signature:**
```python
def convert_batch(
    input_folder: str,
    output_folder: str = None,
    bitrate: str = DEFAULT_BITRATE,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    parallel: bool = True
) -> dict
```

**Parameters:**
- `input_folder` (str): Path to folder containing MP4 files
- `output_folder` (str, optional): Output directory (default: `{input_folder}/mp3_output`)
- `bitrate` (str, optional): Audio bitrate (default: "320k")
- `sample_rate` (int, optional): Sample rate (default: 44100)
- `parallel` (bool, optional): Enable parallel processing (default: True)

**Returns:**
- `dict`: Statistics dictionary with keys:
  - `total` (int): Total files processed
  - `success` (int): Successfully converted
  - `failed` (int): Failed conversions

**Example:**
```python
# Basic usage
result = convert_batch("D:/Videos")

# Custom configuration
result = convert_batch(
    input_folder="D:/Videos/audiobooks",
    output_folder="D:/Music/converted",
    bitrate="256k",
    sample_rate=48000,
    parallel=True
)

print(f"Converted {result['success']}/{result['total']} files")
print(f"Failed: {result['failed']}")
```

**Performance:**
- **Parallel mode** (default): Uses `ThreadPoolExecutor` with 50 workers
- **Sequential mode**: Processes files one at a time
- Parallel mode provides ~5x speedup on multi-core systems

**Output:**
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

### Constants

```python
DEFAULT_BITRATE = "320k"        # Maximum MP3 quality
DEFAULT_SAMPLE_RATE = 44100     # CD-quality sample rate
MAX_WORKERS = 50                # Parallel processing workers
```

---

## youtube_search.py

### Functions

#### `clean_filename_for_search()`

Sanitizes a filename for use as a YouTube search query.

**Signature:**
```python
def clean_filename_for_search(filename: str) -> str
```

**Parameters:**
- `filename` (str): Original filename (with or without extension)

**Returns:**
- `str`: Cleaned search query string

**Example:**
```python
# Example 1: Simple cleaning
filename = "My Song.mp4"
query = clean_filename_for_search(filename)
print(query)  # Output: "My Song"

# Example 2: Complex cleaning
filename = "🎵 Livre_audio - Le-Petit-Prince (2024).mp4"
query = clean_filename_for_search(filename)
print(query)  # Output: "Livre audio Le Petit Prince 2024"

# Example 3: Special characters
filename = "Song___[Official]__(HD).mp4"
query = clean_filename_for_search(filename)
print(query)  # Output: "Song Official HD"
```

**Transformation Pipeline:**
1. Remove file extension using `Path.stem`
2. Encode to ASCII (removes emojis: 🎵 → "")
3. Replace special chars with spaces: `_-()[]` → ` `
4. Normalize multiple spaces to single space
5. Trim leading/trailing whitespace

**Before/After Examples:**

| Input | Output |
|-------|--------|
| `"🎵 Audio Book.mp4"` | `"Audio Book"` |
| `"Song_-_Artist.mp4"` | `"Song Artist"` |
| `"Video   (HD) [2024].mp4"` | `"Video HD 2024"` |
| `"test___file.MP4"` | `"test file"` |

---

#### `search_youtube()`

Searches YouTube for a query and returns the first result's URL.

**Signature:**
```python
def search_youtube(query: str, max_results: int = 1) -> str | None
```

**Parameters:**
- `query` (str): Search query string
- `max_results` (int, optional): Maximum results to retrieve (default: 1)

**Returns:**
- `str | None`: YouTube watch URL or None if not found

**Example:**
```python
# Example 1: Basic search
url = search_youtube("Python tutorial")
if url:
    print(f"Found: {url}")
    # Output: Found: https://www.youtube.com/watch?v=abc123
else:
    print("Not found")

# Example 2: With error handling
query = "Rare obscure video that doesn't exist"
url = search_youtube(query)
print(url)  # Output: None

# Example 3: Multiple results (returns first)
url = search_youtube("Python", max_results=5)
# Still returns only first result URL
```

**Implementation Details:**
- Uses yt-dlp's `ytsearch` extractor
- Extracts video ID from first result
- Constructs standard watch URL format
- Returns None on any exception (network, API errors)

**Error Handling:**
```python
try:
    url = search_youtube("query")
except Exception as e:
    print(f"Search failed: {e}")
    # Not necessary - function handles internally
```

**Rate Limiting:**
- No built-in rate limiting in function
- Caller should implement delays between calls
- See `main()` for rate limiting example

---

#### `get_mp4_files()`

Discovers and sorts MP4 files in a directory.

**Signature:**
```python
def get_mp4_files(folder: Path) -> list[Path]
```

**Parameters:**
- `folder` (Path): Directory to scan

**Returns:**
- `list[Path]`: Sorted list of MP4 file paths

**Example:**
```python
from pathlib import Path

folder = Path("D:/Videos")
files = get_mp4_files(folder)

print(f"Found {len(files)} files:")
for file in files:
    print(f"  - {file.name}")
```

**Differences from audio_converter version:**
- Returns sorted list (alphabetically by filename)
- Otherwise identical implementation

---

#### `main()`

Main entry point for YouTube search workflow.

**Signature:**
```python
def main() -> None
```

**Parameters:**
- None (uses `sys.argv` for CLI arguments)

**CLI Usage:**
```bash
python youtube_search.py <folder> [output_file]
```

**Arguments:**
- `folder` (required): Path to directory containing MP4 files
- `output_file` (optional): Output filename (default: "youtube_links.txt")

**Example:**
```bash
# Basic usage
python youtube_search.py D:/Videos

# Custom output file
python youtube_search.py D:/Videos my_links.txt
```

**Output Files:**

1. **Main file** (`youtube_links.txt`):
```txt
# video1.mp4
https://www.youtube.com/watch?v=abc123

# video2.mp4
https://www.youtube.com/watch?v=def456

# video3.mp4 - NOT FOUND
```

2. **Links-only file** (`youtube_links_links_only.txt`):
```txt
https://www.youtube.com/watch?v=abc123
https://www.youtube.com/watch?v=def456
```

**Workflow:**
1. Parse command-line arguments
2. Validate input folder exists
3. Discover MP4 files
4. For each file:
   - Clean filename
   - Search YouTube
   - Write results to both files
   - Sleep 1 second (rate limiting)
5. Print summary statistics

**Console Output:**
```
============================================================
🔍 YouTube Search from MP4 file names
============================================================

📂 Folder: D:\Downloads\videos
🎵 Files found: 15
📄 Output file: youtube_links.txt
------------------------------------------------------------

[1/15] 🔎 Searching: video1.mp4...
    Query: video1...
    ✅ Found: https://www.youtube.com/watch?v=xxxxx

[2/15] 🔎 Searching: video2.mp4...
    Query: video2...
    ❌ Not found

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

---

## download_mp3.py

### Functions

#### `download_mp3()`

Downloads a YouTube video and extracts audio as MP3.

**Signature:**
```python
def download_mp3(url: str, output_folder: Path) -> tuple[bool, str]
```

**Parameters:**
- `url` (str): YouTube video URL
- `output_folder` (Path): Destination directory for MP3 file

**Returns:**
- `tuple[bool, str]`:
  - `success` (bool): Whether download succeeded
  - `message` (str): "OK" or error message (max 100 chars)

**Example:**
```python
from pathlib import Path

output_folder = Path("./downloads")
output_folder.mkdir(exist_ok=True)

# Example 1: Successful download
success, msg = download_mp3(
    "https://www.youtube.com/watch?v=abc123",
    output_folder
)
if success:
    print("✅ Download complete!")
else:
    print(f"❌ Failed: {msg}")

# Example 2: Invalid URL
success, msg = download_mp3(
    "https://invalid-url.com",
    output_folder
)
print(msg)  # Output: "ERROR: ..."
```

**yt-dlp Command:**
```bash
yt-dlp -f bestaudio \              # Best audio quality
       --extract-audio \           # Extract audio only
       --audio-format mp3 \        # MP3 output
       --audio-quality 0 \         # Best quality
       -o "%(title)s.%(ext)s" \   # Filename template
       --no-playlist \             # Single video only
       <URL>
```

**Output Filename:**
- Format: `{video_title}.mp3`
- Example: `"My Video Title.mp3"`
- Automatically sanitized by yt-dlp

**Error Cases:**

| Error | Message |
|-------|---------|
| yt-dlp not installed | `"yt-dlp non trouvé. Installe-le avec: pip install yt-dlp"` |
| Invalid URL | `"ERROR: ..."` (from yt-dlp stderr) |
| Network error | `"ERROR: Unable to download ..."` |
| Any other exception | Exception message string |

---

#### `read_links()`

Parses a text file containing YouTube URLs.

**Signature:**
```python
def read_links(file_path: str) -> list[str]
```

**Parameters:**
- `file_path` (str): Path to text file with YouTube URLs

**Returns:**
- `list[str]`: List of valid YouTube URLs

**Example:**
```python
# Input file (links.txt):
# # My YouTube Videos
# https://www.youtube.com/watch?v=abc123
# 
# https://www.youtube.com/watch?v=def456
# # Comment line
# https://youtu.be/ghi789

links = read_links("links.txt")
print(links)
# Output: [
#     'https://www.youtube.com/watch?v=abc123',
#     'https://www.youtube.com/watch?v=def456',
#     'https://youtu.be/ghi789'
# ]
```

**Parsing Rules:**
1. Skip empty lines
2. Skip lines starting with `#` (comments)
3. Only include lines containing:
   - `youtube.com/watch` OR
   - `youtu.be/`

**Supported URL Formats:**

| Format | Valid |
|--------|-------|
| `https://www.youtube.com/watch?v=abc123` | ✅ |
| `https://youtu.be/abc123` | ✅ |
| `http://youtube.com/watch?v=abc123` | ✅ |
| `https://youtube.com/playlist?list=...` | ❌ (not matched) |
| `https://vimeo.com/123456` | ❌ (not matched) |

---

#### `main()`

Main entry point for YouTube download workflow.

**Signature:**
```python
def main() -> None
```

**Parameters:**
- None (uses `sys.argv` for CLI arguments)

**CLI Usage:**
```bash
python download_mp3.py <links_file> [output_folder]
```

**Arguments:**
- `links_file` (required): Path to text file with YouTube URLs
- `output_folder` (optional): Destination directory (default: "./mp3_downloads")

**Example:**
```bash
# Basic usage (output to ./mp3_downloads/)
python download_mp3.py youtube_links.txt

# Custom output folder
python download_mp3.py youtube_links.txt D:/Music/youtube
```

**Workflow:**
1. Parse command-line arguments
2. Validate links file exists
3. Create output folder (if doesn't exist)
4. Parse links from file
5. For each URL (sequential):
   - Download and convert to MP3
   - Print progress
   - Track success/failure
6. Save failed URLs to `failed_downloads.txt`
7. Print summary statistics

**Console Output:**
```
============================================================
🎵 YouTube Download → MP3
============================================================

📄 Source file: youtube_links.txt
📁 Output folder: D:\Downloads\mp3
🔗 Links to download: 10
------------------------------------------------------------

[1/10] ⬇️  Downloading...
    URL: https://www.youtube.com/watch?v=abc123
    ✅ Success!

[2/10] ⬇️  Downloading...
    URL: https://www.youtube.com/watch?v=def456
    ❌ Failed: ERROR: Video unavailable

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

**Output Files:**

1. **MP3 files**: `{output_folder}/{video_title}.mp3`
2. **Failed links** (if any): `failed_downloads.txt`

```txt
# failed_downloads.txt
https://www.youtube.com/watch?v=failed1
https://www.youtube.com/watch?v=failed2
```

**Error Handling:**
- Non-existent links file → Exit with error
- Empty links file → Exit with warning
- Individual download failures → Continue processing
- All downloads fail → Still creates summary

---

## Common Patterns

### Path Handling

All scripts use `pathlib.Path` for cross-platform compatibility:

```python
from pathlib import Path

# Creating paths
input_folder = Path("D:/Videos")
output_folder = Path(input_folder) / "mp3_output"

# Path operations
output_folder.mkdir(parents=True, exist_ok=True)
files = list(input_folder.glob("*.mp4"))

# String conversion
subprocess.run(["ffmpeg", "-i", str(input_file), str(output_file)])
```

### Error Handling

Consistent error handling across scripts:

```python
# System dependency check
if shutil.which("ffmpeg") is None:
    print("❌ Error message")
    sys.exit(1)

# File operations
try:
    result = subprocess.run(cmd, check=True, capture_output=True)
    return True, "Success"
except subprocess.CalledProcessError as e:
    error_msg = e.stderr[:100] if e.stderr else "Unknown error"
    return False, error_msg
```

### UTF-8 Encoding

All file I/O uses UTF-8 encoding:

```python
# Reading
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Writing
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Subprocess
subprocess.run(cmd, encoding='utf-8', errors='replace')
```

### Progress Reporting

Emoji-based console output:

```python
# Status indicators
print("✅ Success")
print("❌ Error")
print("⚠️  Warning")
print("📂 Folder")
print("🎵 Media")
print("⬇️  Downloading")
print("🔍 Searching")

# Progress counters
print(f"[{current}/{total}] Processing...")
```

---

## Type Definitions

### Custom Types

```python
from pathlib import Path
from typing import Literal

# Conversion result
ConversionResult = tuple[bool, str, str]
# (success, filename, message)

# Download result
DownloadResult = tuple[bool, str]
# (success, message)

# Statistics dictionary
Stats = dict[Literal["total", "success", "failed"], int]
```

### Function Signatures Summary

```python
# audio_converter.py
check_ffmpeg() -> None
get_mp4_files(Path) -> list[Path]
convert_mp4_to_mp3(Path, Path, str, int) -> tuple[bool, str, str]
convert_batch(str, str | None, str, int, bool) -> dict

# youtube_search.py
clean_filename_for_search(str) -> str
search_youtube(str, int) -> str | None
get_mp4_files(Path) -> list[Path]
main() -> None

# download_mp3.py
download_mp3(str, Path) -> tuple[bool, str]
read_links(str) -> list[str]
main() -> None
```

---

## Error Codes

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Dependency not found (FFmpeg, yt-dlp) |
| 1 | Invalid input folder/file |
| 1 | No files found to process |

### Usage

```bash
python audio_converter.py /path/to/videos
echo $?  # Check exit code
# 0 = success, 1 = error
```

---

## Version Compatibility

### Python Version Requirements

```python
# Minimum: Python 3.8
# Required features:
# - Type hints (PEP 484)
# - f-strings (PEP 498)
# - pathlib (stdlib)
# - Union types via | (3.10+, but using str | None)

# For Python < 3.10, use:
from typing import Optional, Union
def search_youtube(query: str) -> Optional[str]:
    ...
```

### Dependency Versions

```
yt-dlp>=2023.12.30  # Required for all YouTube operations
FFmpeg>=4.0         # System dependency
Python>=3.8         # Runtime requirement
```

---

**Version**: 1.0.0  
**Last Updated**: December 2025  
**Author**: A. DERA  
**License**: MIT
