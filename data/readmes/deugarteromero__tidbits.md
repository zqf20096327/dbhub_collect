# tidbits
A bundle of tidbits!


### Nodejs - List Global Packages
```
npm list -g --depth 0
```
<hr>

### Windows 10 - Check & Kill Used Ports (ex. port 5000)
Using Powershell (might need admin)

To Check
```
netstat -aon | findstr 5000
```
A list of tasks/programs will appear with according PID (end of line)

To Kill (Use PID)
```
taskkill /PID <PIDHERE> /F
```
<hr>

### Linux (Ubuntu) - Check Current Version
```
lsb_release -a
```
