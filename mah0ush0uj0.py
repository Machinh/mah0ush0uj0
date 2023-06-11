import http.server
import socketserver
import webbrowser
import threading
import signal
import sys

# Define o diretório raiz onde o arquivo index.html está localizado
diretorio_raiz = './'

# Define a porta em que o servidor irá ouvir
porta = 9999

# Cria uma classe de manipulador que redireciona para o arquivo index.html
class MeuManipulador(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Define o cabeçalho de redirecionamento para o arquivo index.html
            self.send_response(302)
            self.send_header('Location', '/index.html')
            self.end_headers()
        else:
            # Serve os arquivos do diretório raiz
            super().do_GET()

# Cria o servidor usando o manipulador personalizado
httpd = socketserver.TCPServer(("", porta), MeuManipulador)

print(f"Servidor rodando em http://localhost:{porta}")

# Abre o navegador padrão com a URL do servidor local
url_local = f"http://localhost:{porta}"
webbrowser.open(url_local)

# Variável de controle para o loop de encerramento
encerrar = False

def encerrar_servidor(signal, frame):
    global encerrar
    print("Encerrando servidor...")
    encerrar = True
    httpd.shutdown()
    httpd.server_close()

signal.signal(signal.SIGINT, encerrar_servidor)

def aguardar_encerramento():
    global encerrar
    while not encerrar:
        pass
    sys.exit(0)

# Inicia uma thread para aguardar o encerramento do servidor
thread_encerramento = threading.Thread(target=aguardar_encerramento)
thread_encerramento.start()

try:
    # Inicia o servidor
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
