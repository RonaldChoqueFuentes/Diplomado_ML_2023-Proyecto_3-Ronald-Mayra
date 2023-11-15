

from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import (
    TextAnalyticsClient,
    ExtractiveSummaryAction
) 

import pandas as pd
from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speechsdk
import time
import json
import requests

class Summarize_Text:
    
    def __init__(self):
        key = os.environ.get('LANGUAGE_KEY')
        endpoint = os.environ.get('LANGUAGE_ENDPOINT')

        self._client = self.authenticate_client(key, endpoint)
    
    def authenticate_client(self, key, endpoint):
        ta_credential = AzureKeyCredential(key)
        text_analytics_client = TextAnalyticsClient(
                endpoint=endpoint, 
                credential=ta_credential)
        return text_analytics_client
    
    
    def extract_summarization(self, documents):
        result = None
        
        document = documents

        poller = self._client.begin_analyze_actions(
            document,
            actions=[
                ExtractiveSummaryAction(max_sentence_count=1)
            ],
        )

        document_results = poller.result()
        
        for result in document_results:
            extract_summary_result = result[0]  # first document, first result
            if extract_summary_result.is_error:
                print("Error: '{}' - Mensaje: '{}'".format(
                    extract_summary_result.code, extract_summary_result.message
                ))
            else:
                result = " ".join([sentence.text for sentence in extract_summary_result.sentences])
                
                print("Resumen: \n{}".format(result))
        
        return result
    
    def entity_recognition(self, documents):
        result = None
        
        try:
            data = self._client.recognize_entities(documents = documents)[0]
            result = data.entities
            print("Named Entities: {0}".format(result))
            

        except Exception as err:
            print("Encountered exception. {}".format(err))
            
        if result:
            data = []
            result = " ".join([entity.text for entity in result])
                
        return result
        