from flask import Flask, request, jsonify
import os
import json
from colorizer import Colorizer


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/api', methods=['POST'])
def hello():
    if request.method == 'POST':
        f = request.files['file']
        base64_colored_img = Colorizer(f)
        print(base64_colored_img)
        return json.dumps([f"{base64_colored_img}"])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)