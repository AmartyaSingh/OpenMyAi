import os
import openai
import sys
from gtts import gTTS
from playsound import playsound
from main import OpenAISuite
from colorama import init, Fore, Style


class ChatGPT_Suite(OpenAISuite):
    def __init__(self) -> None:
        self.cgpt_model_engine = "text-davinci-003"
        #--init colorama
        init()
        #--init transcript
        self.transcript = []

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
                        print(Fore.GREEN + "AI: " + Fore.LIGHTMAGENTA_EX + str(formatted_text))
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
        script_args = sys.argv
        if '--speak' in script_args or '--s' in script_args:
            return True
        return False
    
    def check_transcript_argument(self):
        script_args = sys.argv
        if '--transcript' in script_args or '--t' in script_args:
            return True
        return False
    
    def text_to_speech_gtts(self, text):
        # convert text to speech
        tts = gTTS(text=text, lang='en-gb')
        tts.save("response.mp3")
        playsound("response.mp3")
        os.remove("response.mp3")

    def parse_response(self, text):
        last_period_index = text.rfind('.')
        if last_period_index >= 0:
            last_sentence = text[:last_period_index+1]
            new_text = text[:last_period_index]  # remove the last sentence from the text
            return last_sentence
        
    def get_text_response(self, prompt):
        response = openai.Completion.create(
            model=self.cgpt_model_engine,
            prompt=prompt,
            temperature=0.0,
            max_tokens=100)
        return response.choices[0].text.strip()
    
    def create_transcript_file(self):
        with open("transcript.txt", "w") as transcript_file:
            for line in self.transcript:
                transcript_file.write(line + "\n")
    
    