# Universal Speech-to-Text Transcriber and Tranlsator

A Python-based Proof of Concept for transcribing any audio files using the Whisper model locally and translate it to any language. This tool supports both long-form audio processing and sample creation, with options for chunked processing of larger files.

## Features

- Convert M4A files to MP3 format
- Create sample clips from longer audio files
- Local speech-to-text processing using Whisper
- Local trnaslation of transcribed text to chosen language
- Support for both timestamped and clean text output
- Chunked processing for handling large audio files
- Completely offline operation - no API keys needed

## Prerequisites

- Python 3.10+
- FFmpeg
- Sufficient disk space for Whisper model

## Configuration

Adjust these parameters in the script for different use cases:

- `model_size`: Choose from "tiny", "base", "small", "medium", "large-v2"
- `chunk_duration`: Duration in minutes for splitting large files
- `use_chunks`: Boolean to enable/disable chunked processing

## Usage
To run the script, use the following command:

`python transcribe.py <input_file> <source_lang> <target_lang>`

* `<input_file>`: Path to the input audio file (MP3 format)
* `<source_lang>`: Source language code (e.g., "de" for German)
* `<target_lang>`: Target language code (e.g., "hu" for Hungarian)

Example:

`python transcribe.py test.mp3 de hu`

hu
This will transcribe the test.mp3 file from German (`de`) to Hungarian (`hu`).

## Performance Notes

- Recommended to use "medium" model for balance of speed and accuracy
- M1 Mac users can utilize MPS acceleration
- Large files can be processed either directly or in chunks based on available memory
