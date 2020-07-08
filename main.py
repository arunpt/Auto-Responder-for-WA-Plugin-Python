from flask import Flask, request
from addons import plugin, msghandler, send_message


app = Flask(__name__)
@app.route('/bot', methods=['POST'])
def command_handler():
    data = request.get_json()
    incoming = data['query']['message']
    cmd,msg = msghandler(incoming)
    if cmd == "/start":
        return send_message(f"Im alive 😏\n_Powered by : auto responder plugin by mr JUSTIN")
    if cmd == "/help":
        return send_message(plugin.help())
    if cmd == "/sam":
        return send_message(plugin.sam(msg))
    elif cmd == "/tr":
        return send_message(plugin.translate(msg))
    elif cmd == "/mod":
        return send_message(plugin.mod(msg))
    elif cmd == "/flip":
        return send_message(plugin.flip(msg))    
    elif cmd == "/wiki":
        return send_message(plugin.wiki(msg))
    elif cmd == "/dict":
        return send_message(plugin.udict(msg))
    elif cmd == "/maldict":
        return send_message(plugin.olam(msg))
    else:        
        return send_message(" ") #to handle exception thrown by empty msg

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # set port to 5000 if you are using heroku
