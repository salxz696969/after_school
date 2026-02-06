from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema
from app.core.context import get_context
import logging
import colorlog


async def get_context_for_request():
    async for context in get_context():
        return context


app = FastAPI()

# ---- Colored logging setup ----
handler = colorlog.StreamHandler() # type: ignore
handler.setFormatter( # type: ignore
    colorlog.ColoredFormatter( # type: ignore
        "%(log_color)s%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        log_colors={
            "DEBUG": "cyan",
        },
    )
)

root_logger = logging.getLogger()
root_logger.handlers.clear()
root_logger.addHandler(handler) # type: ignore
root_logger.setLevel(logging.DEBUG)
# --------------------------------

graphql_app = GraphQLRouter(schema, context_getter=get_context_for_request)
app.include_router(graphql_app, prefix="/graphql")
