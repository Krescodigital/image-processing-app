import os
import http.server
import socketserver
import uuid  # Agregar esta importación al inicio del archivo
from PIL import Image  # Agregar esta importación al inicio
import io
from clean_ticket import clean_ticket

from http import HTTPStatus
from flask import Flask, request, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/img/<filename>')
def get_image(filename):
    return send_from_directory('tmp/output', filename)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No se ha proporcionado ninguna imagen', 400
    
    file = request.files['image']
    if file.filename == '':
        return 'No se ha seleccionado ningún archivo', 400
    
    # Generar ID único con extensión .jpg
    filename = f"{str(uuid.uuid4())}.jpg"
    
    # Asegurarse de que existe el directorio
    os.makedirs('tmp/output', exist_ok=True)
    
    # Convertir y guardar como JPG
    image = Image.open(file)
    image = clean_ticket(image)

    if image.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[-1])
        image = background
    
    file_path = os.path.join('tmp/output', filename)
    image.save(file_path, 'JPEG', quality=85)
    
    return {'status': 'success', 'img_endpoint': f'http://127.0.0.1:8000/img/{filename}'}, 200



'''
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        msg = 'Hello! you requested %s' % (self.path)
        self.wfile.write(msg.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Asegurarse de que existe el directorio
        os.makedirs('tmp/output', exist_ok=True)
        
        # Extraer el nombre del archivo de los headers
        filename = 'image.jpg'  # nombre por defecto si no se proporciona
            
        # Guardar el archivo
        file_path = os.path.join('tmp/output', filename)
        with open(file_path, 'wb') as f:
            f.write(post_data)
        
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'application/octet-stream')
        self.end_headers()
        
        self.wfile.write(b'Imagen guardada exitosamente')
'''

