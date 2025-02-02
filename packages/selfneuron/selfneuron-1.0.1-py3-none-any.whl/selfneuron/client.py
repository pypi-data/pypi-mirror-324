import json
from typing import Union
import requests
from http import HTTPStatus
from custom_exception import CustomException
from Logger import Logger

logger = Logger().get_logger()

class SelfNeuron:
    api_key = None
    base_url = None
    
    def __init__(self, base_url:str, api_key:str):
        self.base_url = base_url
        self.api_key = api_key

    def fetch_api_key(self):
        # This is the request to get the api key
        url = f"{self.base_url}/api-key/generate"
        # Add the token to the headers
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Connection": "keep-alive"
        }
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            self.api_key = response.json()['data']
            # print("API key is set successfully")

    def cleanup(self):
        try:
            url = f"{self.base_url}/api-key/revoke"
            headers = {
                "Authorization": f"Bearer {self.bearer_token}",
                "Connection": "keep-alive"
            }
            response = requests.get(url=url, headers=headers)
            if response.status_code == 200:
                print("API key revoked below is the response", response.json())
        except Exception as e:
             raise CustomException(e.__traceback__)

    def get_artifacts(self):
        if self.api_key is None:
            raise Exception("api key is not set")
        url = f"{self.base_url}/artifacts"
        headers = {
            "Connection": "keep-alive",
            "SELFNEURON-API-KEY": self.api_key
        }
        response = requests.get(url=url, headers=headers)
        if response.status_code == HTTPStatus.OK:
            data = response.json()['data']
            file_names = []
            for entry in data:
                file_names.append(entry.get('artifactFileName'))
            logger.info(response.json())
            return file_names

        elif response.status_code == HTTPStatus.UNAUTHORIZED:
            raise CustomException("Unauthorized. wrong api-key.")
        elif response.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
            raise CustomException("operation not permitted")

    def upload_artifact(self, artifact:str, keywords:Union[list, str]):
        url = f"{self.base_url}/artifacts/upload"
        headers = {
            "Connection": "keep-alive",
            "Content-Type": "multipart/form-data",
            "SELFNEURON-API-KEY": self.api_key,
        }
        if isinstance(keywords, str):
            keywords = [keywords]

        data = {
            "keywords": keywords
        }
        files = {"file": open(artifact, 'rb')}
        response = requests.post(url=url, headers=headers, data=data, files=files)
        if response.status_code == 200:
            logger.info(response.json())
        elif response.status_code == HTTPStatus.UNAUTHORIZED:
            raise CustomException("Unauthorized. wrong api-key.")
        elif response.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
            raise CustomException("operation not permitted")
    
    def get_keywords(self):
        url = f"{self.base_url}/keywords"
        headers = {
            "Connection": "keep-alive",
            # "Content-Type": "application/json",
            "SELFNEURON-API-KEY": self.api_key,
        }

        response = requests.get(url=url, headers=headers)
        if response.status_code == HTTPStatus.OK:
            data = response.json()['data']
        
        keywords = []
        for entry in data:
            if entry.get('isActive'):
                keywords.append(entry.get('keyword'))
        logger.info(f"keywords retrieved {keywords}")
        return keywords
    
    def get_userprofile(self):
        url = f"{self.base_url}/user/profile"
        headers = {
            "Connection": "keep-alive",
            # "Content-Type": "application/json",
            "SELFNEURON-API-KEY": self.api_key,
        }

        response = requests.get(url=url, headers=headers)
        if response.status_code == HTTPStatus.OK:
            return {'email':response.json().get('email'),
                    'name':response.json().get('name'),
                    'role':response.json().get('role'),
                    'device':response.json().get('device'),
                    'location':response.json().get('location')
            }

    def search(self, search_str:str):
        url = f"{self.base_url}/search"
        headers = {
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Accept":'application/json',
            "SELFNEURON-API-KEY": self.api_key,
        }
        
        data = json.dumps({
            "text": search_str,
            "ipAddress": "89.22.323.22",
            "location": {
                "latitude": 28,
                "longitude": 47
            },
            "device": "mac"
        }) 

        response = requests.post(url=url, headers=headers, data=data)
        data = response.json()['data']
        response_data = data['answers'][0]
        recommendations = data['recommendations']
        similar_content = data['similar_vectors']
        return response_data, recommendations, similar_content

    def get_recommendations(self):
        url = f"{self.base_url}/questions/recommendations"
        headers = {
            "Connection": "keep-alive",
            "SELFNEURON-API-KEY": self.api_key,
        }
        response = requests.get(url=url, headers=headers)
        if response.status_code == HTTPStatus.OK:
            data = response.json()['data']
            logger.info(f"recommended questions {data}")
            return data
        elif response.status_code == HTTPStatus.UNAUTHORIZED:
            raise CustomException("Unauthorized. wrong api-key.")
        elif response.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
            raise CustomException("operation not permitted")




