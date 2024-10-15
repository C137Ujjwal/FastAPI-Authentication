import models
from config import engine
from fastapi import FastAPI
from routes import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)


