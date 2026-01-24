from fastapi_plugin.fast_api_client import Auth0FastAPI
from app.core.config import setting

auth0 = Auth0FastAPI(domain=setting.AUTH0_DOMAIN, audience=setting.AUDIENCE)
