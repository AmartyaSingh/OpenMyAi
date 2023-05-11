import openai
import requests
import sys
import json
from requests.structures import CaseInsensitiveDict
from main import OpenAISuite
from PIL import Image
from io import BytesIO

class DALLE_Suite(OpenAISuite):
    def __init__(self) -> None:
        self.dalle_image_size = "256x256"
        self.download_url = ""
        self.dalle_model_engine = "davinci"
        self.user_image_prompt = ""

    def check_dalle_argument(self):
        script_args = sys.argv
        if '--dalle' in script_args:
            return True
        return False
    
    def dalle_image_size_checker(self):
        try:
            if self.dalle_image_size == '' or '256' in self.dalle_image_size:
                self.dalle_image_size = "256x256"
            elif '512' in self.dalle_image_size:
                self.dalle_image_size = "512x512"
            elif '1024' in self.dalle_image_size:
                self.dalle_image_size = "1024x1024"
            elif '256' not in self.dalle_image_size and \
                 '512' not in self.dalle_image_size and \
                 '1024' not in self.dalle_image_size:
                print("---Invalid image size, defaulting to 256x256")
                self.dalle_image_size = "256x256"
        except:
            self.dalle_image_size = "256x256"
            raise ValueError("---Invalid image size, defaulting to 256x256")
    
    def dalle_generate_image(self):
        while True:
            try:
                self.dalle_image_size = input("Enter a DALLE image size (default: 256x256): ")
                self.dalle_image_size_checker()
                self.user_image_prompt = input("Enter a DALLE prompt: ")
                if self.user_image_prompt == '':
                    break
                headers = CaseInsensitiveDict()
                headers["Content-Type"] = "application/json"
                headers["Authorization"] = f"Bearer {openai.api_key}"
                data = f"""{{
                            "prompt": "{self.user_image_prompt}",
                            "num_images": 1,
                            "size": "{self.dalle_image_size}",
                            "response_format": "url"
                        }}"""
                resp = requests.post("https://api.openai.com/v1/images/generations", 
                                    headers=headers, data=data)
                if resp.status_code != 200:
                    print(resp.text)
                    raise ValueError("Failed to generate image")
                json_data = json.loads(resp.text)
                self.download_url = json_data['data'][0]['url']
                # Create a clickable link using the OSC 8 escape sequence
                print(f'\033]8;;{self.download_url}\aClick here\033]8;;\a')
                # Download the image
                self.dalle_download_image()
            except Exception as ComputeError:
                print(f"---ComputeError: {ComputeError}")

    def dalle_download_image(self):
        try:
            print("+++Downloading image...")
            response = requests.get(self.download_url)
            if response.status_code != 200:
                raise ValueError("Failed to download image")
            else:
                print("---Image downloaded successfully.")
                print("+++Saving image...")
                self.dalle_image_filename_formatting() #formatting filename to be shorter
                image = Image.open(BytesIO(response.content))
                image.save(f'{self.user_image_prompt}.png')
                print("---Image saved successfully.")
        except ValueError as DownloadError:
            print(f"---DownloadError: {DownloadError}")
        except Exception as e:
            print(f"---Exception: {e}")

    def dalle_image_filename_formatting(self):
        if len(self.user_image_prompt) <= 15:
            self.user_image_prompt = self.user_image_prompt.replace(" ", "_")
        elif len(self.user_image_prompt) > 15:
            self.user_image_prompt = self.user_image_prompt.replace(" ", "_")
            self.user_image_prompt = self.user_image_prompt[:15]
