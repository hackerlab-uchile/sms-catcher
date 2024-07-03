from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import modem, dashboard, update, send_message

app = FastAPI()

# Allow all origins (not recommended for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.name = "SMS Catcher API"

@app.get("/")
async def root():
    return "app running"
    
app.include_router(modem.router)
app.include_router(dashboard.router)
app.include_router(update.router)
app.include_router(send_message.router)