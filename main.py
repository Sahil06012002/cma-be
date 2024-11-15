from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware import AuthMiddleware
from routes import product_route, user_route

app = FastAPI(root_path="/api")
app.add_middleware(AuthMiddleware)

origins = [
    "http://localhost:5173",
    "https://cma-fe-psi.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=True,          
    allow_methods=["*"],             
    allow_headers=["*"],             
)

app.include_router(user_route.router,prefix="/user")
app.include_router(product_route.router,prefix="/product")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}

