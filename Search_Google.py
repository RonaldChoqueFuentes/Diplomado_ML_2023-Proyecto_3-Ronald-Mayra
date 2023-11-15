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

class Search_Google:
    def __init__(self):
        
        # URL base de la API de Knowledge Graph
        self._url = "https://kgsearch.googleapis.com/v1/entities:search"
        
    def search(self, query):
        result = None
        api_key = os.environ.get('API_GOOGLE_KEY')
        
        # Parámetros de la consulta
        params = {
            "query": query,
            "key": api_key,
            "limit": 1,  # Puedes ajustar el límite según tus necesidades
            "languages": "es"
        }

        # Realizar la solicitud a la API
        response = requests.get(self._url, params=params)
        data = response.json()

        # Procesar la respuesta
        if "itemListElement" in data and len(data["itemListElement"]) > 0:
            result_info = data["itemListElement"][0]["result"]
            result = result_info["detailedDescription"]["articleBody"]
            print("Info: ", result)
        else:
            print("No se encontraron resultados para la consulta.")
        
        return result
    