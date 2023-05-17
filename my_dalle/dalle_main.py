import openai
import pathlib
import sys
import json
import os
import requests
from urllib.error import HTTPError, URLError
from requests.exceptions import RequestException
from main import OpenAISuite
from PIL import Image
from io import BytesIO
from colorama import init, Fore


class DALLE_Suite(OpenAISuite):
    def __init__(self) -> None:
        self.dalle_image_size = "256x256"  # default
        self.download_url = ""
        self.dalle_model_engine = "davinci"
        self.user_image_prompt = ""
        self.dalle_image_folder_name = f"{os.path.expanduser('~')}/Pictures/Dalle_Images/" # platform independent folder structure
        #--init colorama
        init()
    
    def check_dalle_argument(self):
        return '--dalle' in sys.argv or '--d' in sys.argv
    
    def dalle_image_size_checker(self):
        if self.dalle_image_size == '' or '256' in self.dalle_image_size:
            self.dalle_image_size = "256x256"
        elif '512' in self.dalle_image_size:
            self.dalle_image_size = "512x512"
        elif '1024' in self.dalle_image_size:
            self.dalle_image_size = "1024x1024"
        else:
            print("---Invalid image size, defaulting to 256x256")
            self.dalle_image_size = "256x256"
    
    def dalle_generate_image(self):
        while True:
            self.dalle_image_size = input(Fore.BLUE + "Enter a DALLE image size (default: 256x256): " + Fore.YELLOW)
            self.dalle_image_size_checker()
            self.user_image_prompt = input(Fore.BLUE + "Enter a DALLE prompt: " + Fore.YELLOW)
            if self.user_image_prompt == '':
                return
            try:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {openai.api_key}"
                    }
                data = {
                    "prompt": self.user_image_prompt,
                    "num_images": 1,
                    "size": self.dalle_image_size,
                    "response_format": "url"
                }
                json_data = json.dumps(data)  # Convert data to JSON string
                resp = requests.post("https://api.openai.com/v1/images/generations", 
                                     headers=headers, data=json_data)
                if resp.status_code != 200:
                    print(resp.text)
                    raise ValueError(Fore.RED + "Failed to generate image")
                json_data = json.loads(resp.text)
                self.download_url = json_data['data'][0]['url']
                # Create a clickable link using the OSC 8 escape sequence
                print(Fore.GREEN + '\033[95m'+f'\033]8;;{self.download_url}\aClick here\033]8;;\a')
                # Download the image
                self.dalle_download_image()
            except RequestException as e:
                print(Fore.RED + f"---RequestException: {e}")

    def dalle_download_image(self):
        try:
            print(Fore.YELLOW + "+++Downloading image...")
            response = requests.get(self.download_url)
            if response.status_code != 200:
                raise ValueError(Fore.RED + "Failed to download image")
            print(Fore.GREEN + "---Image downloaded successfully.")
            self.dalle_save_image_to_folder(response)
        except (HTTPError, URLError) as e:
            print(Fore.RED + f"---DownloadError: {e}")
        except IOError as e:
            print(Fore.RED + f"---IOError: {e}")

    def dalle_image_filename_formatting(self):
        self.user_image_prompt = self.user_image_prompt.replace(" ", "_")[:15]

    def dalle_save_image_to_folder(self, response):
        # Saving to custom folder, example /Users/username/Pictures/Dalle_Images/
        folder_path = pathlib.Path(self.dalle_image_folder_name)
        folder_path.mkdir(parents=True, exist_ok=True)
        print(Fore.YELLOW + "+++Saving image to -> " +  Fore.MAGENTA + f"{folder_path}")
        self.dalle_image_filename_formatting()  # Formatting filename to be shorter
        image = Image.open(BytesIO(response.content))
        try:
            image.save(folder_path / f'{self.user_image_prompt}.png')
            print(Fore.GREEN + "---Image saved successfully.")
        except Exception as e:
            # Saving to current directory if folder creation fails
            print(Fore.RED + "---Folder creation failed, saving to current directory instead.")
            image.save(f'{self.user_image_prompt}.png')
            print(Fore.RED + f"---FolderCreationError: {e}")

    def create_folder(self, folder_path):
        print(Fore.YELLOW + "++++Checking if folder exists...")
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(Fore.GREEN + f"----Folder '{folder_path}' created successfully.")
            else:
                print(Fore.GREEN + f"----Folder '{folder_path}' already exists.")
        except FileExistsError:
            print(Fore.GREEN + f"----Folder '{folder_path}' already exists.")
        except OSError as e:
            print(Fore.RED + f"----OSErrorException: {e}")