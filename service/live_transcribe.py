# -*- coding: utf-8 -*-
import io
import os
import datetime
import time
import wave
import pyaudio

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from service.constant import *

class LiveTranscribe:

    def __init__(self):
        self.buffer = []
        self.frames = []
        self.buffer_mode = False
        self.response = ""

        d = datetime.datetime.today()
        today = d.strftime("%Y%m%d-%H%M")
        self.speech_file = "{}.wav".format(today)
        self.text_file = "{}.txt".format(today)

    def _fill_buffer(self, in_data, frame_count, time_info, status):
        if self.buffer_mode:
            self.buffer.append(in_data)
        else:
            self.frames.append(in_data)
        return (None, pyaudio.paContinue)

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=iDeviceindex,
            frames_per_buffer=CHUNK,
            stream_callback=self._fill_buffer
        )
        self._audio_stream.start_stream()
        self.wf = wave.open(self.speech_file, 'wb')
        self.wf.setnchannels(CHANNELS)
        self.wf.setsampwidth(self._audio_interface.get_sample_size(FORMAT))
        self.wf.setframerate(RATE)
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self._audio_interface.terminate()
        self.wf.close()

    def set_audio(self):
        time.sleep(RECORD_SECONDS)
        if len(self.buffer) > 0:
            self.frames = self.buffer + self.frames
            self.buffer = []
        self.wf.writeframes(b''.join(self.frames))
        self.buffer_mode = True
        audio = types.RecognitionAudio(content=b''.join(self.frames))
        self.frames = []
        return audio

    def response_to_text(self, response):
        if not response.results:
            return False
        for result in response.results:
            transcript = result.alternatives[0].transcript
            print('Transcript: {}'.format(transcript))
            with open(self.text_file, 'a') as t:
                print(transcript, file=t)
        self.buffer_mode = False
        return True


def main():
    client = speech.SpeechClient.from_service_account_json(CREDENTIAL_JSON)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code='ja-JP')

    live_transcribe = LiveTranscribe()
    print('Start Rec! ~Enter Ctrl + C to exit~')

    with live_transcribe as stream:
        flag_continue = True
        while flag_continue or IndefinitelyRec:
            try:
                audio = stream.set_audio()
                print('Now Recognizing...')
                response = client.recognize(config, audio)
                flag_continue = stream.response_to_text(response)
            except KeyboardInterrupt:
                break
    print("See you!")


if __name__ == "__main__":
    main()
