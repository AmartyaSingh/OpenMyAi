import os
import openai
from dotenv import load_dotenv


class OpenAISuite:
    def __init__(self) -> None:
        load_dotenv()        
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def main(self):
        from my_dalle.dalle_main import DALLE_Suite
        from my_chatgpt.chatgpt_main import ChatGPT_Suite
        chatgpt_obj = ChatGPT_Suite()
        dalle_obj = DALLE_Suite()
        #--speak enabled. Use --speak to enable text to speech
        if chatgpt_obj.check_speech_argument():
            chatgpt_obj.chat_run(speak_mode=True)
        #--dalle enabled. Use --dalle to enable dalle image generation
        elif dalle_obj.check_dalle_argument():
            dalle_obj.dalle_generate_image()
        #normal mode text run
        elif not chatgpt_obj.check_speech_argument():
            chatgpt_obj.chat_run()

if __name__ == "__main__":
    openai_suite = OpenAISuite()
    openai_suite.main()
