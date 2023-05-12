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

    def chat_run(self, speak_mode=False):
            while True:
                human_input = input(Fore.BLUE + "Me: " + Fore.YELLOW)
                if human_input == '':
                    break
                try:
                    text_response = self.get_text_response(human_input + ' AI: ')
                    if text_response:
                        formatted_text = self.parse_response(text_response)
                        print(Fore.GREEN + "AI: " + Fore.LIGHTMAGENTA_EX + str(formatted_text))
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

    def check_speech_argument(self):
        script_args = sys.argv
        if '--speak' in script_args:
            return True
        return False
    
    def text_to_speech_gtts(self, text):
        # convert text to speech
        tts = gTTS(text=text, lang='en-gb')
        tts.save("response.mp3")
        playsound("response.mp3")
        os.remove("response.mp3")

    '''
    def text_to_speech_pyttsx(self, text): #SEGMENTATION FAULT ERROR
        self.text_to_speech_engine = pyttsx3.init()
        # set the voice rate and volume
        self.text_to_speech_engine.setProperty('rate', 150)    # voice rate in words per minute
        self.text_to_speech_engine.setProperty('volume', 0.6)  # volume level between 0 and 1
        # convert text to speech
        self.text_to_speech_engine.say(text)
        self.text_to_speech_engine.runAndWait()
    '''

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
    

    