import os
import sys
import azure.functions as func
from azure.functions import WsgiMiddleware

# Añade la raíz del repo al path para poder importar 'backend'
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.append(REPO_ROOT)

# Importa tu app Flask (debe existir backend/api.py con 'app = Flask(__name__)')
from backend.api import app as flask_app

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    # Enruta cualquier /api/* hacia tu Flask
    return WsgiMiddleware(flask_app).handle(req, context)
