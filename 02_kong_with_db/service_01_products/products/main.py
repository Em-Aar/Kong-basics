from fastapi import FastAPI


app = FastAPI(
    title='Service 01 for products',
    version='1.0.0'
)


@app.get('/')
async def root():
    return {"message": "Root of product service"}


@app.get('/products')
async def all_products():
    return {"message": "list of all products in products service"}


@app.get('/products/single-product')
async def single_product():
    return {"message": "single product path in products service"}
