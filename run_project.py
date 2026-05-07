import os
import subprocess
import sys
import time
import threading
import requests  # Adicionado para check de saude da API

def run_command(command, cwd=None, name=""):
    print(f"[EXECUTANDO] {name}: {command}")
    # Usando subprocess.PIPE para capturar erros se necessario, mas mantendo o log no terminal
    process = subprocess.Popen(command, shell=True, cwd=cwd)
    return process

def check_api_ready(url, timeout=30):
    """Aguarda a API estar pronta antes de seguir."""
    start_time = time.time()
    print(f"Aguardando API em {url}...")
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{url}/status")
            if response.status_code == 200:
                print("✅ API Online!")
                return True
        except:
            pass
        time.sleep(1)
    return False

def main():
    print("🌿 Tupi-Logic: Gerenciador do Projeto\n")
    
    # Check de dependencias basicas
    try:
        subprocess.run(["npm", "--version"], capture_output=True, shell=True, check=True)
    except:
        print("❌ ERRO: Node.js/npm nao encontrado! O Web UI nao podera ser iniciado.")
        print("Instale o Node.js em: https://nodejs.org/")
        sys.exit(1)

    # 1. Gerar Dataset
    if not os.path.exists("dataset/dados.json"):
        print("1/4 Gerando dataset inicial...")
        subprocess.run([sys.executable, "src/gerar_dataset.py"], check=True)
    else:
        print("1/4 Dataset ja existe. Pulando geracao.")
    
    # 2. Treinar (opcional)
    if os.path.exists("modelos_salvos/tupi_melhor.pth"):
        print("2/4 Modelo ja existe.")
        res = input("   Deseja treinar novamente para melhorar a precisao? (s/N): ")
        if res.lower() == 's':
            subprocess.run([sys.executable, "src/treinar.py"], check=True)
    else:
        print("2/4 Iniciando treinamento obrigatorio...")
        subprocess.run([sys.executable, "src/treinar.py"], check=True)
    
    print("\n3/4 Iniciando Backend API (Flask)...")
    backend = run_command(f"{sys.executable} src/api/app.py", name="Backend")
    
    # Aguarda a API subir antes de tentar rodar o front
    if not check_api_ready("http://localhost:5000"):
        print("❌ ERRO: O Backend demorou muito para iniciar.")
        backend.terminate()
        sys.exit(1)
    
    print("\n4/4 Iniciando Frontend (Vite)...")
    if not os.path.exists("web-ui/node_modules"):
        print("Instalando dependencias do frontend (primeira execucao)...")
        subprocess.run("npm install", shell=True, cwd="web-ui", check=True)
    
    frontend = run_command("npm run dev", cwd="web-ui", name="Frontend")
    
    print("\n" + "="*50)
    print("🚀 TUDO PRONTO E RODANDO!")
    print(f"🔗 API: http://localhost:5000")
    print(f"🔗 Web UI: http://localhost:5173")
    print("="*50)
    print("\nPressione Ctrl+C para encerrar todos os processos.\n")
    
    try:
        while True:
            # Verifica se os processos ainda estao vivos
            if backend.poll() is not None:
                print("⚠️ Backend parou inesperadamente!")
                break
            if frontend.poll() is not None:
                print("⚠️ Frontend parou inesperadamente!")
                break
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nEncerrando processos...")
    finally:
        backend.terminate()
        frontend.terminate()
        print("Até logo!")

if __name__ == "__main__":
    main()
