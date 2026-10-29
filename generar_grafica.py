import matplotlib.pyplot as plt

# Datos de prueba para la gráfica
nodos = ['1 Nodo (Local)', '2 Nodos (P2P)', '3 Nodos (Consenso completo)']
latencia_ms = [510, 1020, 1510]

# Crear la gráfica
plt.figure(figsize=(7, 4))
plt.bar(nodos, latencia_ms, color=['#0284c7', '#2563eb', '#059669'])
plt.title('Latencia Promedio según Tamaño de la Red AuraGrid')
plt.xlabel('Configuración de Red')
plt.ylabel('Tiempo de Respuesta (ms)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Guardar la imagen en la carpeta diagrams
plt.savefig('diagrams/latencia_auragrid.png')
print("¡Gráfica guardada exitosamente en diagrams/latencia_auragrid.png!")

# Mostrar la gráfica en pantalla
plt.show()