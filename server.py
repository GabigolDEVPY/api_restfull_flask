from flask import Flask, request, jsonify
import json


app = Flask(__name__)

dados = list()

# retornar todos
@app.route("/todos", methods=["GET"])
def rotornar_todos():
    return jsonify(dados)

@app.route("/<int:id>", methods=["GET"])
def rotornar_um(id):
    if dados == []:
        return jsonify("LISTA VAZIA")
    for dado in dados:
        if dado["id"] == id:
            return jsonify(dado)


# retornar um usuário
@app.route("/adicionar", methods=["POST"])
def adicionar():
    dado_novo = request.get_json()
    dados.append(dado_novo)
    return jsonify("Usuário cadastrado com sucesso")


# editar usuário
@app.route("/editar/<int:id>", methods=["PUT"])
def rotornar_todo(id):
    dado_alterado = request.get_json()
    for dado in dados:
        if dado["id"] == id:
            dado.update(dado_alterado)
            return jsonify("Usuário alterado com sucesso")
        
        
@app.route("/excluir/<int:id>", methods=["DELETE"])
def excluir_user(id):
    for dado in dados:
        if dado["id"] == id:
            dados.remove(dado)
            return jsonify("Usuário deletado com sucesso")








if __name__ == "__main__":
    app.run(port=5000, host="localhost", debug=True)    