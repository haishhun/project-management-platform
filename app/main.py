from fastapi import FastAPI
app = FastAPI(
    title="Project Management Platform",
    version="1.0.0"
)

@app.get("/")
def root():
    return "{Hello, World}"