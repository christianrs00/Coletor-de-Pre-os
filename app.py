from flask import (
    Flask,
    render_template,
    request
) 
from database.banco import buscar_produto_web
from servicos.coletor import atualizar_produto
from database.banco import historico_grafico
from database.banco import melhores_ofertas_loja


app = Flask(__name__)

@app.route("/")

def inicio():
    return render_template("index.html")

@app.route("/buscar", methods=["POST"])
def buscar():

    produto = request.form["produto"]

    atualizar_produto(produto)

    resultados = buscar_produto_web(produto)

    historico = historico_grafico(produto)

    ofertas_loja = melhores_ofertas_loja(produto)

    economia = 0

    if len(ofertas_loja) > 1:
        print(ofertas_loja)

        melhor_preco = float (ofertas_loja[0][1] or 0)
        segundo_preco = float (ofertas_loja[1][1] or 0)

        economia = round(
            segundo_preco - melhor_preco,
            2
        )

    return render_template(
        "resultados.html",
        produto=produto,
        resultados=resultados,
        historico=historico,
        ofertas_loja = ofertas_loja,
        economia = economia,
        encontrou=len(resultados) > 0
    )


if __name__ == "__main__":
    app.run(
        debug=True
    )