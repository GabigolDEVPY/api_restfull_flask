from flask import Flask, request, jsonify
from pyngrok import ngrok
import json
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import sys
import threading
import random


class main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.label = QLabel("OLAAAAAA MUNDO")
        self.central_layout.addWidget(self.label)
        
    def trocar_cor(self, cor):
        self.central_widget.setStyleSheet(f"background-color: {cor};")
        
    def trocar_cor_ramdom(self):
        cores = ["green", "blue", "red", "black", "white"]
        cor = random.choice(cores)
        self.central_widget.setStyleSheet(f"background-color: {cor};")


app = Flask(__name__)

dados = list()

# Retornar todos
@app.route("/cor", methods=["PUT"])
def rotornar_todos():
    cor_app = request.get_json()
    window.trocar_cor((cor_app[0]))
    return jsonify("NOME TROCADO", cor_app)

@app.route("/todos", methods=["GET"])
def rotornar_todoss():
    window.trocar_cor_ramdom()
    return jsonify(dados)

@app.route("/<int:id>", methods=["GET"])
def rotornar_um(id):
    if not dados:
        return jsonify("LISTA VAZIA")
    for dado in dados:
        if dado["id"] == id:
            return jsonify(dado)

# Adicionar usuário
@app.route("/adicionar", methods=["POST"])
def adicionar():
    dado_novo = request.get_json()
    dados.append(dado_novo)
    return jsonify("Usuário cadastrado com sucesso")

# Editar usuário
@app.route("/editar/<int:id>", methods=["PUT"])
def rotornar_todo(id):
    dado_alterado = request.get_json()
    for dado in dados:
        if dado["id"] == id:
            dado.update(dado_alterado)
            return jsonify("Usuário alterado com sucesso")

# Excluir usuário
@app.route("/excluir/<int:id>", methods=["DELETE"])
def excluir_user(id):
    for dado in dados:
        if dado["id"] == id:
            dados.remove(dado)
            return jsonify("Usuário deletado com sucesso")


if __name__ == "__main__":
    # Criar um túnel Ngrok na porta 5000
    public_url = ngrok.connect(5000).public_url
    print(f"🔥 API disponível publicamente em: {public_url}")

    # Iniciar o Flask em uma thread separada
    flask_thread = threading.Thread(target=lambda: app.run(port=5000, host="0.0.0.0", debug=False))

    flask_thread.start()

    # Iniciar a interface gráfica
    app_side = QApplication(sys.argv)
    window = main()
    window.show()
    app_side.exec()
