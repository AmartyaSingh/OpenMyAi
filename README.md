## Confirguring Code:
    1. Create .env file in current directory and create variable OPENAI_API_KEY containing your key value,
        Ex: OPENAI_API_KEY=your+api+key+no+quotes
        (Keep .env confidential)

    2. Install all needed library requirements using the requirements.txt file into a virtual environment.
        - Run below to create virtual environment in project root dir,
```
          python3.10 -m venv <your_venv_name>
```
```       
          source <your_venv_name>/bin/activate
```
          To deactivate venv,
```       
          deactivate
```
        - Run below in terminal cd,
```
          pip3.10 install requirements.txt
```
          (Assuming pip version 3.10 and python version 3.10 installed)

## Running Code:
###  1. DALLE Mode, 
        a. '--dalle' or '--d' arg needed.
```             
                python3.10 main.py --dalle
```         
            or
```             
                python3.10 main.py --d
```
        b. When running in Dalle mode, 
            - Specify image size i.e. 256, 512 or 1024 in the prompt.
            - Specify image prompt.
            - Wait for image to be returned and downloaded.
            (File saved in <User>/Pictures/Dalle_Images/ directory)
            - `Enter` when done. This will exit present terminal run.

###  2. ChatGPT Mode,
        a. Normal mode, no arg needed to be passed.
```
                    python3.10 main.py
```
        b. Speech mode, '--speak' or '--s' arg needed.
```
                    python3.10 main.py --speak
```         
            or
```
                    python3.10 main.py --s
```
        c. Transcript Mode, '--transcript' or '--t' options.
```
                    python3.10 main.py --transcript
```         
            or
```
                    python3.10 main.py --t
```
            - Runs can have multiple options as well.
```
                    python3.10 main.py --s --t
```
            - `Enter` when done. This will exit present terminal run.