import numpy as np

# Función de membresía triangular mejorada para evitar división por cero
def trimf(x, a, b, c):
    x = np.array(x, dtype=float)
    # Lado izquierdo
    if a == b:
        izquierda = np.where((x >= a) & (x <= b), 1, 0)
    else:
        izquierda = np.maximum((x - a) / (b - a), 0)
    # Lado derecho
    if b == c:
        derecha = np.where((x >= b) & (x <= c), 1, 0)
    else:
        derecha = np.maximum((c - x) / (c - b), 0)
    return np.minimum(izquierda, derecha)

# Funciones de membresía de los antecedentes
def conexion_baja(x): return trimf(x, 0, 0, 4)
def conexion_media(x): return trimf(x, 2, 5, 8)
def conexion_alta(x): return trimf(x, 6, 10, 10)

def velocidad_baja(x): return trimf(x, 0, 0, 40)
def velocidad_media(x): return trimf(x, 20, 50, 80)
def velocidad_alta(x): return trimf(x, 60, 100, 100)

def wifi_baja(x): return trimf(x, 0, 0, 40)
def wifi_media(x): return trimf(x, 20, 50, 80)
def wifi_alta(x): return trimf(x, 60, 100, 100)

def perdida_paquetes_baja(x): return trimf(x, 0, 0, 20)
def perdida_paquetes_media(x): return trimf(x, 10, 30, 60)
def perdida_paquetes_alta(x): return trimf(x, 40, 100, 100)

def dns_bajo(x): return trimf(x, 0, 0, 2)
def dns_medio(x): return trimf(x, 1, 5, 9)
def dns_alto(x): return trimf(x, 8, 10, 10)

# Reglas: (Etiqueta, función que devuelve el grado de activación)
reglas = [
    ('R1: SI conexion BAJA Y perdida_paquetes ALTA ENTONCES falla_router ALTA', 
     lambda c,p,s,w,d: min(conexion_baja(c), perdida_paquetes_alta(p))),
    ('R2: SI conexion BAJA Y perdida_paquetes MEDIA ENTONCES falla_router MEDIA',
     lambda c,p,s,w,d: min(conexion_baja(c), perdida_paquetes_media(p))),
    ('R3: SI conexion MEDIA Y perdida_paquetes BAJA Y velocidad BAJA ENTONCES falla_cable MEDIA',
     lambda c,p,s,w,d: min(conexion_media(c), perdida_paquetes_baja(p), velocidad_baja(s))),
    ('R4: SI velocidad BAJA Y perdida_paquetes MEDIA ENTONCES congestion ALTA',
     lambda c,p,s,w,d: min(velocidad_baja(s), perdida_paquetes_media(p))),
    ('R5: SI error_dns ALTA ENTONCES problema_dns ALTA',
     lambda c,p,s,w,d: dns_alto(d)),
    ('R6: SI error_dns MEDIA ENTONCES problema_dns MEDIA',
     lambda c,p,s,w,d: dns_medio(d)),
    ('R7: SI wifi BAJA ENTONCES falla_cable MEDIA',
     lambda c,p,s,w,d: wifi_baja(w)),
    ('R8: SI wifi BAJA Y conexion BAJA ENTONCES problema_isp MEDIA',
     lambda c,p,s,w,d: min(wifi_baja(w), conexion_baja(c))),
    ('R9: SI velocidad ALTA Y perdida_paquetes BAJA ENTONCES problema_isp BAJA',
     lambda c,p,s,w,d: min(velocidad_alta(s), perdida_paquetes_baja(p))),
    ('R10: SI conexion BAJA Y velocidad BAJA ENTONCES problema_isp ALTA',
     lambda c,p,s,w,d: min(conexion_baja(c), velocidad_baja(s))),
    ('R11: SI wifi ALTA Y velocidad ALTA ENTONCES congestion BAJA',
     lambda c,p,s,w,d: min(wifi_alta(w), velocidad_alta(s))),
    ('R12: SI perdida_paquetes BAJA Y velocidad BAJA ENTONCES falla_cable ALTA',
     lambda c,p,s,w,d: min(perdida_paquetes_baja(p), velocidad_baja(s))),
]

# Causas consecuentes y recomendaciones
causas = ['falla_router', 'falla_cable', 'problema_isp', 'problema_dns', 'congestion']
recomendaciones = {
    'falla_router': 'Reiniciar o reemplazar el router y revisar su configuración.',
    'falla_cable': 'Inspeccionar y sustituir cables de red dañados.',
    'problema_isp': 'Contactar al ISP para verificar el estado del servicio.',
    'problema_dns': 'Configurar correctamente el DNS o usar servidores alternativos.',
    'congestion': 'Reducir tráfico de red o actualizar el ancho de banda.'
}

# Casos de prueba
casos_prueba = [
    {'conexion': 2, 'perdida_paquetes': 80, 'velocidad': 20, 'wifi': 30, 'error_dns': 2},
    {'conexion': 8, 'perdida_paquetes': 10, 'velocidad': 80, 'wifi': 90, 'error_dns': 0},
    {'conexion': 5, 'perdida_paquetes': 30, 'velocidad': 40, 'wifi': 50, 'error_dns': 5},
    {'conexion': 6, 'perdida_paquetes': 20, 'velocidad': 10, 'wifi': 20, 'error_dns': 8},
    {'conexion': 1, 'perdida_paquetes': 10, 'velocidad': 90, 'wifi': 70, 'error_dns': 1},
]

# Ejecutar inferencia para cada caso de prueba
for idx, caso in enumerate(casos_prueba, 1):
    c, p, s, w, d = caso['conexion'], caso['perdida_paquetes'], caso['velocidad'], caso['wifi'], caso['error_dns']
    
    # Calcular activaciones de reglas
    activaciones = [(etiqueta, func(c,p,s,w,d)) for etiqueta, func in reglas if func(c,p,s,w,d) > 0]
    
    # Agregar grados de causa
    grados_causa = {causa: 0 for causa in causas}
    for etiqueta, act in activaciones:
        for causa_actual in causas: # Renombrado para evitar conflicto con la variable 'causas' global
            if causa_actual in etiqueta:
                grados_causa[causa_actual] = max(grados_causa[causa_actual], act)
    
    # Defuzzificación (salida nítida = grado máximo)
    diagnostico = max(grados_causa, key=grados_causa.get)
    
    # Mostrar resultados
    print(f"\n--- CASO DE PRUEBA {idx} ---")
    print("Valores de entrada:", caso)
    print("Reglas activadas y sus grados de activación:")
    for etiqueta, grado in activaciones:
        print(f"  {etiqueta} → grado de activación: {grado:.2f}")
    print("Grados de pertenencia para cada causa posible:", grados_causa)
    print("Diagnóstico (causa con mayor grado de pertenencia):", diagnostico)
    print("Recomendación para el diagnóstico:", recomendaciones[diagnostico])
