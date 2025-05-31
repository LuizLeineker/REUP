from flask import Flask, request, jsonify
import mysql.connector
from config import MYSQL_CONFIG

app = Flask(__name__)

def conectar_banco():
    return mysql.connector.connect(**MYSQL_CONFIG)

@app.route("/", methods=['GET'])
def index():
    return "Olá mundo"

# CREATE
@app.route("/create-produto", methods=["POST"])
def inserir_produto():
    dados = request.json

    id = dados.get("id")
    modelo = dados.get("modelo")
    tamanho = dados.get("tamanho")
    marca = dados.get("marca")

    if not id or not modelo or not tamanho or not marca:
        return jsonify({"erro": "Todos os campos são obrigatórios!"}), 400

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        sql = "INSERT INTO produtos (id, modelo, tamanho, marca) VALUES (%s, %s, %s, %s)"
        valores = (id, modelo, tamanho, marca)

        cursor.execute(sql, valores)
        conexao.commit()

        return jsonify({"mensagem": "Produto inserido com sucesso!"}), 201

    except mysql.connector.Error as erro:
        return jsonify({"erro": str(erro)}), 500

    finally:
        cursor.close()
        conexao.close()

# READ
@app.route("/produtos", methods=["GET"])
def listar_produtos():
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        sql = "SELECT * FROM produtos"
        cursor.execute(sql)
        resultados = cursor.fetchall()

        produtos = []
        for linha in resultados:
            produto = {
                "id": linha[0],
                "modelo": linha[1],
                "tamanho": linha[2],
                "marca": linha[3]
            }
            produtos.append(produto)

        return jsonify(produtos)

    except mysql.connector.Error as erro:
        return jsonify({"erro": str(erro)}), 500

    finally:
        cursor.close()
        conexao.close()


# SEARCH
@app.route("/search/produto/<id>", methods=["GET"])
def buscar_produto(id):
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        sql = "SELECT * FROM produtos WHERE id = %s"
        cursor.execute(sql, (id,))
        resultado = cursor.fetchone()

        if resultado:
            produto = {
                "id": resultado[0],
                "modelo": resultado[1],
                "tamanho": resultado[2],
                "marca": resultado[3]
            }
            return jsonify(produto)
        else:
            return jsonify({"mensagem": "Produto não encontrado"}), 404

    except mysql.connector.Error as erro:
        return jsonify({"erro": str(erro)}), 500

    finally:
        cursor.close()
        conexao.close()

#DELETE
@app.route("/delete/produto/<id>", methods=["DELETE"])
def remover_produto(id):
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        sql = "DELETE FROM produtos WHERE id = %s"
        cursor.execute(sql, (id,))
        conexao.commit()

        if cursor.rowcount == 0:
            return jsonify({"mensagem": "Produto não encontrado"}), 404

        return jsonify({"mensagem": "Produto removido com sucesso!"}), 200

    except mysql.connector.Error as erro:
        return jsonify({"erro": str(erro)}), 500

    finally:
        cursor.close()
        conexao.close()



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
