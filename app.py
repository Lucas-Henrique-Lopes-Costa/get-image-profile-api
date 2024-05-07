from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/api/instagram/<username>')
def get_instagram_user_info(username):
    url = f"https://storiesig.info/api/ig/userInfoByUsername/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch data"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
