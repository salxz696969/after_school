from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema
from app.core.context import get_context
from app.utils import setup_logging


async def get_context_for_request():
    async for context in get_context():
        return context


app = FastAPI()

setup_logging()

graphql_app = GraphQLRouter(schema, context_getter=get_context_for_request)
app.include_router(graphql_app, prefix="/graphql")

