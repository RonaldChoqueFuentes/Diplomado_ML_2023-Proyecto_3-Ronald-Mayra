
from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speechsdk
import time
import json
import requests

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions

class Speech_Service:
    
    def  __init__(self):
        self._speech_config = self.get_speech_config()
        self._audio_config = self.get_audio_config()
    
    def get_speech_config(self):
        result = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION')) 
        return result

    def get_audio_config(self):
        result = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        return result
    
    def log_msg(self, msg):
        print(msg)
        
    def speech_to_text(self):
        result = None
        # https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=stt
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self._speech_config, language="es-BO")

        self.log_msg("Speak into your microphone.")
        speak_result = speech_recognizer.recognize_once()
        if speak_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            result = speak_result.text
            self.log_msg("recognise: {}".format(result))
        elif speak_result.reason == speechsdk.ResultReason.NoMatch:
            self.log_msg("No speech could be recognized: {}".format(speak_result.no_match_details))
        elif speak_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speak_result.cancellation_details
            self.log_msg("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                self.log_msg("Error details: {}".format(cancellation_details.error_details))
                self.log_msg("Did you set the speech resource key and region values?")

        return result
    
    def text_to_speech(self, text):
        result = False
        
        self._speech_config.speech_synthesis_voice_name='es-BO-MarceloNeural'
            
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self._speech_config, audio_config=self._audio_config)
    
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            self.log_msg("Speech to text: [{}]".format(text))
            result = True
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            self.log_msg("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    self.log_msg("Error details: {}".format(cancellation_details.error_details))
                    self.log_msg("Did you set the speech resource key and region values?")

        return result