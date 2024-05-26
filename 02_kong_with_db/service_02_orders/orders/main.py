from fastapi import FastAPI


app = FastAPI(
    title='Orders service',
    version='1.0.0'
)


@app.get('/')
async def root_orders():
    return {"message": "root of orders service"}


@app.get('/orders')
async def all_orders():
    return {"message": "orders path of orders service"}
