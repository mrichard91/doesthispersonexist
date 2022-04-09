from flask import Flask, jsonify, request
from flask_cors import cross_origin
from gan_detector import scan_url
import json
app = Flask(__name__)

@app.route('/scan_url', methods=['POST'])
@cross_origin()
def url_scan():
    url = json.loads(request.data).get('url')
    try:
        results = scan_url(url)
    except Exception as e:
        return jsonify({'status': 'fail', 'results': str(e)})
    print(results)
    return jsonify({'status': 'ok', 'results': results})

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)