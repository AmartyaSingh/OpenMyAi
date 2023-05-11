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
        self.download_url = ""
        self.user_image_prompt = ""

    def check_dalle_argument(self):
        script_args = sys.argv
        if '--dalle' in script_args:
            return True
        return False
    
    def dalle_generate_image(self, size="256x256"):
        while True:
            try:
                self.user_image_prompt = input("Enter a DALLE prompt: ")
                if self.user_image_prompt == '':
                    break
                headers = CaseInsensitiveDict()
                headers["Content-Type"] = "application/json"
                headers["Authorization"] = f"Bearer {openai.api_key}"
                data = f"""{{
                            "prompt": "{self.user_image_prompt}",
                            "num_images": 1,
                            "size": "{size}",
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
                image = Image.open(BytesIO(response.content))
                image.save(f'{self.user_image_prompt}.png')
                print("---Image saved successfully.")
        except ValueError as DownloadError:
            print(f"---DownloadError: {DownloadError}")
        except Exception as e:
            print(f"---Exception: {e}")