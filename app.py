from flask import Flask, jsonify, request
from flask_cors import cross_origin
from gan_detector import scan_url, scan_data
import json
app = Flask(__name__)

@app.route('/scan_url', methods=['POST'])
@cross_origin()
def url_scan():
    payload = json.loads(request.data)
    if str(payload.get('url')).startswith('http'):
        url = payload.get('url')
        try:
            results = scan_url(url)
        except Exception as e:
            return jsonify({'status': 'fail', 'results': str(e)})
    elif str(payload.get('data')).startswith('data'):
        try:
            data = payload.get('data').split(',')[1]
            results = scan_data(data)
        except Exception as e:
            return jsonify({'status': 'fail', 'results': str(e)})
    return jsonify({'status': 'ok', 'results': results})

@app.route('/')
def main():
    return jsonify({'status': 'ok'})

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)