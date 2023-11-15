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

class Safety_Service:
    def __init__(self):
        self._key = os.environ["CONTENT_SAFETY_KEY"]
        self._endpoint = os.environ["CONTENT_SAFETY_ENDPOINT"]
        
    
    def analyze_text(self, text_input: str):
        
        result = 0
        
        # Create a Content Safety client
        client = ContentSafetyClient(self._endpoint, AzureKeyCredential(self._key))

        # Contruct request
        request = AnalyzeTextOptions(text=text_input)

        # Analyze text
        try:
            response = client.analyze_text(request)
        except HttpResponseError as e:
            print("Analyze text failed.")
            if e.error:
                print(f"Error code: {e.error.code}")
                print(f"Error message: {e.error.message}")
                raise
            print(e)
            raise
        
        if response.hate_result:
            print(f"Hate severity: {response.hate_result.severity}")
            result = result + response.hate_result.severity
        if response.self_harm_result:
            print(f"SelfHarm severity: {response.self_harm_result.severity}")
            result = result + response.self_harm_result.severity
                
        if response.sexual_result:
            print(f"Sexual severity: {response.sexual_result.severity}")
            result = result + response.sexual_result.severity
                
        if response.violence_result:
            print(f"Violence severity: {response.violence_result.severity}")
            result = result + response.violence_result.severity
        
        return result
