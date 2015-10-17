# Talentbot

Talentbot ska minimera tiden det tar att ta reda på vad en kollega kan och vill jobba med, och maximera förståelsen för vilka kunskaper som finns (och inte finns) i företaget.

* Konsulter ska känna sig trygga att sälj vet vad konsulterna kan och vill jobba med
* Sälj ska blixtsnabbt kunna ta reda på vad en given konsult kan

## Arkitektur

* Korta snabba slagningar görs via Slack mha en bot
* Boten är en bot-användare som körs av en Python-baserad känns
* Trello fungerar både som databas och administrationsgränssnitt

                      Undersök talanger
                             +         
                             |         
                             |         
                       +-----v------+  
                       |            |  
                       |   Slack    |  
                       |            |  
                       +-----+------+  
                             |         
                       +-----+------+  
                       |            |  
                       |   Python   |  
                       |            |  
                       +-----+------+  
                             |         
                       +-----+------+  
Definiera talanger     |            |  
Överblicka talanger+--->   Trello   |  
                       |            |  
                       +------------+ 
