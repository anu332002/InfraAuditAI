import uvicorn
from src.app import metrics_exporter

if __name__ == "__main__":
    uvicorn.run("src.app.metrics_exporter:app", port=8000, reload=True)
