import socket
import json
import time

def send_inference_request(host, port, payload):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        
        request = {
            'type': 'INFERENCE_REQUEST',
            'data': payload
        }
        
        start_time = time.time()
        client.send(json.dumps(request).encode())
        
        response = client.recv(2048)
        elapsed_time = (time.time() - start_time) * 1000
        
        print(f"\n--- RESPUESTA DEL SISTEMA DISTRIBUIDO ---")
        print(f"Resultado: {json.loads(response.decode())}")
        print(f"Tiempo de respuesta: {elapsed_time:.2f} ms")
        client.close()
    except Exception as e:
        print(f"Error al conectar con el nodo: {e}")

if __name__ == '__main__':
    print("Enviando petición de prueba a AuraGrid (Nodo Líder Port 8001)...")
    send_inference_request('127.0.0.1', 8001, "Frame_Camara_Diagonal_34")