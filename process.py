import os
import argparse
from pydub import AudioSegment

def convert_m4a_to_mp3(m4a_path, mp3_path):
    """Convert M4A file to MP3 format."""
    audio = AudioSegment.from_file(m4a_path, format="m4a")
    audio.export(mp3_path, format="mp3")
    print(f"Converted {m4a_path} to {mp3_path}")

def create_sample(input_path, output_path, duration_minutes):
    """Create a sample of the specified duration from the input audio file."""
    try:
        audio = AudioSegment.from_file(input_path)
        sample = audio[:duration_minutes * 60 * 1000]  # duration in milliseconds
        
        # Export the sample
        sample.export(output_path, format="mp3")
        print(f"Successfully created {duration_minutes}-minute sample: {output_path}")
        
    except Exception as e:
        print(f"Error creating sample: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process audio files.")
    parser.add_argument("input_file", help="Input audio file (M4A format)")
    args = parser.parse_args()

    input_file = args.input_file
    base_name = os.path.splitext(input_file)[0]
    mp3_file = f"{base_name}.mp3"
    sample_file = f"{base_name}_sample.mp3"
    
    # Convert M4A to MP3 if needed
    if not os.path.exists(mp3_file):
        if os.path.exists(input_file):
            convert_m4a_to_mp3(input_file, mp3_file)
        else:
            print(f"Error: Input file '{input_file}' not found!")
    
    # Create 3-minute sample if MP3 exists
    if os.path.exists(mp3_file):
        create_sample(mp3_file, sample_file, 3)
    else:
        print(f"Error: MP3 file '{mp3_file}' not found!")
