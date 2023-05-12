import openai
import requests
import sys
import json
import os
from requests.structures import CaseInsensitiveDict
from main import OpenAISuite
from PIL import Image
from io import BytesIO
from colorama import init, Fore, Style


class DALLE_Suite(OpenAISuite):
    def __init__(self) -> None:
        self.dalle_image_size = "256x256" #default
        self.download_url = ""
        self.dalle_model_engine = "davinci"
        self.user_image_prompt = ""
        self.dalle_image_folder_name = f"/Users/{os.getlogin()}/Pictures/Dalle_Images/"
        #--init colorama
        init()
    
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
                self.dalle_image_size = input(Fore.BLUE + "Enter a DALLE image size (default: 256x256): " + Fore.YELLOW)
                self.dalle_image_size_checker()
                self.user_image_prompt = input(Fore.BLUE + "Enter a DALLE prompt: " + Fore.YELLOW)
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
                    raise ValueError(Fore.RED + "Failed to generate image")
                json_data = json.loads(resp.text)
                self.download_url = json_data['data'][0]['url']
                # Create a clickable link using the OSC 8 escape sequence
                print(Fore.GREEN + '\033[95m'+f'\033]8;;{self.download_url}\aClick here\033]8;;\a')
                # Download the image
                self.dalle_download_image()
            except Exception as ComputeError:
                print(Fore.RED + f"---ComputeError: {ComputeError}")

    def dalle_download_image(self):
        try:
            print(Fore.YELLOW + "+++Downloading image...")
            response = requests.get(self.download_url)
            if response.status_code != 200:
                raise ValueError(Fore.RED + "Failed to download image")
            else:
                print(Fore.GREEN + "---Image downloaded successfully.")
                print(Fore.YELLOW + "+++Saving image...")
                self.dalle_save_image_to_folder(response)
                print(Fore.GREEN + "---Image saved successfully.")
        except ValueError as DownloadError:
            print(Fore.RED + f"---DownloadError: {DownloadError}")
        except Exception as e:
            print(Fore.RED + f"---Exception: {e}")

    def dalle_image_filename_formatting(self):
        if len(self.user_image_prompt) <= 15:
            self.user_image_prompt = self.user_image_prompt.replace(" ", "_")
        elif len(self.user_image_prompt) > 15:
            self.user_image_prompt = self.user_image_prompt.replace(" ", "_")
            self.user_image_prompt = self.user_image_prompt[:15]

    def dalle_save_image_to_folder(self, response):
        try:
            #saving to custom folder i.e. /Users/username/Pictures/Dalle_Images/
            self.create_folder(self.dalle_image_folder_name)
            self.dalle_image_filename_formatting() #formatting filename to be shorter
            image = Image.open(BytesIO(response.content))
            image.save(f'{self.dalle_image_folder_name}/{self.user_image_prompt}.png')
        except Exception as e:
            #saving to current directory if folder creation fails
            print(Fore.RED + "---Folder creation failed, saving to current directory instead.")
            image = Image.open(BytesIO(response.content))
            image.save(f'{self.user_image_prompt}.png')
            print(Fore.RED + f"---FolderCreationError: {e}")

    def create_folder(self, folder_path):
        try:
            print(Fore.YELLOW + "++++Checking if folder exists...")
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(Fore.GREEN + f"----Folder '{folder_path}' created successfully.")
            else:
                print(Fore.GREEN + f"----Folder '{folder_path}' already exists.")
        except OSError as e:
            print(Fore.RED + f"----OSErrorException: {e}")