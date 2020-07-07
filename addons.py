import wikipedia
import urbandict
import requests
from googletrans import Translator
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq

class Plugin:
    def sam(self, message):
        retun 
        my_url="https://www.flipkart.com/search?q=samsung+mobiles&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_HistoryAutoSuggest_0_2&otracker1=AS_QueryStore_HistoryAutoSuggest_0_2&as-pos=0&as-type=HISTORY&as-searchtext=sa"

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

containers = page_soup.findAll("div", { "class": "_3O0U0u"})
#print(len(containers))

#print(soup.prettify(containers[0]))

container = containers[0]
#print(container.div.img["alt"])

price = container.findAll("div", {"class": "col col-5-12 _2o7WAb"})
#print(price[0].text)


ratings = container.findAll("div", {"class": "niH0FQ"})
#rint(ratings[0].text)

filename = "products.csv"
f = open(filename, "w")

headers = "Product_Name, Pricing, Ratings \n"
f.write(headers)

for container in containers:
    product_name = container.div.img["alt"]
    price_container = container.findAll("div", {"class": "col col-5-12 _2o7WAb"})
    price = price_container[0].text.strip()

    rating_container = container.findAll("div", {"class": "niH0FQ"})
    rating = rating_container[0].text

   #rint("Product_Name:"+ product_name)
   #print("Price: " + price)
   #print("Ratings:" + rating)

    #String parsing
    trim_price=''.join(price.split(','))
    rm_rupee = trim_price.split('₹')
    add_rs_price = "Rs."+rm_rupee[1]
    split_price = add_rs_price.split('E')
    final_price = split_price[0]

    split_rating = rating.split(" ")
    final_rating = split_rating[0]

    print(product_name.replace("," ,"|") +"," + final_price +"," + final_rating + "\n")
    f.write(product_name.replace("," ,"|") +"," + final_price +"," + final_rating + "\n")
f.close()
    def help(self):
        return "/start - To check whether bot is online or not\n" \
               "/help - Help message\n" \
               "/tr <language code> = <text to translate>\n" \
               "/dict <word>\n" \
               "/maldict <word>\n" \
               "/wiki <search query>\n" \
               
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
