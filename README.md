# madb
Multiple choice devices to run adb command

# Requriments
1. Installed adb
2. Python 3.7+
# install
1. Install libs ```xargs -L 1 pip3 install < requirements.txt```
2. Add run permission ```chmod +x madb.py```
3. Link to bin path, *nix example
        
        ln -sf "`pwd`/madb.py" /usr/local/bin/madb
        ln -sf "`pwd`/mscrcpy.py" /usr/local/bin/mscrcpy
5. To work adb completions add to your ~/.zshrc ```compdef '_dispatch adb adb' madb``` and run ```. ~/.zshrc``` . If on start zsh see ```command not found``` change in rc file to 

        autoload -Uz compinit
        compinit
        compdef '_dispatch adb adb' madb

# usage
1. run madb command (all command how adb)
2. choice devices 
3. enter

<img width="428" alt="Screenshot 2022-05-16 at 15 22 05" src="https://user-images.githubusercontent.com/1923645/168593673-81241f16-73d4-45f7-a8c5-f6f63855fccf.png">

# multiple connect device
1. add to your env start with ADB_DEVICE, ex: ```ADB_DEVICE_XIAOMI = 192.168.1.100```
2. run ```madb connect```
3. choice devices
4. enter


# How control inquirer checkboxes 
* Move to down position - arrow down or tab
* Move to up position - arrow uo or shift+tab
* Select position - right arrow or space
* Unselect position - left arrow or space
* Select all positions - ctrl+a
* Unselect all positions ctrl+q
* Confirm selected positions - enter


