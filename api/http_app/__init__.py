import os, sys
import azure.functions as func
from azure.functions import WsgiMiddleware

# Añade 'api' al sys.path para importar backend.api
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../api
if REPO_ROOT not in sys.path:
    sys.path.append(REPO_ROOT)

from backend.api import app as flask_app

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return WsgiMiddleware(flask_app).handle(req, context)
