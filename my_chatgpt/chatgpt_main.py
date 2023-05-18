import os
import openai
import sys
import time
import pathlib
from gtts import gTTS
from playsound import playsound
from main import OpenAISuite
from colorama import init, Fore


class ChatGPT_Suite(OpenAISuite):
    def __init__(self) -> None:
        self.cgpt_model_engine = "text-davinci-003"
        #--init colorama
        init()
        #--init transcript
        self.transcript = []
        self.transcript_folder_path = f"{os.path.expanduser('~')}/Documents/ChatGPT_Transcripts/" # platform independent folder structure


    def chat_run(self, speak_mode=False, transcript_mode=False):
        while True:
            human_input = input(Fore.BLUE + "Me: " + Fore.YELLOW)
            self.transcript.append('Human: ' + human_input)
            if human_input == '':
                break
            try:
                text_response = self.get_text_response(human_input + ' AI: ')
                if text_response:
                    formatted_text = self.parse_response(text_response)
                    print(Fore.GREEN + "AI: " + Fore.LIGHTMAGENTA_EX + formatted_text)
                    self.transcript.append('AI: ' + formatted_text)
                    if speak_mode:
                        self.text_to_speech_gtts(formatted_text)
                else:
                    raise AssertionError("No response from AI")
            except AssertionError as error:
                print(Fore.RED + f"---Error: {error}")
            except openai.error.RateLimitError as rl_error:
                print(Fore.RED + f"---RateLimitError: {rl_error}")
            except Exception as error:
                print(Fore.RED + f"---Error: {error}")
        if transcript_mode:
            self.create_transcript_file()

    def check_speech_argument(self):
        return '--speak' in sys.argv or '--s' in sys.argv
    
    def check_transcript_argument(self):
        return '--transcript' in sys.argv or '--t' in sys.argv

    ##test using pyttx3 module for in-memory usage instead of hard file creation.
    def text_to_speech_gtts(self, text):
        # convert text to speech
        tts = gTTS(text=text, lang='en-gb')
        tts.save("response.mp3")
        playsound("response.mp3")
        os.remove("response.mp3")

    def parse_response(self, text):
        last_period_index = text.rfind('.')
        text = text.replace("\n", "")
        if last_period_index != -1:
            all_but_last_sentence = text[:last_period_index+1]
            new_text = text[:last_period_index]  # remove the last sentence from the text
            return all_but_last_sentence
        return text
        
    def get_text_response(self, prompt):
        response = openai.Completion.create(
            model=self.cgpt_model_engine,
            prompt=prompt,
            temperature=0.0,
            max_tokens=100, 
            n=1)
        text_response = response.choices[0].text
        return text_response
    
    def create_transcript_file(self):
        self.remove_last_human_blank_input()
        try:
            folder_path = pathlib.Path(self.transcript_folder_path)
            folder_path.mkdir(parents=True, exist_ok=True)
            # Saving to custom folder, example /Users/username/Documents/ChatGpt_Transcripts/
            print(Fore.YELLOW + "+++Saving Transcript to -> " +  Fore.MAGENTA + f"{self.transcript_folder_path}")
            with open(f"{folder_path}/transcript_{str(int(time.time()))}.txt", "w") as transcript_file:
                transcript_file.writelines(line + "\n" for line in self.transcript)
            print(Fore.GREEN + "---Transcript saved successfully.")
        except Exception as e:
            print(Fore.RED + "---Folder creation failed, saving to current directory instead.")
            with open(f"transcript_{str(int(time.time()))}.txt", "w") as transcript_file:
                transcript_file.writelines(line + "\n" for line in self.transcript)
            print(Fore.RED + f"---FolderCreationError: {e}")

    def remove_last_human_blank_input(self):
        if self.transcript:
            del self.transcript[-1]