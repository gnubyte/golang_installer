# Golang Installer for *nix

Some space-pilot astronauts that make Go Lang & maintain its' website thought it would be funny to make installing Go Lang a pain in the ass. Especially if whatever process you are following requires specific versions of go in order to develop for that application. So here is a program/script that makes it easy. 

If you're on Ubuntu save yourself a haedache and just run a `sudo apt-get install golang -y`


## What

 - installs golang
 - puts it in your bash (bashrc or bash_profile) profile
 - offers an interactive menu of versions for linux users to install golang from, optionally
 - offers a simple portable binary you can run to install golang non interactively


## Requirements
 - you're running linux
 - Linux x86, X64 machines at this time
 - you're using bash


## Usage


#### Using the binary

From the binary, get a menu of different versions (WARNING it can be long):

```./main.bin --versions```

Install Go-lang v1.18

```./main.bin```



Install a specific version

```./main.bin -v 1.18```


#### Using the script

Clone this repo

Install the python requirements

```pip3 install -r requirements.txt```


Run The Script.

```python3 main.py --versions```


