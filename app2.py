
from flask import Flask, jsonify, request, send_from_directory, url_for
from flask_cors import CORS
import instaloader
import requests
import os
import threading

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Pasta onde as imagens serão armazenadas
IMAGE_DIR = "image"
os.makedirs(IMAGE_DIR, exist_ok=True)


def download_image(image_url, image_path, callback):
    try:
        response = requests.get(image_url, timeout=7)  # Timeout para a requisição
        if response.status_code == 200:
            with open(image_path, "wb") as f:
                f.write(response.content)
            callback(None, image_url)
        else:
            callback("Failed to download image", None)
    except requests.exceptions.RequestException as e:
        callback(str(e), None)


@app.route("/profile_pic", methods=["GET"])
def get_profile_pic():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400

    L = instaloader.Instaloader()

    # Fazer login antes de carregar o perfil
    L.login(
        "lucashlc.contato", "Instagram@fake123"
    )  # Substitua pelos detalhes de sua conta

    try:
        profile = instaloader.Profile.from_username(L.context, username)
        image_url = profile.profile_pic_url
        image_path = os.path.join(IMAGE_DIR, f"{username}.jpg")

        def on_complete(error, image_url):
            if error:
                return jsonify({"error": error}), 500
            image_url = url_for(
                "download_file", filename=f"{username}.jpg", _external=True
            )
            image_url = (
                image_url.replace("http://", "https://")
                if "localhost" not in image_url
                else image_url
            )
            return jsonify({"profile_pic_url": image_url})

        # Inicia uma thread para baixar a imagem
        thread = threading.Thread(
            target=download_image, args=(image_url, image_path, on_complete)
        )
        thread.start()
        thread.join(timeout=7)  # Espera no máximo 7 segundos
        if thread.is_alive():
            thread.join(1)  # Dá mais 1 segundo para a thread concluir
            return jsonify(
                {"profile_pic_url": None}
            )  # Retorna sem imagem após 7 segundos
        else:
            return on_complete(None, image_url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/image/<path:filename>")
def download_file(filename):
    return send_from_directory(IMAGE_DIR, filename, as_attachment=False)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
