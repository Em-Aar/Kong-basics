from fastapi import FastAPI


app = FastAPI(
    title="Kong Db-less service-1",
    version="1.0.0",
    description= ""
    )


@app.get('/')
async def root():
    return {"message":"hello world"}