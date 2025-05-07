import numpy as np

# Improved triangular membership to avoid division by zero
def trimf(x, a, b, c):
    x = np.array(x, dtype=float)
    # Left side
    if a == b:
        left = np.where((x >= a) & (x <= b), 1, 0)
    else:
        left = np.maximum((x - a) / (b - a), 0)
    # Right side
    if b == c:
        right = np.where((x >= b) & (x <= c), 1, 0)
    else:
        right = np.maximum((c - x) / (c - b), 0)
    return np.minimum(left, right)

# Antecedent membership functions
def connection_low(x): return trimf(x, 0, 0, 4)
def connection_med(x): return trimf(x, 2, 5, 8)
def connection_high(x): return trimf(x, 6, 10, 10)

def speed_low(x): return trimf(x, 0, 0, 40)
def speed_med(x): return trimf(x, 20, 50, 80)
def speed_high(x): return trimf(x, 60, 100, 100)

def wifi_low(x): return trimf(x, 0, 0, 40)
def wifi_med(x): return trimf(x, 20, 50, 80)
def wifi_high(x): return trimf(x, 60, 100, 100)

def packet_loss_low(x): return trimf(x, 0, 0, 20)
def packet_loss_med(x): return trimf(x, 10, 30, 60)
def packet_loss_high(x): return trimf(x, 40, 100, 100)

def dns_low(x): return trimf(x, 0, 0, 2)
def dns_med(x): return trimf(x, 1, 5, 9)
def dns_high(x): return trimf(x, 8, 10, 10)

# Rules: (Label, function returning activation degree)
rules = [
    ('R1: SI connection BAJA Y packet_loss ALTA ENTONCES router_fault ALTA', 
     lambda c,p,s,w,d: min(connection_low(c), packet_loss_high(p))),
    ('R2: SI connection BAJA Y packet_loss MEDIO ENTONCES router_fault MEDIO',
     lambda c,p,s,w,d: min(connection_low(c), packet_loss_med(p))),
    ('R3: SI connection MEDIA Y packet_loss BAJA Y speed BAJA ENTONCES cable_fault MEDIO',
     lambda c,p,s,w,d: min(connection_med(c), packet_loss_low(p), speed_low(s))),
    ('R4: SI speed BAJA Y packet_loss MEDIO ENTONCES congestion ALTA',
     lambda c,p,s,w,d: min(speed_low(s), packet_loss_med(p))),
    ('R5: SI dns_error ALTA ENTONCES dns_issue ALTA',
     lambda c,p,s,w,d: dns_high(d)),
    ('R6: SI dns_error MEDIO ENTONCES dns_issue MEDIO',
     lambda c,p,s,w,d: dns_med(d)),
    ('R7: SI wifi BAJA ENTONCES cable_fault MEDIO',
     lambda c,p,s,w,d: wifi_low(w)),
    ('R8: SI wifi BAJA Y connection BAJA ENTONCES isp_issue MEDIO',
     lambda c,p,s,w,d: min(wifi_low(w), connection_low(c))),
    ('R9: SI speed ALTA Y packet_loss BAJA ENTONCES isp_issue BAJA',
     lambda c,p,s,w,d: min(speed_high(s), packet_loss_low(p))),
    ('R10: SI connection BAJA Y speed BAJA ENTONCES isp_issue ALTA',
     lambda c,p,s,w,d: min(connection_low(c), speed_low(s))),
    ('R11: SI wifi ALTA Y speed ALTA ENTONCES congestion BAJA',
     lambda c,p,s,w,d: min(wifi_high(w), speed_high(s))),
    ('R12: SI packet_loss BAJA Y speed BAJA ENTONCES cable_fault ALTA',
     lambda c,p,s,w,d: min(packet_loss_low(p), speed_low(s))),
]

# Consequent causes and recommendations
causes = ['router_fault', 'cable_fault', 'isp_issue', 'dns_issue', 'congestion']
recommendations = {
    'router_fault': 'Reiniciar o reemplazar el router y revisar su configuración.',
    'cable_fault': 'Inspeccionar y sustituir cables de red dañados.',
    'isp_issue': 'Contactar al ISP para verificar el estado del servicio.',
    'dns_issue': 'Configurar correctamente el DNS o usar servidores alternativos.',
    'congestion': 'Reducir tráfico de red o actualizar el ancho de banda.'
}

# Test cases
test_cases = [
    {'connection': 2, 'packet_loss': 80, 'speed': 20, 'wifi': 30, 'dns_error': 2},
    {'connection': 8, 'packet_loss': 10, 'speed': 80, 'wifi': 90, 'dns_error': 0},
    {'connection': 5, 'packet_loss': 30, 'speed': 40, 'wifi': 50, 'dns_error': 5},
    {'connection': 6, 'packet_loss': 20, 'speed': 10, 'wifi': 20, 'dns_error': 8},
    {'connection': 1, 'packet_loss': 10, 'speed': 90, 'wifi': 70, 'dns_error': 1},
]

# Run inference for each test case
for idx, case in enumerate(test_cases, 1):
    c, p, s, w, d = case['connection'], case['packet_loss'], case['speed'], case['wifi'], case['dns_error']
    
    # Compute rule activations
    activations = [(label, func(c,p,s,w,d)) for label, func in rules if func(c,p,s,w,d) > 0]
    
    # Aggregate cause degrees
    cause_degrees = {cause: 0 for cause in causes}
    for label, act in activations:
        for cause in causes:
            if cause in label:
                cause_degrees[cause] = max(cause_degrees[cause], act)
    
    # Defuzzification (crisp output = max degree)
    diagnosis = max(cause_degrees, key=cause_degrees.get)
    
    # Display results
    print(f"\n--- CASO DE PRUEBA {idx} ---")
    print("Valores de entrada:", case)
    print("Reglas activadas y sus grados de activación:")
    for label, degree in activations:
        print(f"  {label} → grado de activación: {degree:.2f}")
    print("Grados de pertenencia para cada causa posible:", cause_degrees)
    print("Diagnóstico (causa con mayor grado de pertenencia):", diagnosis)
    print("Recomendación para el diagnóstico:", recommendations[diagnosis])
