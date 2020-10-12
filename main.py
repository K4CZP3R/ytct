from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers import auth, search, videos
from exceptions import google_oauth_exception, ytct_missing_data
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:4200",
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    search.router,
    prefix="/search",
    tags=["search"]
)

app.include_router(
    videos.router,
    prefix="/videos",
    tags=["videos"]
)

@app.exception_handler(ytct_missing_data.YtctMissingData)
@app.exception_handler(google_oauth_exception.GoogleOauthException)
async def google_oauth_exception_handler(request: Request, exc: google_oauth_exception.GoogleOauthException):
    return JSONResponse(
        status_code=422,
        content={"message": f"Oops! Something went wrong! {exc.message}"}
    )

@app.get("/")
async def root():
    return {"message": "Hello World!"}