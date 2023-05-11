## Confirguring Code:
    1. Create .env file in current directory and create variable OPENAI_API_KEY containing your key value,
        Ex: OPENAI_API_KEY=your+api+key+no+quotes
        (Keep .env confidential)
    2. Install all needed library requirements using the requirements.txt file.
       Run below in terminal cd,
        `pip3.10 install requirements.txt`

## Running Code:
    - DALLE Integration, --dalle arg needed.
        Ex: python3.10 main.py --dalle
    - ChatGPT Integration,
        - normal mode, no arg needed to be passed.
            Ex: python3.10 main.py
        - speach mode, --speak arg needed.
            Ex: python3.10 main.py --speak