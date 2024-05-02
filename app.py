from flask import Flask, jsonify, request, send_from_directory, url_for
from flask_cors import CORS
import instaloader
import requests
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Pasta onde as imagens serão armazenadas
IMAGE_DIR = "image"
os.makedirs(IMAGE_DIR, exist_ok=True)


@app.route("/profile_pic", methods=["GET"])
def get_profile_pic():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400

    L = instaloader.Instaloader()
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        image_url = profile.profile_pic_url
        image_path = os.path.join(IMAGE_DIR, f"{username}.jpg")

        # Baixa a imagem e salva localmente
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_path, "wb") as f:
                f.write(response.content)
        else:
            return jsonify({"error": "Failed to download image"}), 500

        # Constrói a URL segura (HTTPS) para a imagem local
        # Modifique para usar url_for e _external=True para garantir que a URL completa seja gerada com HTTPS
        image_url = url_for("download_file", filename=f"{username}.jpg", _external=True)
        image_url = (
            image_url.replace("http://", "https://")
            if "localhost" not in image_url
            else image_url
        )

        # Retorna a URL local da imagem
        return jsonify({"profile_pic_url": image_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/image/<path:filename>")
def download_file(filename):
    return send_from_directory(IMAGE_DIR, filename, as_attachment=False)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
