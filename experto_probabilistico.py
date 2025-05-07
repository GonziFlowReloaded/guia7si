# Priori de cada causa (P(C))
priors = {
    'Mantenimiento o fallas del ISP': 0.25,
    'Problemas de DNS en equipos o router': 0.20,
    'Cable de red dañado': 0.10,
    'Señal Wi‑Fi débil en zonas alejadas': 0.15,
    'Congestión o lentitud del servidor interno': 0.30,
}

# Probabilidades condicionales P(Síntoma | Causa)
likelihoods = {
    'Mantenimiento o fallas del ISP': {
        'Sin conexión a Internet': 0.90,
        'Conexión intermitente': 0.70,
        'Lentitud al acceder al servidor interno': 0.30,
        'Mensajes de error DNS': 0.20,
        'Señal Wi‑Fi débil': 0.10,
    },
    'Problemas de DNS en equipos o router': {
        'Sin conexión a Internet': 0.60,
        'Conexión intermitente': 0.40,
        'Lentitud al acceder al servidor interno': 0.50,
        'Mensajes de error DNS': 0.10,
        'Señal Wi‑Fi débil': 0.10,
    },
    'Cable de red dañado': {
        'Sin conexión a Internet': 0.85,
        'Conexión intermitente': 0.80,
        'Lentitud al acceder al servidor interno': 0.60,
        'Mensajes de error DNS': 0.30,
        'Señal Wi‑Fi débil': 0.30,
    },
    'Señal Wi‑Fi débil en zonas alejadas': {
        'Sin conexión a Internet': 0.40,
        'Conexión intermitente': 0.60,
        'Lentitud al acceder al servidor interno': 0.30,
        'Mensajes de error DNS': 0.10,
        'Señal Wi‑Fi débil': 0.85,
    },
    'Congestión o lentitud del servidor interno': {
        'Sin conexión a Internet': 0.50,
        'Conexión intermitente': 0.50,
        'Lentitud al acceder al servidor interno': 0.20,
        'Mensajes de error DNS': 0.90,
        'Señal Wi‑Fi débil': 0.10,
    },
}

# Lista de síntomas
symptoms = [
    'Sin conexión a Internet',
    'Conexión intermitente',
    'Lentitud al acceder al servidor interno',
    'Mensajes de error DNS',
    'Señal Wi‑Fi débil',
]

def diagnosticar(evidencia):
    """
    evidencia: dict con claves iguales a los nombres de los síntomas y valores 1 (presente) o 0 (ausente)
    Devuelve un dict con las probabilidades posteriores normalizadas y ordenadas de mayor a menor.
    """
    posteriors = {}
    # Calcular P(C) * ∏ P(S|C)^e * (1-P(S|C))^(1-e)
    for causa, p_c in priors.items():
        score = p_c
        for sintoma in symptoms:
            p_s_given_c = likelihoods[causa][sintoma]
            if evidencia.get(sintoma, 0):
                score *= p_s_given_c
            else:
                score *= (1 - p_s_given_c)
        posteriors[causa] = score

    # Normalizar para obtener distrib. de probabilidad
    total = sum(posteriors.values())
    for causa in posteriors:
        posteriors[causa] /= total

    # Ordenar de mayor a menor
    return dict(sorted(posteriors.items(), key=lambda item: item[1], reverse=True))


# Acciones sugeridas
acciones = {
    'Mantenimiento o fallas del ISP': 'Contactar al ISP',
    'Problemas de DNS en equipos o router': 'Revisar configuración de DNS en router y equipos',
    'Cable de red dañado': 'Inspeccionar y reemplazar el cable de red',
    'Señal Wi‑Fi débil en zonas alejadas': 'Reubicar router o instalar repetidor Wi‑Fi',
    'Congestión o lentitud del servidor interno': 'Analizar carga y rendimiento del servidor interno',
}


# Cinco casos de prueba
casos = [
    # Caso 1: sólo sin conexión
    {'Sin conexión a Internet': 1,
     'Conexión intermitente': 0,
     'Lentitud al acceder al servidor interno': 0,
     'Mensajes de error DNS': 0,
     'Señal Wi‑Fi débil': 0},

    # Caso 2: intermitente + lentitud interna
    {'Sin conexión a Internet': 0,
     'Conexión intermitente': 1,
     'Lentitud al acceder al servidor interno': 1,
     'Mensajes de error DNS': 0,
     'Señal Wi‑Fi débil': 0},

    # Caso 3: sólo errores DNS
    {'Sin conexión a Internet': 0,
     'Conexión intermitente': 0,
     'Lentitud al acceder al servidor interno': 0,
     'Mensajes de error DNS': 1,
     'Señal Wi‑Fi débil': 0},

    # Case 4: lentitud interna + Wi‑Fi débil
    {'Sin conexión a Internet': 0,
     'Conexión intermitente': 0,
     'Lentitud al acceder al servidor interno': 1,
     'Mensajes de error DNS': 0,
     'Señal Wi‑Fi débil': 1},

    # Caso 5: múltiples síntomas
    {'Sin conexión a Internet': 1,
     'Conexión intermitente': 1,
     'Lentitud al acceder al servidor interno': 0,
     'Mensajes de error DNS': 1,
     'Señal Wi‑Fi débil': 0},
]

if __name__ == "__main__":
    for i, ev in enumerate(casos, start=1):
        resultado = diagnosticar(ev)
        causa_mas_probable, prob = next(iter(resultado.items()))
        print(f"Caso {i}: síntomas={ev}")
        print(f"  Diagnóstico: {causa_mas_probable} (p={prob:.2f})")
        print(f"  Acción sugerida: {acciones[causa_mas_probable]}\n")
