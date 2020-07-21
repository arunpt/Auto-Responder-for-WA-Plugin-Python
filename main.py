from flask import Flask, request, render_template
from addons import plugin, msghandler, send_message


app = Flask(__name__)
@app.route('/bot', methods=['POST'])
def command_handler():
    data = request.get_json()
    incoming = data['query']['message']
    cmd,msg = msghandler(incoming)
    if cmd == "/start":
        return send_message(f"Im alive 😏\n_Powered by : auto responder plugin by W4RR10R_")
    if cmd == "/help":
        return send_message(plugin.help())
    elif cmd == "/tr":
        return send_message(plugin.translate(msg))
    elif cmd == "/wiki":
        return send_message(plugin.wiki(msg))
    elif cmd == "/dict":
        return send_message(plugin.udict(msg))
    elif cmd == "/maldict":
        return send_message(plugin.olam(msg))
    elif cmd == "/mod":
        return send_message(plugin.mod(msg))
    elif cmd == "/flip":
        return send_message(plugin.flip(msg))
    elif cmd == "/klcovid":
        return send_message(plugin.covid())
    elif cmd == "/weather":
        return send_message(plugin.weather(msg))
    else:        
        return send_message(" ") #to handle exception thrown by empty msg

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template("forbidden.html")
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)