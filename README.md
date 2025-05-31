# HuggingFace Models
## VERY IMPORTANT all models weight like 15 GB
# In first start you will have a huge download because models must locate localy
# If you work on windows and want to delete the model find directory "C:\Users\\<your_user_name>\\.cache\huggingface\hub"



**pip install -r requirements.txt**
For install pytorch on windows use pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126


SUB REQUIREMENTS (WINDOWS)
GO TO https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
Download file https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/download/2022-01-04/gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe

After instalation go to System Environment Variables
IN Users variables for <user> push create with params :
Name: GTK
Value: Path where you save for example (C:\Program Files\GTK3-Runtime Win64\bin)
