## Confirguring Code:
    1. Create .env file in current directory and create variable OPENAI_API_KEY containing your key value,
        Ex: OPENAI_API_KEY=your+api+key+no+quotes
        (Keep .env confidential)

    2. Install all needed library requirements using the requirements.txt file into a virtual environment.
        - Run below to create virtual environment in project root dir,
```bash
          python3.10 -m venv <your_venv_name>
          source <your_venv_name>/bin/activate
```
          To deactivate venv,
```bash
          deactivate
```
        - Run below in terminal cd,
```bash
          pip3.10 install requirements.txt
```
          (Assuming pip version 3.10 and python version 3.10 installed)

## Running Code:
###  1. DALLE Mode, 
        a. Using the dalle shell script.
```bash             
                ./run_dalle.sh
```         
        (If encountering permission denied error, use `chmod +x ./run_dalle.sh` in current directory)

        b. When running in Dalle mode, 
            - Specify image size i.e. 256, 512 or 1024 in the prompt.
            - Specify image prompt.
            - Wait for image to be returned and downloaded.
            (File saved in <User>/Pictures/Dalle_Images/ directory)
            - `Enter` when done. This will exit present terminal run.

###  2. ChatGPT Mode,
        a. Normal mode, no arg needed to be passed.
```bash
                    ./run_chatgpt.sh
```
        (If encountering permission denied error, use `chmod +x ./run_dalle.sh` in current directory)
        
        b. Speech mode, '--speak' or '--s' arg needed.
```bash
                    ./run_chatgpt.sh --speak
```         
            or
```bash
                    ./run_chatgpt.sh --s
```
        c. Transcript Mode, '--transcript' or '--t' options.
```bash
                    ./run_chatgpt.sh --transcript
```         
            or
```bash
                    ./run_chatgpt.sh --t
```
            - Runs can have multiple options as well.
```bash
                    ./run_chatgpt.sh --s --t
```
            - `Enter` when done. This will exit present terminal run.