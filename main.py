from dotenv import load_dotenv
import os
load_dotenv()
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from supabase import create_client
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI()

# --- RAG: búsqueda de apuntes ---
modelo = SentenceTransformer("all-MiniLM-L6-v2")
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def buscar_contexto(pregunta: str) -> str:
    vector = modelo.encode(pregunta).tolist()
    resultado = supabase.rpc("buscar_apuntes", {"vector_pregunta": vector}).execute()
    return "\n".join([r["contenido"] for r in resultado.data])
# ----------------------------------

# --- Cadena de LangChain (plantilla + modelo) ---
llm = ChatGroq(model="llama-3.1-8b-instant", streaming=True)
plantilla = ChatPromptTemplate.from_template(
    "Basándote SOLO en esto:\n{contexto}\nResponde: {pregunta}"
)
cadena = plantilla | llm
# ----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pregunta(BaseModel):
    pregunta: str

@app.get("/")
def inicio():
    return {"mensaje": "¡Mi primer mesero está funcionando!"}

@app.post("/preguntar")
async def recibir_pregunta(datos: Pregunta):
    try:
        contexto = buscar_contexto(datos.pregunta)

        def generar():
            for chunk in cadena.stream({"contexto": contexto, "pregunta": datos.pregunta}):
                yield chunk.content or ""
        return StreamingResponse(generar(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=503, detail="La IA no respondió, intenta de nuevo")