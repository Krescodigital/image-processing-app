import requests
import os

def test_upload():
    #upload image
    url = 'http://127.0.0.1:8000/upload'
    files = {'image': open('tests/tests_input/ticket 0.jpeg', 'rb')}
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    #get the image from the returned endpoint
    img_endpoint = response.json()['img_endpoint']
    response = requests.get(img_endpoint)
    
    # Asegurarse de que existe el directorio de salida
    os.makedirs('tests/tests_outputs', exist_ok=True)
    
    # Extraer el nombre del archivo del endpoint
    filename = img_endpoint.split('/')[-1]
    
    # Guardar la imagen en tests_outputs
    output_path = os.path.join('tests/tests_outputs', filename)
    with open(output_path, 'wb') as f:
        f.write(response.content)
    
    print(f"Imagen guardada en: {output_path}")

if __name__ == "__main__":
    test_upload() 