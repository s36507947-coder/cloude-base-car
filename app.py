import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# গ্লোবাল ভেরিয়েবল: ডিফল্টভাবে গাড়ি থেমে থাকবে (S = Stop)
current_command = "S"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update_command():
    global current_command
    data = request.json
    if data and 'command' in data:
        current_command = data['command']
        # সিরিয়ালে দেখার জন্য প্রিন্ট (অপশনাল)
        print(f"Server received: {current_command}")
        return jsonify({"status": "success", "command": current_command})
    return jsonify({"status": "error"}), 400

@app.route('/command', methods=['GET'])
def get_command():
    # ESP8266 এই এন্ডপয়েন্ট থেকে কমান্ড পড়বে
    return current_command

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)