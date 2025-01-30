import os
import requests 
import atexit

BASE_URL = "https://api.simplex.sh"
import json

class Simplex:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session_id = None
        atexit.register(self.cleanup_session)

    def cleanup_session(self):
        if self.session_id:
            try:
                self.close_session(self.session_id)
            except:
                pass

    def close_session(self):
        response = requests.post(
            f"{BASE_URL}/close",
            headers={
                'x-api-key': self.api_key
            },
            data={'session_id': self.session_id}
        )
        self.session_id = None
        return response.json()

    def create_session(self):
        response = requests.post(
            f"{BASE_URL}/create-session",
            headers={
                'x-api-key': self.api_key
            }
        )

        response_json = response.json()
        self.session_id = response_json['session_id']
        livestream_url = response_json['livestream_url']

        print(f"\nSession created successfully!")
        print(f"Session ID: {self.session_id}")
        print(f"Livestream URL: {livestream_url}\n")

        return self.session_id, livestream_url

    def goto(self, url: str, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action goto with url='{url}'")
        
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url

        data = {'url': url}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/goto",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        return response.json()

    def click(self, element_description: str, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action click with element_description='{element_description}'")

        data = {'element_description': element_description}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/click",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        return response.json()

    def type(self, text: str, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action type with text='{text}'")

        data = {'text': text}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/type",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        return response.json()

    def press_enter(self, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError("Must call create_session before calling action press_enter")

        data = {}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/press-enter",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        return response.json()

    def extract_bbox(self, element_description: str, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action extract_bbox with element_description='{element_description}'")

        data = {'element_description': element_description}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.get(
            f"{BASE_URL}/extract-bbox",
            headers={
                'x-api-key': self.api_key
            },
            params=data
        )
        
        return response.json()

    def extract_text(self, element_description: str, cdp_url: str = None, use_vision: bool = False):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action extract_text with element_description='{element_description}'")

        data = {'element_description': element_description}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        if use_vision:
            data['use_vision'] = use_vision

        response = requests.get(    
            f"{BASE_URL}/extract-text",
            headers={
                'x-api-key': self.api_key
            },
            params=data
        )
        return response.json()

    def extract_image(self, element_description: str, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action extract_image with element_description='{element_description}'")

        data = {'element_description': element_description}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.get(
            f"{BASE_URL}/extract-image",
            headers={
                'x-api-key': self.api_key
            },
            params=data
        )
        return response.json()

    def scroll(self, pixels: float, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action scroll with pixels={pixels}")

        data = {'pixels': pixels}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/scroll",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        return response.json()

    def wait(self, milliseconds: int, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action wait with milliseconds={milliseconds}")

        data = {'milliseconds': milliseconds}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/wait",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        return response.json()
    
    def capture_login_session(self, url: str):
        response = requests.post(
            f"{BASE_URL}/capture_login_session",
            headers={
                'x-api-key': self.api_key
            },
            data={'url': url}
        )
        return response.json()
    
    def restore_login_session(self, session_data_filepath: str, cdp_url: str = None):
        filename = session_data_filepath
        
        with open(filename, 'r') as f:
            session_data = json.load(f)
        
        # Serialize the data to JSON string
        data = {
            'session_data': json.dumps(session_data)  # Serialize the session_data
        }
        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id
        
        response = requests.post(
            f"{BASE_URL}/restore_login_session",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        return response.json()

    def run_agent(self, prompt: str, cdp_url: str = None):
        if not cdp_url and not self.session_id:
            raise ValueError(f"Must call create_session before calling action run_agent with and prompt='{prompt}'")

        data = {'prompt': prompt}

        if cdp_url:
            data['cdp_url'] = cdp_url
        else:
            data['session_id'] = self.session_id

        response = requests.post(
            f"{BASE_URL}/run-agent",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        return response.json()
