# Mi Tutor IA

Tutor académico con IA que responde preguntas basándose en apuntes propios (RAG).

🔗 **Demo en vivo:** https://curso-fastapi-kappa.vercel.app

## Tecnologías
- FastAPI (backend)
- LangChain + Groq (llama-3.1-8b-instant)
- Supabase (base de datos vectorial)
- Hugging Face Inference API (embeddings)
- HTML + Tailwind CSS (frontend)

## Cómo correrlo en local

1. Clona el repositorio y entra a la carpeta `backend/`
2. Crea un entorno virtual: `python -m venv venv`
3. Actívalo y corre: `pip install -r requirements.txt`
4. Crea un archivo `.env` con tus propias claves
5. Corre el servidor: `uvicorn main:app --reload`
6. Abre `frontend/index.html` con Live Server

## Variables de entorno necesarias

Crea un archivo `.env` en la carpeta `backend/` con:
```
GROQ_API_KEY=tu_clave_aqui
SUPABASE_URL=tu_url_aqui
SUPABASE_KEY=tu_clave_aqui
HF_TOKEN=tu_token_aqui
```

## Estructura del proyecto

```
curso-fastapi/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   └── index.html
├── .gitignore
└── README.md
```

## Limitaciones conocidas

- El sistema depende de que el modelo (llama-3.1-8b-instant) rechace preguntas fuera del contexto de los apuntes; en pruebas fue consistente en la mayoría de los casos, pero no al 100%. Una mejora futura sería agregar un filtro de similitud por distancia antes de enviar el contexto al modelo.