import http.server
import socketserver
import json
import time
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# ==================== BACKEND: LISTAS CIRCULARES DOBLES ====================

class Nodo:
    """Nodo para la lista circular doble"""
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None
        self.anterior = None

class ListaCircularDoble:
    """Implementación de lista circular doble"""
    def __init__(self):
        self.actual = None
        self.tamanio = 0
    
    def agregar(self, valor):
        """Agrega un nodo a la lista circular"""
        nuevo_nodo = Nodo(valor)
        
        if self.actual is None:
            # Primera inserción
            nuevo_nodo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = nuevo_nodo
            self.actual = nuevo_nodo
        else:
            # Insertar al final
            ultimo = self.actual.anterior
            nuevo_nodo.siguiente = self.actual
            nuevo_nodo.anterior = ultimo
            ultimo.siguiente = nuevo_nodo
            self.actual.anterior = nuevo_nodo
        
        self.tamanio += 1
    
    def avanzar(self):
        """Avanza al siguiente nodo en la lista circular"""
        if self.actual:
            self.actual = self.actual.siguiente
            return True
        return False
    
    def retroceder(self):
        """Retrocede al nodo anterior en la lista circular"""
        if self.actual:
            self.actual = self.actual.anterior
            return True
        return False
    
    def obtener_valor_actual(self):
        """Obtiene el valor del nodo actual"""
        return self.actual.valor if self.actual else None
    
    def buscar_y_posicionar(self, valor):
        """Busca un valor y posiciona el puntero actual en ese nodo"""
        if not self.actual:
            return False
        
        nodo_inicio = self.actual
        while True:
            if self.actual.valor == valor:
                return True
            self.actual = self.actual.siguiente
            if self.actual == nodo_inicio:
                break
        return False

class RelojCircular:
    """Reloj implementado con listas circulares dobles"""
    def __init__(self):
        # Crear lista circular para horas (1-12)
        self.horas = ListaCircularDoble()
        for i in range(1, 13):
            self.horas.agregar(i)
        
        # Crear lista circular para minutos (0-59)
        self.minutos = ListaCircularDoble()
        for i in range(60):
            self.minutos.agregar(i)
        
        # Crear lista circular para segundos (0-59)
        self.segundos = ListaCircularDoble()
        for i in range(60):
            self.segundos.agregar(i)
        
        # Sincronizar con hora del sistema
        self.sincronizar_con_sistema()
    
    def sincronizar_con_sistema(self):
        """Sincroniza el reloj con la hora del sistema"""
        ahora = datetime.now()
        hora_12 = ahora.hour % 12
        if hora_12 == 0:
            hora_12 = 12
        
        self.horas.buscar_y_posicionar(hora_12)
        self.minutos.buscar_y_posicionar(ahora.minute)
        self.segundos.buscar_y_posicionar(ahora.second)
    
    def avanzar_segundo(self):
        """Avanza un segundo en el reloj"""
        self.segundos.avanzar()
        
        # Si los segundos vuelven a 0, avanzar minutos
        if self.segundos.obtener_valor_actual() == 0:
            self.minutos.avanzar()
            
            # Si los minutos vuelven a 0, avanzar horas
            if self.minutos.obtener_valor_actual() == 0:
                self.horas.avanzar()
    
    def obtener_tiempo(self):
        """Obtiene el tiempo actual del reloj"""
        return {
            'horas': self.horas.obtener_valor_actual(),
            'minutos': self.minutos.obtener_valor_actual(),
            'segundos': self.segundos.obtener_valor_actual()
        }
    
    def ajustar_tiempo(self, horas, minutos, segundos):
        """Ajusta el tiempo del reloj manualmente"""
        if 1 <= horas <= 12:
            self.horas.buscar_y_posicionar(horas)
        if 0 <= minutos <= 59:
            self.minutos.buscar_y_posicionar(minutos)
        if 0 <= segundos <= 59:
            self.segundos.buscar_y_posicionar(segundos)

# ==================== SERVIDOR HTTP ====================

# Instancia global del reloj
reloj = RelojCircular()
ultimo_tick = time.time()

class ManejadorReloj(http.server.SimpleHTTPRequestHandler):
    """Manejador HTTP personalizado para el reloj"""
    
    def do_GET(self):
        global ultimo_tick
        
        # Parsear la URL
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/tiempo':
            # Actualizar el reloj si ha pasado un segundo
            tiempo_actual = time.time()
            if tiempo_actual - ultimo_tick >= 1.0:
                reloj.avanzar_segundo()
                ultimo_tick = tiempo_actual
            
            # Enviar el tiempo actual
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            tiempo = reloj.obtener_tiempo()
            self.wfile.write(json.dumps(tiempo).encode())
        
        elif parsed_path.path == '/api/sincronizar':
            # Sincronizar con la hora del sistema
            reloj.sincronizar_con_sistema()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            tiempo = reloj.obtener_tiempo()
            self.wfile.write(json.dumps(tiempo).encode())
        
        elif parsed_path.path == '/api/ajustar':
            # Ajustar el tiempo manualmente
            params = parse_qs(parsed_path.query)
            horas = int(params.get('horas', [12])[0])
            minutos = int(params.get('minutos', [0])[0])
            segundos = int(params.get('segundos', [0])[0])
            
            reloj.ajustar_tiempo(horas, minutos, segundos)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            tiempo = reloj.obtener_tiempo()
            self.wfile.write(json.dumps(tiempo).encode())
        
        else:
            # Servir archivos estáticos (HTML, CSS, JS)
            super().do_GET()
    
    def log_message(self, format, *args):
        """Sobrescribir para mostrar logs más limpios"""
        print(f"[Servidor] {format % args}")

def iniciar_servidor(puerto=8000):
    """Inicia el servidor HTTP"""
    with socketserver.TCPServer(("", puerto), ManejadorReloj) as httpd:
        print(f"\n{'='*60}")
        print(f"CLOCK")
        print(f"{'='*60}")
        print(f"\n Servidor iniciado en http://localhost:{puerto}")
        print(f" Abre tu navegador y visita: http://localhost:{puerto}")
        print(f"\n El reloj está sincronizado con tu hora del sistema")
        print(f"Presiona Ctrl+C para detener el servidor\n")
        print(f"{'='*60}\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Servidor detenido")

if __name__ == "__main__":
    iniciar_servidor()
