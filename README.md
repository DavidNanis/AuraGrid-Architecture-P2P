# AuraGrid: Framework Distribuido de Consenso Peer-to-Peer para Edge-AI

AuraGrid es un prototipo de arquitectura distribuida diseñado en Python (`asyncio`, `sockets`, `ThreadPoolExecutor`) para validar la consistencia de inferencias de Inteligencia Artificial ejecutadas en dispositivos de borde (*Edge Computing*).

## 🚀 Arquitectura y Componentes
- **Patrones de Diseño:** Proxy (comunicación sockets), Mediator (gestión de consenso), Observer (notificación de votos).
- **Consenso Distribuido:** Algoritmo de mayoría calificada (>50% de votos).
- **Concurrencia:** Procesamiento multi-hilo para evitar el bloqueo del bucle de eventos asíncrono.

## 🛠️ Ejecución del Proyecto

1. **Crear entorno virtual e instalar dependencias:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt