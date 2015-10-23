# Talentbot

Talentbot ska minimera tiden det tar att ta reda på vad en kollega kan och vill jobba med, och maximera förståelsen för vilka kunskaper som finns (och inte finns) i företaget.

* Konsulter ska känna sig trygga att sälj vet vad konsulterna kan och vill jobba med
* Sälj ska blixtsnabbt kunna ta reda på vad en given konsult kan

## Arkitektur

* Användare gör slagningar i sin Slack-klient
* Slagningarna fångas av Talentbot, som körs som en [bot user](https://api.slack.com/bot-users)
* Boten är realiserad med en Python-baserad tjänst
* Trello fungerar både som databas och administrationsgränssnitt

## Kom igång med Talentbot

Klona repositoryt till din lokala maskin: 

> git clone https://github.com/citerus/talentbot.git

Använd virtualenv för att skapa en lokal Pythonmiljö att installera paket i:

> virtualenv env

Installera nödvändiga paket:

> pip install -r requirements.txt

### Python

* [Introduktion till Pythons pakethantering](http://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/)
* [Miljökonfiguration på Mac](http://hackercodex.com/guide/python-development-environment-on-mac-osx/)
* [Installera paket](https://pip.readthedocs.org/en/1.1/requirements.html#requirements-files) med pip install -r requirements.txt

### Slack

* https://api.slack.com
* https://api.slack.com/rtm
* Exempel på anrop till Slacks API: https://github.com/os/slacker/blob/master/slacker/__init__.py

### Trello

* https://developers.trello.com
* [Om Trellos rate limits](http://help.trello.com/article/838-api-rate-limits)
