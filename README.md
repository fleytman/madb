# madb
Multiple choice devices to run adb command

# Requriments
1. Installed adb
2. Python 3.7+
# install
1. Install libs ```pip3 install -r requirements.txt```
2. Add run permission ```chmod +x madb.py```
3. Copy to bin path, example ```cp madb.py /usr/local/bin/madb```
4. To work adb completions add to your ~/.zshrc ```compdef madb=adb``` and run ```. ~/.zshrc``` . If on start zsh see ```command not found``` change in rc file to 

        autoload -Uz compinit
        compinit
        compdef madb=adb

# usage
1. run madb command (all command how adb)
2. choice devices
3. enter


<img width="428" alt="Screenshot 2022-05-16 at 15 22 05" src="https://user-images.githubusercontent.com/1923645/168593673-81241f16-73d4-45f7-a8c5-f6f63855fccf.png">


