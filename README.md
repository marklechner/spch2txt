# Hungarian Speech-to-Text Transcriber

A Python-based Proof of Concept for transcribing Hungarian audio files using the Whisper model locally. This tool supports both long-form audio processing and sample creation, with options for chunked processing of larger files.

## Features

- Convert M4A files to MP3 format
- Create sample clips from longer audio files
- Local speech-to-text processing using Whisper
- Support for both timestamped and clean text output
- Chunked processing for handling large audio files
- Completely offline operation - no API keys needed

## Prerequisites

- Python 3.7+
- FFmpeg
- Sufficient disk space for Whisper model

## Configuration

Adjust these parameters in the script for different use cases:

- `model_size`: Choose from "tiny", "base", "small", "medium", "large-v2"
- `chunk_duration`: Duration in minutes for splitting large files
- `use_chunks`: Boolean to enable/disable chunked processing

## Performance Notes

- Recommended to use "medium" model for balance of speed and accuracy
- M1 Mac users can utilize MPS acceleration
- Large files can be processed either directly or in chunks based on available memory
