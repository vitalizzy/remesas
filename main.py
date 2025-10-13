def estructurar_informacion_con_gemini(texto_pdf: str) -> dict:
    """
    Envía el texto extraído a Gemini y le pide que lo estructure en formato JSON.
    """
    # --- CORRECCIÓN AQUÍ ---
    # Usamos 'gemini-1.5-flash-latest' que es el identificador correcto del modelo.
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    # Prompt mejorado para la extracción de datos
    prompt = f"""Eres un experto en extracción de datos de documentos financieros.
A partir del siguiente texto extraído de un documento, necesito que extraigas la siguiente información
y la devuelvas en un formato JSON estricto.

Los campos requeridos son:
{{
    "referencia_unica": string,          // Referencia Única del documento
    "nombre_librado": string,            // Nombre completo del Librado
    "iban": string,                      // Número IBAN, mantener formato
    "importe": float,                    // Cantidad en euros, solo número
    "vencimiento": string,               // Fecha de vencimiento (formato DD/MM/YYYY)
    "emisor": string,                    // Nombre del Emisor
    "identificacion_emisor": string,     // Número o código de identificación del Emisor
    "referencia_fichero": string,        // Referencia del Fichero
    "fecha_recepcion": string,           // Fecha de Recepción (formato DD/MM/YYYY)
    "fecha_documento": string,           // Fecha del Documento (formato DD/MM/YYYY)
    "referencia_documento": string       // Referencia Única del Documento
}}

Reglas importantes:
1. Mantener el formato exacto de fechas como DD/MM/YYYY
2. Para campos no encontrados, usar null (no dejar vacío)
3. Mantener el formato original del IBAN con espacios
4. El importe debe ser un número decimal (sin símbolo €)
5. Devolver SOLO el JSON, sin explicaciones adicionales

Texto del documento a procesar:
{texto_pdf}"""

    try:
        # Hacemos la llamada a la API
        respuesta = model.generate_content(prompt)
        
        if not respuesta.text:
            print("❌ Error: Respuesta vacía del modelo")
            return None
            
        # Limpiamos la respuesta para obtener un JSON puro
        json_limpio = limpiar_respuesta_json(respuesta.text)
        
        try:
            # Convertimos la respuesta de string JSON a un diccionario de Python
            datos_estructurados = json.loads(json_limpio)
            
            # Validación básica de los campos requeridos
            campos_requeridos = {
                'referencia_unica', 'nombre_librado', 'iban', 'importe',
                'vencimiento', 'emisor', 'identificacion_emisor',
                'referencia_fichero', 'fecha_recepcion', 'fecha_documento',
                'referencia_documento'
            }
            
            # Asegurarse de que todos los campos existan (pueden ser None)
            for campo in campos_requeridos:
                if campo not in datos_estructurados:
                    datos_estructurados[campo] = None
            
            return datos_estructurados
            
        except json.JSONDecodeError as e:
            print(f"❌ Error al decodificar JSON: {e}")
            print("Respuesta recibida:")
            print(json_limpio)
            return None
            
    except Exception as e:
        print(f"❌ Error al procesar con Gemini: {e}")
        return None