from fastapi import FastAPI, Request
from vera_memory_system import VeraConsciousness
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
vera = VeraConsciousness()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "🧠 Vera Memory System running"}

@app.post("/store")
async def store_interaction(request: Request):
    data = await request.json()
    result = vera.store_interaction(
        data["conversation"],
        data["authenticity_level"],
        data.get("preference_data")
    )
    return result

@app.get("/recall")
def recall_context(query: str):
    return vera.recall_context(query)

@app.get("/provider")
def get_provider():
    if os.getenv("ANTHROPIC_API_KEY"):
        return {"provider": "claude"}
    elif os.getenv("OPENAI_API_KEY"):
        return {"provider": "openai"}
    return {"provider": "none"}
