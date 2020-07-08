import wikipedia
import urbandict
import sys
import requests
from googletrans import Translator
from bs4 import BeautifulSoup


class Plugin:   
    def help(self):
        return "/start - To check whether bot is online or not\n" \
               "/help - Help message\n" \
               "/tr <language code> = <text to translate>\n" \
               "/dict <word>\n" \
               "/maldict <word>\n" \
               "/wiki <search query>\n" \
               "/mod <app name>\n" \
               
    def mod(self, app_name):
        url = f"https://moddroid.com/?s={app_name.replace(' ','+')}"
        page = BeautifulSoup(requests.get(url).content,"html.parser")
        content = page.find('div',{'class':'rd-details-top'})
        if content:
            app_url = content.find('a', href=True)['href']
            dwn_page = BeautifulSoup(requests.get(app_url + "?download").content,"html.parser")
            app_urls = dwn_page.find('div',{'id':'download-tab'})
            links = ["*Available versions are:*\n\n"]
            [links.append(dwn_url.get_text() + "\n" + dwn_url['href'] + "\n\n") \
               for dwn_url in app_urls.find_all('a', href=True)]
            dwn_url = ''.join(links)
            return dwn_url
        else:
            return "no results"
           
    def translate(self, message):
        try:
            lan_code,text = message.split("=")
        except:
            return "```format /tr ml = Hello```\n" \
                   "_Language codes: https://developers.google.com/admin-sdk/directory/v1/languages_"     
        translator = Translator()
        lan_code = lan_code.strip()
        try:
            translated = translator.translate(text.strip(), dest=lan_code)
            return f"*Translated from {translated.src} to {lan_code}* \n_{translated.text}_"
        except Exception as err:
            return str(err) 
        
   def flip(self, app_name):
      url = requests.get('https://www.flipkart.com/search?q={app_name.replace(' ','+')}')
      content = r.content.decode(encoding='UTF-8')
      soup = BeautifulSoup(r.content.decode(encoding='UTF-8'), "lxml")
      reviews = soup.find_all('div', {"class": "_3ULzGw"})
        for item in reviews:
        return (item.text)
                
    def olam(self, query):
        if not query:
            return "No search query"
        url = "https://olam.in/Dictionary/en_ml/{}".format(query.replace(" ", "+"))
        page = BeautifulSoup(requests.get(url).content, 'html.parser')
        content = page.find('div',{"id":"results"})
        if content:
            meaning = ""
            for words in content.find_all('span'):
                meaning += f"{words.text.strip()}\n"
            return meaning
        else:
            return "No results found"
        
    def udict(self, word):
        try:
            mean = urbandict.define(word)
            return f"Word: {word}\n" \
                   f"Meaning: {mean[0]['def']}\n"
        except:
            return "No results found"
            
    def wiki(self, query):
        if not query:
            return "Invalid search query"
        try:
            excerpt = wikipedia.summary(query)
        except:
            return "No results found"
        return f"*Search query:* {query}\n" \
               f"{excerpt.strip()}"

def msghandler(message): # Split commands and message text
    msgs = message.split(' ',1)
    return msgs if len(msgs) == 2 else [msgs[0].strip(),None]

def send_message(text=None):
    if len(text) >= 65536:
        text = "Exceeded character limit"
    return {"replies": [{"message": text}]}   
            
plugin = Plugin()
