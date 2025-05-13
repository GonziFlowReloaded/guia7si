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

    diagnostico_final = []
    explicaciones = []

    sintomas_lower = [s.lower() for s in sintomas]

    for sintoma_principal, causas in diagnosticos_posibles.items():
        if sintoma_principal in sintomas_lower:
            if isinstance(causas, dict):
                encontrado = False
                for sub_sintoma, diag in causas.items():
                    if sub_sintoma in sintomas_lower:
                        diagnostico_final.append(diag)
                        explicaciones.append(f"Regla activada: SI {sintoma_principal} Y {sub_sintoma} → ENTONCES '{diag}'")
                        encontrado = True
                if not encontrado and "default" in causas:
                    diag = causas["default"]
                    diagnostico_final.append(diag)
                    explicaciones.append(f"Regla por defecto activada: SI {sintoma_principal} → ENTONCES '{diag}'")
            else:
                diag = causas
                diagnostico_final.append(diag)
                explicaciones.append(f"Regla activada: SI {sintoma_principal} → ENTONCES '{diag}'")

    if not diagnostico_final:
        return ["No se pudo determinar un diagnóstico con los síntomas proporcionados."], []

    return diagnostico_final, explicaciones
