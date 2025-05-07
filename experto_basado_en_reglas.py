# Definición simple del sistema experto
def diagnosticar(sintomas):
    diagnostico = []
    if "sin_conexion" in sintomas:
        if "ping_router_falla" in sintomas:
            diagnostico.append("Verificar estado del router.")
        elif "ping_externo_falla" in sintomas:
            diagnostico.append("Contactar al ISP.")
    if "conexion_intermitente" in sintomas:
        if "conector_danado" in sintomas:
            diagnostico.append("Reemplazar cable/conector.")
        else:
            diagnostico.append("Verificar estabilidad del ISP.")
    if "carga_lenta" in sintomas:
        if "error_dns" in sintomas:
            diagnostico.append("Revisar configuración DNS.")
        elif "trafico_excesivo" in sintomas:
            diagnostico.append("Limitar consumo ancho banda.")
    if "wifi_debil" in sintomas:
        diagnostico.append("Instalar repetidor Wi-Fi o mover router más cerca.")
    if "servidor_lento" in sintomas:
        diagnostico.append("Verificar cableado y servidor interno.")
    return diagnostico

# Ejemplo de uso
sintomas_usuario = ["conexion_intermitente", "conector_danado"]
print(diagnosticar(sintomas_usuario))

