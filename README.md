# JS_AI-Environment

Project of JS X AI in little games.




To run this project, you need to install several dependencies
1. Node.js
2. PyTorch

1. Below are the steps to install Node.js:

Open your Terminal/Powershell (Windows) and run the following command one by one:
# installs fnm (Fast Node Manager)
winget install Schniz.fnm
# configure fnm environment
fnm env --use-on-cd | Out-String | Invoke-Expression
# download and install Node.js
fnm use --install-if-missing 22
# verifies the right Node.js version is in the environment
node -v # should print `v22.11.0`
# verifies the right npm version is in the environment
npm -v # should print `10.9.0`



2. Below are the steps to install PyTorch:
1. Open your terminal
2. cd into JS_AI-Environment directory
3. Send command line by line :

python -m venv venv (You should see a venv folder)

venv\Scripts\activate (To activate the virtual environment)
It will look something like this if done correctly : (venv) D:\Code\JS_AI-Environment\

Run this command if your GPU has cuda support : pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
Run this command if your GPU does not has cuda support : pip3 install torch torchvision torchaudio

