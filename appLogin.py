from flask import Flask, jsonify, request
from flask_cors import CORS
import instaloader

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Autenticação Instaloader
L = instaloader.Instaloader()

# Autenticação do Instagram (substitua 'SEU_USUÁRIO' e 'SUA_SENHA' pelos seus dados de login)
L.login("SEU_USUÁRIO", "SUA_SENHA")

@app.route('/profile_pic', methods=['GET'])
def get_profile_pic():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    try:
        # Tentar acessar o perfil do Instagram
        profile = instaloader.Profile.from_username(L.context, username)
        return profile.profile_pic_url

    except instaloader.exceptions.LoginRequiredException:
        return jsonify({'error': 'Authentication error: Login required'}), 401
    except instaloader.exceptions.ProfileNotExistsException:
        return jsonify({'error': 'Profile not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
