# Kör applikationen på Ubuntu 14.04

## Installera Python 2.7.10 på ubuntu
Från http://tecadmin.net/install-python-2-7-on-ubuntu-and-linuxmint/
```
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

cd /usr/src
sudo wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
sudo tar xzf Python-2.7.10.tgz

cd Python-2.7.10
sudo ./configure
sudo make altinstall
```

## Installera pip för Python 2.7.10 (pip2.7)
```
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python2.7 get-pip.py
```

## Starta applikationen i bakgrunden
```
git clone git@github.com:citerus/talentbot.git
cd talentbot
pip2.7 install -r requirements.txt
nohup python2.7 main.py &
```
