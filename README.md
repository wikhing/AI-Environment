# JS_AI-Environment

Project of JS X AI in little games.




To run this project, you need to install several dependencies
1. Node.js
2. PyTorch


# Run the command in terminal
```
winget install Schniz.fnm

fnm env --use-on-cd | Out-String | Invoke-Expression

fnm use --install-if-missing 22

node -v # should print `v22.11.0`

npm -v # should print `10.9.0`
```


# Steps to install PyTorch:

```
python -m venv venv (You should see a venv folder)

venv\Scripts\activate (To activate the virtual environment)

pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118  
# if this one doesn't work, try this one instead

pip3 install torch torchvision torchaudio  


```
