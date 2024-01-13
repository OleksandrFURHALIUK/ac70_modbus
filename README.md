# Readme
***
This program is designed to control the frequency converter Veichi AC70 via rs485 network 
with Ethernet -> Rs485 converter VTR-E/485 with default port 9761
***
### Install
Install requirements with command
```commandline
pip install -r requirements.txt
```

---
### Build
For build binary with pyinstaller use command
``` commandline
pyinstaller --onefile --name=ac70 main.py
```
After execution in current directory will bee presence folder build and dist. Ready binary file will be in dist directory with name ac70.

---
### Work with program
For example read state use command:
```commandline
ac70 192.168.3.198 get_state
```
For set motor data use:
```commandline
ac70 192.168.3.198 set_motor_data 220 5.4 2.2 50 1440
```
Where: 
* 220 - voltage in V 
 *   5.4 - current in A 
 *   2.2 - power in kW 
 *   50 - frequency in Hz 
 *   1440 - speed in RPM 