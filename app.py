from flask import Flask, jsonify, request
from flask_cors import CORS
import instaloader

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

@app.route('/profile_pic', methods=['GET'])
def get_profile_pic():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, username)
    
    return jsonify({'profile_pic_url': profile.profile_pic_url})

if __name__ == '__main__':
    app.run(debug=True)
