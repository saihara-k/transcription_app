# -*- coding: utf-8 -*-
import io, os, datetime, time
import wave, pyaudio

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


class LiveTranscribe:

    def __init__(value):
        self.value = value
        pass

    def __call__():
        pass

    def function():
        pass

def main():
    live_transcribe = LiveTranscribe()
    live_transcribe()

if __name__ == "__main__":
    main()    

# インスタンス
client = speech.SpeechClient()

# 録音ファイル
speech_file = "sample.wav"

# 文字起こしファイル
d = datetime.datetime.today()
today = d.strftime("%Y%m%d-%H%M%S")
text_file = "{}.txt".format(today)

# バッファ用変数
buffer = []
BufferMode = False

# 基本情報の設定
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2 ** 11

# 録音に関する基本情報
iDeviceindex = 0
RECORD_SECONDS = 3

# 音声認識に渡すリクエストの基本情報
config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=RATE,
    language_code='ja-JP')


# コールバック関数
def callback(in_data, frame_count, time_info, status):
    if BufferMode:
        buffer.append(in_data)
    else:
        frames.append(in_data)
    return (None, pyaudio.paContinue)


# メイン関数
if __name__ == "__main__":
    print('Start Rec!')
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    input_device_index=iDeviceindex,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)

    # 録音開始(ずっとつけっぱ)
    stream.start_stream()
    pre_response = {}
    response = ""

    while True:
        try:
            frames = []
            BufferMode = False

            time.sleep(RECORD_SECONDS)

            BufferMode = True

            wf = wave.open(speech_file, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            if len(buffer) > 0:
                frames = buffer + frames
                buffer = []
            wf.writeframes(b''.join(frames))
            wf.close()

            # 録音したファイルを読み込む
            with io.open(speech_file, 'rb') as audio_file:
                content = audio_file.read()
                audio = types.RecognitionAudio(content=content)

            pre_response = response
            response = client.recognize(config, audio)
            if pre_response == response:
                break
            for result in response.results:
                print('Transcript: {}'.format(
                    result.alternatives[0].transcript))
                with open(text_file, 'a') as t:
                    print(result.alternatives[0].transcript, file=t)
        except KeyboardInterrupt:
            break

    print("Closing audio stream...")
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Finish Transcribing!")
