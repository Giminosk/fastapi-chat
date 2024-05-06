from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Chat",
        docs_url="/api/v1/docs",
        debug=True,
    )
    return app


app = FastAPI(
    title="FastAPI Chat",
    docs_url="/api/v1/docs",
    debug=True,
)
