from flask import jsonify
from . import home_bp

@home_bp.route('/home', methods=['GET'])
def home():
    return jsonify({"message": "Bienvenido a la API"})
