# Auto-Responder WA Plugin 
> A simple bot plugin for whatsapp written in python flask.

### Installation (server side)
```bash
  # clone this repo
  git clone https://github.com/CW4RR10R/Auto-Responder-for-WA-Plugin-Python.git
  cd Auto-Responder-for-WA-Plugin-Python

  # create virtual environment
  virtualenv -p /usr/bin/python3 venv
  . ./venv/bin/activate

  # install requirements via pip
  pip install -r requirements.txt
  
  # start the bot
  python3 main.py
```
### Setup (client side)
* Open AutoResponder WA app
* Create a rule in pattern matching with **_/*_**
* Get the url from your server after installation (something like https://yourdomain.com/bot or http://localhost:8080/bot)
* Enter the url in _Connect to web server_ slot
* Hit save and send /help from another account to the bot
  
**For further reference check the screenshots attached to this repo**