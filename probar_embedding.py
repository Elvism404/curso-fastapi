from datetime import datetime
# Importamos el creador de agentes moderno que SI está en tu versión actual
from langchain.agents import create_agent  
from langchain_core.tools import tool
from langchain_groq import ChatGroq

# 1. EL MODELO (Configurado para gastar el mínimo de tokens posible)
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # El modelo más ahorrador y rápido de Groq
    temperature=0,                 # Evita que la IA invente datos
    max_tokens=150                 # Bozal estricto: la respuesta será muy corta
)

# 2. HERRAMIENTA 1: Dar la hora
@tool
def dar_la_hora(query: str = "") -> str:
    """Úsala únicamente cuando el usuario pregunte la hora actual del sistema o qué hora es."""
    return datetime.now().strftime("%H:%M")

# 3. HERRAMIENTA 2: Tus apuntes académicos (Simulados directamente en Python)

@tool
def buscar_apuntes_academicos(pregunta: str) -> str:
    """Úsala únicamente cuando pregunten conceptos matemáticos como limites, derivadas o integrales."""
    base_de_datos = [
        "La derivada mide la razon de cambio de una funcion.",
        "El limite es el valor al que se acerca una funcion.",
        "Una integral calcula el area bajo una curva."
    ]
    
    pregunta_limpia = pregunta.lower().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    
    for apunte in base_de_datos:
        for palabra in ["derivada", "limite", "integral"]:
            if palabra in pregunta_limpia and palabra in apunte.lower():
                return apunte
            
    return "No encontre apuntes sobre ese tema especifico."



# Juntamos ambas herramientas en una lista
herramientas = [dar_la_hora, buscar_apuntes_academicos]

# 4. EL PROMPT (Instrucciones sencillas para que la IA decida)
prompt_sistema = (
    "Eres un asistente de estudio. Tienes acceso a herramientas para dar la hora y buscar apuntes. "
    "Tu trabajo es leer la pregunta, decidir qué herramienta necesitas, usarla una sola vez, "
    "y responder usando una sola frase corta basada estrictamente en lo que te devuelva la herramienta."
)

# 5. CREACIÓN DEL AGENTE MODERNO (Libre de errores de importación)
agente = create_agent(
    model=llm, 
    tools=herramientas,
    system_prompt=prompt_sistema,
    debug=True  # Te mostrará el paso a paso en la terminal para que entiendas el chiste del agente
)

# 6. HACEMOS LA PREGUNTA DE PRUEBA
# Puedes cambiar esta pregunta por: "¿que es un limite?" o por: "¿que hora es?"
pregunta_usuario = "¿que es un limite?"

try:
    respuesta = agente.invoke(
        {"messages": [{"role": "user", "content": pregunta_usuario}]},
        config={"recursion_limit": 15}  # Límite seguro para dar los pasos normales y cerrarse solo
    )
    
    print("\n================ RESPUESTA FINAL ================")
    print(respuesta["messages"][-1].content)
    print("=================================================")

except Exception as e:
    print(f"\n[Proceso detenido de forma segura]: {e}")

