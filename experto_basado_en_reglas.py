# Definición simple del sistema experto
def diagnosticar(sintomas):
    diagnosticos_posibles = {
        "sin_conexion": {
            "ping_router_falla": "Verificar estado del router.",
            "ping_externo_falla": "Contactar al ISP."
        },
        "conexion_intermitente": {
            "conector_danado": "Reemplazar cable/conector.",
            "default": "Verificar estabilidad del ISP."
        },
        "carga_lenta": {
            "error_dns": "Revisar configuración DNS.",
            "trafico_excesivo": "Limitar consumo ancho banda."
        },
        "wifi_debil": "Instalar repetidor Wi-Fi o mover router más cerca.",
        "servidor_lento": "Verificar cableado y servidor interno."
    }

    diagnostico_final = set() # Usar un conjunto para evitar diagnósticos duplicados

    # Convertir síntomas a minúsculas para comparación insensible a mayúsculas/minúsculas
    sintomas_lower = [s.lower() for s in sintomas]

    for sintoma_principal, causas in diagnosticos_posibles.items():
        if sintoma_principal in sintomas_lower:
            if isinstance(causas, dict):
                encontrado_sub_sintoma = False
                for sub_sintoma, diag in causas.items():
                    if sub_sintoma in sintomas_lower:
                        diagnostico_final.add(diag)
                        encontrado_sub_sintoma = True
                if not encontrado_sub_sintoma and "default" in causas:
                    diagnostico_final.add(causas["default"])
            else: # Es un diagnóstico directo
                diagnostico_final.add(causas)

    if not diagnostico_final:
        return ["No se pudo determinar un diagnóstico con los síntomas proporcionados."]

    return list(diagnostico_final)

# Ejemplo de uso
sintomas_usuario = ["conexion_intermitente", "conector_danado"]
print(diagnosticar(sintomas_usuario))

sintomas_usuario_2 = ["sin_conexion", "ping_router_falla"]
print(diagnosticar(sintomas_usuario_2))

sintomas_usuario_3 = ["carga_lenta"] # Prueba default para carga_lenta si no hay sub-sintoma
print(diagnosticar(sintomas_usuario_3))

sintomas_usuario_4 = ["wifi_debil"]
print(diagnosticar(sintomas_usuario_4))

sintomas_usuario_5 = ["sintoma_desconocido"]
print(diagnosticar(sintomas_usuario_5))

sintomas_usuario_6 = ["Conexion_Intermitente", "CONECTOR_DANADO"] # Prueba case-insensitivity
print(diagnosticar(sintomas_usuario_6))

