from fastapi import FastAPI

app = FastAPI()

app.name = "SMS Catcher API"
app.version = "0.1.0"

@app.get("/")
def read_root():
    return "test"

