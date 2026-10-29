import asyncio
import json
import socket
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

class AuraNode:
    def __init__(self, node_id, host, port, peers):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.peers = peers  # Lista de tuplas (host, port) de otros nodos
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.is_running = True

    async def start_server(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"[{self.node_id}] Nodo iniciado en {self.host}:{self.port}")
        async with server:
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        data = await reader.read(2048)
        message = json.loads(data.decode())
        
        if message['type'] == 'INFERENCE_REQUEST':
            print(f"[{self.node_id}] Petición de inferencia recibida de cliente.")
            response = await self.process_and_consensus(message['data'])
            writer.write(json.dumps(response).encode())
            await writer.drain()
        
        elif message['type'] == 'VOTE_REQUEST':
            vote = self.evaluate_inference(message['data'])
            writer.write(json.dumps({'vote': vote, 'node_id': self.node_id}).encode())
            await writer.drain()

        writer.close()

    def heavy_ai_inference(self, data_input):
        # Simulación de carga computacional de IA (Edge-AI)
        time.sleep(0.5) 
        result = sum(ord(c) for c in str(data_input)) % 100
        return result

    async def process_and_consensus(self, data_input):
        loop = asyncio.get_event_loop()
        # Procesamiento local en hilo secundario (Pattern Offloading)
        local_result = await loop.run_in_executor(self.executor, self.heavy_ai_inference, data_input)
        print(f"[{self.node_id}] Inferencia local completada: {local_result}")

        # Solicitar votos a los pares (Consenso Distribuido)
        votes = [local_result]
        for peer_host, peer_port in self.peers:
            try:
                reader, writer = await asyncio.open_connection(peer_host, peer_port)
                req = json.dumps({'type': 'VOTE_REQUEST', 'data': data_input})
                writer.write(req.encode())
                await writer.drain()
                
                resp = await reader.read(1024)
                vote_data = json.loads(resp.decode())
                votes.append(vote_data['vote'])
                writer.close()
            except Exception as e:
                print(f"[{self.node_id}] No se pudo contactar al nodo en {peer_port}: {e}")

        # Evaluación de Mayoría (Consenso)
        consensus_value = max(set(votes), key=votes.count)
        approved = votes.count(consensus_value) > (len(votes) / 2)

        return {
            'status': 'APPROVED' if approved else 'REJECTED',
            'consensus_value': consensus_value,
            'total_votes': len(votes),
            'node_id': self.node_id
        }

    def evaluate_inference(self, data_input):
        return self.heavy_ai_inference(data_input)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Uso: python node.py <node_id> <port> <peer_ports_separated_by_comma>")
        sys.exit(1)

    node_id = sys.argv[1]
    port = int(sys.argv[2])
    peer_ports = [int(p) for p in sys.argv[3].split(',')] if sys.argv[3] != 'none' else []
    peers = [('127.0.0.1', p) for p in peer_ports]

    node = AuraNode(node_id, '127.0.0.1', port, peers)
    asyncio.run(node.start_server())