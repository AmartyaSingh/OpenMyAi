## Confirguring Code:
    1. Create .env file in current directory and create variable OPENAI_API_KEY containing your key value,
        Ex: OPENAI_API_KEY=your+api+key+no+quotes
        (Keep .env confidential)

    2. Install all needed library requirements using the requirements.txt file into a virtual environment.
        - Run below in terminal cd,
          ```pip3.10 install requirements.txt```
          (Assuming pip version 3.10 and python version 3.10 installed)
        - Run below to create virtual environment in project root dir,
          ```python3.10 -m venv <your_venv_name>```
          ```source <your_venv_name>/bin/activate```
          To deactivate venv,
          ```deactivate```

## Running Code:
    1. DALLE Integration, --dalle arg needed.
        Ex: ```python3.10 main.py --dalle```
    2. ChatGPT Integration,
        - normal mode, no arg needed to be passed.
            Ex: ```python3.10 main.py```
        - speech mode, --speak arg needed.
            Ex: ```python3.10 main.py --speak```