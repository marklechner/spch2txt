import argparse
import time
import os
from faster_whisper import WhisperModel
from pydub import AudioSegment
from transformers import MarianMTModel, MarianTokenizer
import torch

class AudioTranscriber:
    def __init__(self, model_size="medium", device="cpu", compute_type="int8"):
        print(f"Loading {model_size} model...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.translator = None
        self.tokenizer = None

    def load_translation_model(self, source_lang, target_lang="hu"):
        model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.translator = MarianMTModel.from_pretrained(model_name)

    def translate_text(self, text, source_lang, target_lang="hu"):
        if source_lang != target_lang:
            if self.translator is None or self.tokenizer is None:
                self.load_translation_model(source_lang, target_lang)
            inputs = self.tokenizer(text, return_tensors="pt", padding=True)
            translated = self.translator.generate(**inputs)
            translated_text = self.tokenizer.batch_decode(translated, skip_special_tokens=True)
            return translated_text[0]
        return text

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

    def transcribe_file(self, audio_path, output_prefix=None, source_lang="hu", target_lang="hu"):
        """Transcribe a single audio file"""
        if output_prefix is None:
            output_prefix = audio_path.rsplit('.', 1)[0]

        print(f"Transcribing: {audio_path}")
        segments, info = self.model.transcribe(
            audio_path,
            language=source_lang,
            beam_size=5,
            vad_filter=True
        )

        # Convert segments to list for multiple uses
        segments_list = list(segments)

        # Save timestamped version
        with open(f"{output_prefix}_timestamped.txt", 'w', encoding='utf-8') as f:
            for segment in segments_list:
                translated_text = self.translate_text(segment.text, source_lang, target_lang)
                f.write(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {translated_text}\n")

        # Save clean version
        with open(f"{output_prefix}_clean.txt", 'w', encoding='utf-8') as f:
            for segment in segments_list:
                translated_text = self.translate_text(segment.text, source_lang, target_lang)
                f.write(f"{translated_text}\n")

        return segments_list

    def process_large_file(self, input_file, chunk_duration=10, use_chunks=True, source_lang="hu", target_lang="hu"):
        """Process either in chunks or as a single file"""
        start_time = time.time()
        base_name = input_file.rsplit('.', 1)[0]

        if use_chunks:
            print("Splitting audio into chunks...")
            chunks = self.split_audio(input_file, chunk_duration)
            
            all_segments = []
            all_translated_segments = []
            for chunk in chunks:
                chunk_prefix = f"{base_name}_chunk_{chunks.index(chunk)}"
                segments = self.transcribe_file(chunk, output_prefix=chunk_prefix, source_lang=source_lang, target_lang=target_lang)
                all_segments.extend(segments)
                for segment in segments:
                    translated_text = self.translate_text(segment.text, source_lang, target_lang)
                    all_translated_segments.append((segment.start, segment.end, segment.text, translated_text))
                
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
            
            with open(f"{base_name}_translated_full.txt", 'w', encoding='utf-8') as f:
                for start, end, original_text, translated_text in all_translated_segments:
                    f.write(f"[{start:.2f}s -> {end:.2f}s] {translated_text}\n")
            
            with open(f"{base_name}_clean_translated_full.txt", 'w', encoding='utf-8') as f:
                for _, _, _, translated_text in all_translated_segments:
                    f.write(f"{translated_text}\n")
        else:
            # Process entire file at once
            self.transcribe_file(input_file, base_name, source_lang=source_lang, target_lang=target_lang)

        duration = time.time() - start_time
        print(f"\nTranscription completed in {duration:.2f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe and translate audio files.")
    parser.add_argument("input_file", help="Input audio file (MP3 format)")
    parser.add_argument("source_lang", help="Source language code")
    parser.add_argument("target_lang", help="Target language code")
    args = parser.parse_args()

    # Initialize transcriber
    transcriber = AudioTranscriber(model_size="medium")
    
    # Process the full audio file
    input_file = args.input_file
    source_lang = args.source_lang
    target_lang = args.target_lang
    
    # Choose whether to process in chunks or as a single file
    transcriber.process_large_file(
        input_file,
        chunk_duration=20,  # minutes per chunk
        use_chunks=True,    # Set to False to process as single file
        source_lang=source_lang,
        target_lang=target_lang
    )