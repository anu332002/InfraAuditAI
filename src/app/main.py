import uvicorn
from src.app import metrics_exporter

# Optional: import from utils if needed
# from src.app.utils import get_message

if __name__ == "__main__":
    uvicorn.run("src.app.metrics_exporter:app", port=8000, reload=True)
