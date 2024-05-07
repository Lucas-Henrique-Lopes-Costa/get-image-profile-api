from flask import Flask, jsonify
import requests
import os


app = Flask(__name__)

@app.route('/api/instagram/<username>')
def get_instagram_user_info(username):
    url = f"https://storiesig.info/api/ig/userInfoByUsername/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch data"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)