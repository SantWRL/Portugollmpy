import sys
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

# Adiciona o diretorio src ao path para importar modulos
sys.path.append(str(Path(__file__).parent.parent))

from inferencia import carregar_modelo, traduzir_com_beam
from interpretador import InterpretadorPortugol
from config import CAMINHO_MODELO_BEST, CAMINHO_MODELO

app = Flask(__name__)
CORS(app)

# Estado global do interpretador (para manter variaveis entre chamadas)
interpretador = InterpretadorPortugol()
modelo_data = {"modelo": None, "vocab_pt": None, "vocab_portugol": None}

def init_model():
    caminho = CAMINHO_MODELO_BEST if CAMINHO_MODELO_BEST.exists() else CAMINHO_MODELO
    if not caminho.exists():
        return False
    
    try:
        m, v_pt, v_pg = carregar_modelo(caminho)
        modelo_data["modelo"] = m
        modelo_data["vocab_pt"] = v_pt
        modelo_data["vocab_portugol"] = v_pg
        return True
    except Exception as e:
        print(f"Erro ao carregar modelo: {e}")
        return False

@app.route("/traduzir", methods=["POST"])
def traduzir():
    if not modelo_data["modelo"]:
        if not init_model():
            return jsonify({"error": "Modelo nao carregado. Treine a IA primeiro."}), 500
            
    data = request.json
    frase = data.get("frase", "")
    if not frase:
        return jsonify({"error": "Frase vazia"}), 400
        
    portugol = traduzir_com_beam(frase, 
                                modelo_data["modelo"], 
                                modelo_data["vocab_pt"], 
                                modelo_data["vocab_portugol"])
    
    return jsonify({"portugol": portugol})

@app.route("/executar", methods=["POST"])
def executar():
    data = request.json
    codigo = data.get("codigo", "")
    if not codigo:
        return jsonify({"error": "Codigo vazio"}), 400
        
    logs = interpretador.executar(codigo)
    
    return jsonify({
        "logs": logs,
        "variaveis": interpretador.variaveis
    })

@app.route("/reset", methods=["POST"])
def reset():
    global interpretador
    interpretador = InterpretadorPortugol()
    return jsonify({"status": "Interpretador resetado"})

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "modelo_carregado": modelo_data["modelo"] is not None,
        "total_variaveis": len(interpretador.variaveis)
    })

if __name__ == "__main__":
    init_model()
    app.run(port=5000, debug=True)
