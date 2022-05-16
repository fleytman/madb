# madb
Multiple choice devices to run adb command

# Requriments
1. Unix based OS
2. Installed adb
3. Python3
# install
1. Install libs ```pip3 install -r requirements.txt```
2. Copy to bin path, example ```cp madb.py /usr/local/bin/madb```
3. To work adb completions add to your ~/.zshrc ```compdef madb=adb``` and run ```. ~/.zshrc```