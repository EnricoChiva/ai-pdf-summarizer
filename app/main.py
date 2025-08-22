from fastapi import FastAPI
import uvicorn

app = FastAPI()

products = []


@app.get("/")
async def get_products():
    return products


@app.get("/products/{product_id}")
async def get_product_by_id(product_id: int):
    for product in products:
        if product.get("id") == product_id:
            return product
    return {"error": "Produkt nicht gefunden"}


@app.put("/products/{product_id}")
async def update_product(product_id: int, new_product: dict):
    for index, p in enumerate(products):
        if p.get("id") == product_id:
            products[index] = new_product
            return {"success": "Produkt wurde geupdatet" }
    return {"error" : "Produkt konntenicht gefunden werden"}


@app.delete("/products/{product_id}")
async def delete_by_id(product_id: int):
    for p in products:
        if p.get("id") == product_id:
            products.remove(p)
            return{"succeess":"Produkt wurde gelöschen"}
    return{"error": "Produkt konte nicht gefunden werden"}


@app.post("/products")
async def create_product(product: dict):
    products.append(product)
    return{"success": "Produkt wurde erstellt"}

