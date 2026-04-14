from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# গ্লোবাল ভেরিয়েবল যেখানে গাড়ির বর্তমান কমান্ড সেভ থাকবে।
# 'S' মানে Stop.
current_command = "S" 

@app.route('/')
def index():
    # এটি আপনার রিমোট কন্ট্রোল ওয়েবপেজ লোড করবে
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update_command():
    global current_command
    data = request.json
    if data and 'command' in data:
        current_command = data['command']
        print(f"New Command Received: {current_command}")
        return jsonify({"status": "success", "command": current_command})
    return jsonify({"status": "error"}), 400

@app.route('/command', methods=['GET'])
def get_command():
    # ESP8266 এই লিংকে এসে বর্তমান কমান্ডটি নিয়ে যাবে
    return current_command

if __name__ == '__main__':
    # Render.com এর জন্য 0.0.0.0 তে রান করতে হয়
    app.run(host='0.0.0.0', port=10000)