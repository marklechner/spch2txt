from faster_whisper import WhisperModel
from pydub import AudioSegment
import time
import os

class AudioTranscriber:
    def __init__(self, model_size="medium", device="cpu", compute_type="int8"):
        print(f"Loading {model_size} model...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        
    def split_audio(self, input_file, chunk_duration=10):
        """Split audio into chunks of specified minutes"""
        audio = AudioSegment.from_file(input_file)
        chunks = []
        
        # Convert duration to milliseconds
        chunk_length = chunk_duration * 60 * 1000
        
        # Split audio into chunks
        for i in range(0, len(audio), chunk_length):
            chunk = audio[i:i + chunk_length]
            chunk_path = f"temp_chunk_{i//chunk_length}.mp3"
            chunk.export(chunk_path, format="mp3")
            chunks.append(chunk_path)
            
        return chunks

    def transcribe_file(self, audio_path, output_prefix=None):
        """Transcribe a single audio file"""
        if output_prefix is None:
            output_prefix = audio_path.rsplit('.', 1)[0]

        print(f"Transcribing: {audio_path}")
        segments, info = self.model.transcribe(
            audio_path,
            language="hu",
            beam_size=5,
            vad_filter=True
        )

        # Convert segments to list for multiple uses
        segments_list = list(segments)

        # Save timestamped version
        with open(f"{output_prefix}_timestamped.txt", 'w', encoding='utf-8') as f:
            for segment in segments_list:
                f.write(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n")

        # Save clean version
        with open(f"{output_prefix}_clean.txt", 'w', encoding='utf-8') as f:
            for segment in segments_list:
                f.write(f"{segment.text}\n")

        return segments_list

    def process_large_file(self, input_file, chunk_duration=10, use_chunks=True):
        """Process either in chunks or as a single file"""
        start_time = time.time()
        base_name = input_file.rsplit('.', 1)[0]

        if use_chunks:
            print("Splitting audio into chunks...")
            chunks = self.split_audio(input_file, chunk_duration)
            
            all_segments = []
            for chunk in chunks:
                segments = self.transcribe_file(chunk)
                all_segments.extend(segments)
                
            # Clean up chunk files
            for chunk in chunks:
                os.remove(chunk)
                
            # Save combined results
            with open(f"{base_name}_timestamped_full.txt", 'w', encoding='utf-8') as f:
                for segment in all_segments:
                    f.write(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n")
                    
            with open(f"{base_name}_clean_full.txt", 'w', encoding='utf-8') as f:
                for segment in all_segments:
                    f.write(f"{segment.text}\n")
        else:
            # Process entire file at once
            self.transcribe_file(input_file, base_name)

        duration = time.time() - start_time
        print(f"\nTranscription completed in {duration:.2f} seconds")

if __name__ == "__main__":
    # Initialize transcriber
    transcriber = AudioTranscriber(model_size="medium")
    
    # Process the full audio file
    input_file = "hang.mp3"
    
    # Choose whether to process in chunks or as a single file
    transcriber.process_large_file(
        input_file,
        chunk_duration=10,  # minutes per chunk
        use_chunks=False     # Set to False to process as single file
    )   