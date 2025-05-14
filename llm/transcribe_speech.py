from pydub import AudioSegment
import os
import codecs
import tempfile

# https://huggingface.co/gacky1601/whisper-small-taiwanese-asr-v2
from transformers import pipeline
pipe = pipeline(task="automatic-speech-recognition", model="gacky1601/whisper-small-taiwanese-asr-v2")

# https://github.com/openai/whisper
import whisper
model = whisper.load_model("large-v3")

audio_path = os.path.join(os.getcwd(), 'llm/data/audio')

print(audio_path)


def convert_m4a_to_mp3(m4a_filename):
    audio = AudioSegment.from_file(f'{audio_path}/{m4a_filename}.m4a')
    audio.export(f'{audio_path}/{m4a_filename}.mp3', format="mp3")

    # print(f'Converted m4a to mp3.')

convert_m4a_to_mp3('test')

def convert_mp3_to_wav(mp3_filename):
    audio = AudioSegment.from_mp3(f'{audio_path}/{mp3_filename}.mp3')
    audio.export(f'{audio_path}/{mp3_filename}.wav', format="wav")

    # print(f'Converted mp3 to wav.')

convert_mp3_to_wav('test')


def transcribe_speech(filepath):
    # output = pipe(os.path.join(audio_path, filepath))

    output = model.transcribe(os.path.join(audio_path, filepath), fp16=False)
    # print(output)
    with open(os.path.join(audio_path, "transcribe_speech.txt"), "w", encoding="utf-8") as f:
        f.write(output["text"])
    return output["text"]

transcribe_speech("test.m4a")


def split_and_transcribe_audio(file_path, segment_length_seconds=30):

    try:
        audio = AudioSegment.from_file(os.path.join(audio_path, file_path))
    except Exception as e:
        raise Exception(f"Error loading audio file: {e}")

    # Correct calculation of milliseconds
    segment_length_ms = segment_length_seconds * 1000
    transcripts = []

    with tempfile.TemporaryDirectory() as temp_dir:
        for i, segment in enumerate([audio[i:i+segment_length_ms] for i in range(0, len(audio), segment_length_ms)]):
            segment_file_path = os.path.join(temp_dir, f"segment_{i}.mp3")
            segment.export(segment_file_path, format="mp3")

            # transcript = transcribe_audio_with_whisper(segment_file_path)
            transcript = transcribe_speech(segment_file_path)
            # transcript = model.transcribe(segment_file_path, fp16=False)
            time_in_seconds = i * segment_length_seconds
            timestamp = f"[{time_in_seconds // 60:02d}:{time_in_seconds % 60:02d}]"
            transcripts.append(timestamp + " " + transcript)

    output_file_name = os.path.splitext(os.path.basename(file_path))[0] + '.txt'
    print(f"Writing transcripts to {output_file_name}")
    # Using UTF-8 encoding
    with codecs.open(output_file_name, 'w', encoding='utf-8') as f:
        f.write("\n".join(transcripts))

# split_and_transcribe_audio("test2.mp3")



# Set your OpenAI API key here
# openai.api_key = 'your_openai_api_key'

# def transcribe_audio_with_whisper(audio_file_path):
#     """
#     Transcribe an audio file using OpenAI's Whisper API.

#     Args:
#     - audio_file_path: Path to the audio file to transcribe.

#     Returns:
#     - The transcribed text as a string.
#     """
#     with open(audio_file_path, "rb") as audio_file:
#         # response = openai.Audio.transcribe('whisper-1', audio_file)
#         response = pipe(audio_file)
#         return response['data']['text']
#         with open(output_dir, "w", encoding="utf-8") as f:
#             f.write(result_text)
#         print(response)