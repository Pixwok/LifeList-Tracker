from pydantic import BaseModel
from typing import Generic, TypeVar

d = TypeVar("T") # d accepte tout les types de valeur 

# Modèle de réponse API
class APIResponse(BaseModel, Generic[d]): # Paramètrable avec n'importe quel type de data   
    success: bool
    data: d | None = None
    error: str | None = None

# Réponse de succès
def success_response(data: d | None = None) -> APIResponse[d]:
    return APIResponse(
        success = True,
        data = data,
        error = None
    )

# Réponse d'erreur 
def error_response(message: str) -> APIResponse[None]:
    return APIResponse(
        success = False,
        data = None,
        error = message
    )