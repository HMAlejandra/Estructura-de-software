import tkinter as tk
import math
import time

#  LISTAS CIRCULARES DOBLES

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
            ultimo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = ultimo
            nuevo_nodo.siguiente = self.actual
            self.actual.anterior = nuevo_nodo
        
        self.tamanio += 1
    
    def avanzar(self):
        """Avanza al siguiente nodo en la lista circular"""
        if self.actual is not None:
            self.actual = self.actual.siguiente
            return True
        return False
    
    def retroceder(self):
        """Retrocede al nodo anterior en la lista circular"""
        if self.actual is not None:
            self.actual = self.actual.anterior
            return True
        return False
    
    def obtener_valor_actual(self):
        """Obtiene el valor del nodo actual"""
        if self.actual is not None:
            return self.actual.valor
        return None
    
    def establecer_valor(self, valor):
        """Establece el nodo actual según un valor específico"""
        if self.actual is None:
            return False
        
        nodo_inicio = self.actual
        while True:
            if self.actual.valor == valor:
                return True
            self.avanzar()
            if self.actual == nodo_inicio:
                break
        return False

class RelojBackend:
    """Backend del reloj usando listas circulares dobles"""
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
        
        # Inicializar con la hora actual del sistema
        self.sincronizar_con_sistema()
    
    def sincronizar_con_sistema(self):
        """Sincroniza el reloj con la hora actual del sistema"""
        tiempo_actual = time.localtime()
        hora_12 = tiempo_actual.tm_hour % 12
        if hora_12 == 0:
            hora_12 = 12
        
        self.horas.establecer_valor(hora_12)
        self.minutos.establecer_valor(tiempo_actual.tm_min)
        self.segundos.establecer_valor(tiempo_actual.tm_sec)
    
    def avanzar_segundo(self):
        """Avanza un segundo y actualiza minutos/horas si es necesario"""
        self.segundos.avanzar()
        
        # Si los segundos vuelven a 0, avanzar minuto
        if self.segundos.obtener_valor_actual() == 0:
            self.minutos.avanzar()
            
            # Si los minutos vuelven a 0, avanzar hora
            if self.minutos.obtener_valor_actual() == 0:
                self.horas.avanzar()
    
    def obtener_tiempo(self):
        """Retorna el tiempo actual como tupla (horas, minutos, segundos)"""
        return (
            self.horas.obtener_valor_actual(),
            self.minutos.obtener_valor_actual(),
            self.segundos.obtener_valor_actual()
        )
    
    def establecer_tiempo(self, horas, minutos, segundos):
        """Establece manualmente el tiempo del reloj"""
        if 1 <= horas <= 12:
            self.horas.establecer_valor(horas)
        if 0 <= minutos <= 59:
            self.minutos.establecer_valor(minutos)
        if 0 <= segundos <= 59:
            self.segundos.establecer_valor(segundos)

#  FRONTEND: INTERFAZ GRÁFICA 

class RelojAnalogico:
    """Frontend del reloj analógico con tkinter"""
    def __init__(self, root):
        self.root = root
        self.root.title("CLOCK")
        self.root.configure(bg='#f0f0f0')
        
        # Backend del reloj
        self.reloj = RelojBackend()
        
        # Configuración del canvas
        self.canvas_size = 400
        self.center_x = self.canvas_size // 2
        self.center_y = self.canvas_size // 2
        self.radio = 150
        
        # Crear canvas
        self.canvas = tk.Canvas(
            root, 
            width=self.canvas_size, 
            height=self.canvas_size,
            bg='white',
            highlightthickness=2,
            highlightbackground='#ff69b4'
        )
        self.canvas.pack(padx=20, pady=20)
        
        # Frame para controles
        control_frame = tk.Frame(root, bg='#f0f0f0')
        control_frame.pack(pady=10)
        
        # Etiqueta digital
        self.label_digital = tk.Label(
            control_frame,
            text="",
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg='#ff69b4'
        )
        self.label_digital.pack(pady=5)
        
        # Botones de control
        btn_frame = tk.Frame(control_frame, bg='#f0f0f0')
        btn_frame.pack(pady=5)
        
        tk.Button(
            btn_frame,
            text="Sincronizar con Sistema",
            command=self.sincronizar,
            bg='#ff69b4',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Ajustar Hora",
            command=self.abrir_ajuste,
            bg='#ff69b4',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        # Dibujar el reloj
        self.dibujar_reloj_base()
        self.actualizar_reloj()
    
    def dibujar_reloj_base(self):
        """Dibuja la base del reloj (círculo y números)"""
        # Círculo exterior (rosado)
        self.canvas.create_oval(
            self.center_x - self.radio - 10,
            self.center_y - self.radio - 10,
            self.center_x + self.radio + 10,
            self.center_y + self.radio + 10,
            fill='#ffb6d9',
            outline='#ff69b4',
            width=3
        )
        
        # Círculo interior (blanco)
        self.canvas.create_oval(
            self.center_x - self.radio,
            self.center_y - self.radio,
            self.center_x + self.radio,
            self.center_y + self.radio,
            fill='white',
            outline='#ff69b4',
            width=2
        )
        
        # Dibujar números de las horas
        for i in range(1, 13):
            angulo = math.radians(90 - (i * 30))
            x = self.center_x + (self.radio - 30) * math.cos(angulo)
            y = self.center_y - (self.radio - 30) * math.sin(angulo)
            self.canvas.create_text(
                x, y,
                text=str(i),
                font=('Arial', 16, 'bold'),
                fill='#333333'
            )
        
        # Dibujar marcas de minutos
        for i in range(60):
            angulo = math.radians(90 - (i * 6))
            if i % 5 == 0:
                # Marcas más grandes para las horas
                r1 = self.radio - 15
                r2 = self.radio - 5
                width = 3
            else:
                # Marcas pequeñas para los minutos
                r1 = self.radio - 10
                r2 = self.radio - 5
                width = 1
            
            x1 = self.center_x + r1 * math.cos(angulo)
            y1 = self.center_y - r1 * math.sin(angulo)
            x2 = self.center_x + r2 * math.cos(angulo)
            y2 = self.center_y - r2 * math.sin(angulo)
            
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill='#666666',
                width=width
            )
        
        # Centro del reloj
        self.canvas.create_oval(
            self.center_x - 8,
            self.center_y - 8,
            self.center_x + 8,
            self.center_y + 8,
            fill='#ff69b4',
            outline='#ff1493',
            width=2
        )
    
    def dibujar_manecilla(self, angulo, longitud, ancho, color, tag):
        """Dibuja una manecilla del reloj"""
        angulo_rad = math.radians(90 - angulo)
        x = self.center_x + longitud * math.cos(angulo_rad)
        y = self.center_y - longitud * math.sin(angulo_rad)
        
        self.canvas.create_line(
            self.center_x, self.center_y,
            x, y,
            fill=color,
            width=ancho,
            capstyle=tk.ROUND,
            tags=tag
        )
    
    def actualizar_reloj(self):
        """Actualiza la visualización del reloj"""
        # Obtener tiempo actual
        horas, minutos, segundos = self.reloj.obtener_tiempo()
        
        # Borrar manecillas anteriores
        self.canvas.delete('manecilla')
        
        # Calcular ángulos
        angulo_segundos = segundos * 6  # 360/60 = 6 grados por segundo
        angulo_minutos = minutos * 6 + (segundos * 0.1)  # Movimiento suave
        angulo_horas = (horas % 12) * 30 + (minutos * 0.5)  # 360/12 = 30 grados por hora
        
        # Dibujar manecillas (de atrás hacia adelante)
        # Manecilla de horas (corta y gruesa)
        self.dibujar_manecilla(angulo_horas, self.radio * 0.5, 8, '#333333', 'manecilla')
        
        # Manecilla de minutos (mediana)
        self.dibujar_manecilla(angulo_minutos, self.radio * 0.7, 6, '#666666', 'manecilla')
        
        # Manecilla de segundos (larga y delgada)
        self.dibujar_manecilla(angulo_segundos, self.radio * 0.8, 2, '#ff69b4', 'manecilla')
        
        # Actualizar etiqueta digital
        self.label_digital.config(
            text=f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        )
        
        # Avanzar un segundo en el backend
        self.reloj.avanzar_segundo()
        
        # Programar siguiente actualización (1000ms = 1 segundo)
        self.root.after(1000, self.actualizar_reloj)
    
    def sincronizar(self):
        """Sincroniza el reloj con la hora del sistema"""
        self.reloj.sincronizar_con_sistema()
    
    def abrir_ajuste(self):
        """Abre ventana para ajustar la hora manualmente"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Ajustar Hora")
        ventana.configure(bg='#f0f0f0')
        ventana.geometry("300x200")
        
        # Obtener tiempo actual
        horas, minutos, segundos = self.reloj.obtener_tiempo()
        
        # Frame para los spinboxes
        frame = tk.Frame(ventana, bg='#f0f0f0')
        frame.pack(pady=20)
        
        tk.Label(frame, text="Horas:", bg='#f0f0f0', font=('Arial', 12)).grid(row=0, column=0, padx=5, pady=5)
        spin_horas = tk.Spinbox(frame, from_=1, to=12, width=5, font=('Arial', 12))
        spin_horas.delete(0, tk.END)
        spin_horas.insert(0, horas)
        spin_horas.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Minutos:", bg='#f0f0f0', font=('Arial', 12)).grid(row=1, column=0, padx=5, pady=5)
        spin_minutos = tk.Spinbox(frame, from_=0, to=59, width=5, font=('Arial', 12))
        spin_minutos.delete(0, tk.END)
        spin_minutos.insert(0, minutos)
        spin_minutos.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Segundos:", bg='#f0f0f0', font=('Arial', 12)).grid(row=2, column=0, padx=5, pady=5)
        spin_segundos = tk.Spinbox(frame, from_=0, to=59, width=5, font=('Arial', 12))
        spin_segundos.delete(0, tk.END)
        spin_segundos.insert(0, segundos)
        spin_segundos.grid(row=2, column=1, padx=5, pady=5)
        
        def aplicar():
            h = int(spin_horas.get())
            m = int(spin_minutos.get())
            s = int(spin_segundos.get())
            self.reloj.establecer_tiempo(h, m, s)
            ventana.destroy()
        
        tk.Button(
            ventana,
            text="Aplicar",
            command=aplicar,
            bg='#ff69b4',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=5
        ).pack(pady=10)

# ==================== EJECUCIÓN PRINCIPAL ====================

if __name__ == "__main__":
    root = tk.Tk()
    app = RelojAnalogico(root)
    root.mainloop()
