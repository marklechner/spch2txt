from pydub import AudioSegment
import os

def convert_m4a_to_mp3(input_path, output_path):
    """
    Convert M4A file to MP3 format.
    
    Args:
        input_path (str): Path to input M4A file
        output_path (str): Path where MP3 file will be saved
    """
    try:
        # Load the M4A file
        audio = AudioSegment.from_file(input_path, format="m4a")
        
        # Export as MP3
        audio.export(output_path, format="mp3")
        print(f"Successfully converted {input_path} to {output_path}")
        
    except Exception as e:
        print(f"Error during conversion: {str(e)}")

def create_sample(input_path, output_path, duration_minutes=3):
    """
    Create a sample of specified duration from an MP3 file.
    
    Args:
        input_path (str): Path to input MP3 file
        output_path (str): Path where sample MP3 file will be saved
        duration_minutes (int): Duration of sample in minutes
    """
    try:
        # Load the MP3 file
        audio = AudioSegment.from_file(input_path, format="mp3")
        
        # Convert minutes to milliseconds
        duration_ms = duration_minutes * 60 * 1000
        
        # Take the first three minutes
        sample = audio[:duration_ms]
        
        # Export the sample
        sample.export(output_path, format="mp3")
        print(f"Successfully created {duration_minutes}-minute sample: {output_path}")
        
    except Exception as e:
        print(f"Error creating sample: {str(e)}")

if __name__ == "__main__":
    # File paths
    m4a_file = "hang.m4a"
    mp3_file = "hang.mp3"
    sample_file = "sample.mp3"
    
    # Convert M4A to MP3 if needed
    if not os.path.exists(mp3_file):
        if os.path.exists(m4a_file):
            convert_m4a_to_mp3(m4a_file, mp3_file)
        else:
            print(f"Error: Input file '{m4a_file}' not found!")
    
    # Create 3-minute sample if MP3 exists
    if os.path.exists(mp3_file):
        create_sample(mp3_file, sample_file, 3)
    else:
        print(f"Error: MP3 file '{mp3_file}' not found!")
