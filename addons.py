import wikipedia
import urbandict
import requests
from urllib.parse import urlparse
from googletrans import Translator
from bs4 import BeautifulSoup

class Plugin:   
    def help(self):
        return "/start - To check whether bot is online or not\n" \
               "/help - Help message\n" \
               "/tr <language code> = <text to translate>\n" \
               "/dict <word> - English dictionary\n" \
               "/maldict <word> - Eng-Mal dictionary\n" \
               "/wiki <search query> - Wiki searching\n" \
               "/mod <app name> - Get mod apps\n" \
               "/klcovid - Kerala covid statistics\n" \
               "/flip <product name> - Search flipkart products\n" \
               "/weather <location> - weather\n" \
               
     
    def parse_html(self, url):
        return BeautifulSoup(requests.get(url).content,"html.parser")
    
    def weather(self, location):
        if not location:
            return "format /weather kannur"            
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={location.strip()}&units=metric&appid=APP_ID"
        r = requests.get(api_url).json()
        return f'*Location:* _{location.strip()}_\n' \
               f'*Temperature:* _{r["main"]["temp"]}℃_\n' \
               f'*Humidity:* _{r["main"]["humidity"]}_\n' \
               f'*Wind Speed:* _{r["wind"]["speed"]}_\n' \
               f'*Condition:* _{r["weather"][0]["description"]}_'
                     
    def covid(self):
        soup = self.parse_html("https://dashboard.kerala.gov.in/")
        confirmed = soup.find("div",{"class":"small-box bg-info"}).h3.text
        active = soup.find("div",{"class":"small-box bg-warning"}).h3.text
        recovered = soup.find("div",{"class":"small-box bg-success"}).h3.text
        death = soup.find("div",{"class":"small-box bg-danger"}).h3.text
        updated = soup.find("li",{"class":"breadcrumb-item active"}).text
        return f"🥺 *Confirmed:* {confirmed}\n\n😨 *Active:* {active}\n\n💚 *Recovered:* {recovered}\n\n😥 *Death:* {death}\n\n _{updated}_"
    
    def flip(self, query):
        if not query:
            return "/flip <product name>"
        soup = self.parse_html(f"https://www.flipkart.com/search?q={query.replace(' ','+')}")
        parsed = soup.find_all("div",{"class":"_1-2Iqu row"})
        if len(parsed) == 0:
            return "No results"
        msg = ""  
        for i,content in enumerate(parsed):
            msg += f"*{content.find('div',class_='_3wU53n').get_text().strip()}*\n"
            msg += "Price: " + content.find("div",class_="_1vC4OE _2rQ-NK").get_text() + "\n"
            msg += content.find("span",class_="_38sUEc" ).get_text() + "\n" if content.find("span",class_="_38sUEc" ) else "No ratings\n" 
            msg += "".join([f"● _{specs.get_text().strip()}_\n" for specs in content.find_all("li",class_="tVe95H")])
            prdct_url =  "https://www.flipkart.com" + soup.find_all("div", {"class": "_1UoZlX"})[i].a.get('href')
            msg += requests.get(f"https://da.gd/s?url={prdct_url}").text + "\n\n"
        return msg
        
    def dl_droid(self, app_name):
        page = self.parse_html(f"https://dlandroid.com/?s={app_name.replace(' ','+')}")
        results = page.find('div',class_="post")
        if results:
            page_url = results.find('a', href=True)['href']
            app_id = urlparse(page_url).path.strip("/")
            dwn_page = self.parse_html(f"https://dl-android.com/p/index.php?id={app_id}")    
            dwn_btn = dwn_page.find("div",class_="dlbtng")
            link = ["*Available versions are:*\n\n"]
            [link.append(links.get_text() + "\n" + links['href'] + "\n\n") for links in dwn_btn.find_all('a', href=True) if links.get_text() != "Azio - Download New Music Offline Free"]
            return ''.join(link)
        else:
            return "No results found"
            
    def mod(self, app_name):
        if not app_name:
            return "format\n/mod <app name>"
        url = f"https://moddroid.com/?s={app_name.replace(' ','+')}"
        page = self.parse_html(url)
        content = page.find('div',{'class':'rd-details-top'})
        if content:
            app_url = content.find('a', href=True)['href']
            dwn_page = self.parse_html(app_url + "?download")
            app_urls = dwn_page.find('div',{'id':'download-tab'})
            links = ["*Available versions are:*\n\n"]
            [links.append(dwn_url.get_text() + "\n" + dwn_url['href'] + "\n\n") \
               for dwn_url in app_urls.find_all('a', href=True)]
            return ''.join(links)            
        else:
            return self.dl_droid(app_name)
           
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
                
    def olam(self, query):
        if not query:
            return "No search query"
        url = "https://olam.in/Dictionary/en_ml/{}".format(query.replace(" ", "+"))
        page = self.parse_html(url)
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