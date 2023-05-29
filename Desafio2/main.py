from fastapi import FastAPI, Depends
from pydantic import BaseModel

import sqlite3

app = FastAPI()
  
conn = sqlite3.connect("products.db")
cursor = conn.cursor()

    
cursor.execute("""
    CREATE TABLE IF NOT EXISTS product (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        ProductNumber TEXT,
        Color TEXT,
        Price FLOAT
    )
""")

class Product(BaseModel):
    Name: str
    ProductNumber: str
    Color: str
    Price: float

@app.post("/products")
async def add_product(product:Product):
    
    cursor.execute("INSERT INTO product (Name, ProductNumber, Color, Price) VALUES (?, ?, ?, ?)", (product.Name, product.ProductNumber, product.Color, product.Price))
    
    conn.commit()
    
    return { "message" : f"Produto {product.Name} foi criado !"}
    
  
@app.get("/products")
async def list_products():
  cursor.execute("SELECT * FROM product")
  product = cursor.fetchall()
  
  return { "products" : product }

@app.get("/products/{id}")
async def list_product(id:int):
  cursor.execute("SELECT * FROM product WHERE Id = ?", (id,))
  product = cursor.fetchone()
  
  if product:
    return { "product" : product }
  else:
    return {"message": f"Produto com ID {id} não encontrado"}

@app.put("/products/{id}")
async def update_product(id:int, product:Product):
  
  cursor.execute("UPDATE product SET Name = ?, ProductNumber = ?, Color = ?, Price = ? WHERE Id = ?", (product.Name, product.ProductNumber, product.Color, product.Price, id))
  
  conn.commit()
 
  
  if cursor.rowcount > 0:
        return {"message": f"Produto com ID {id} atualizado com sucesso!"}
  else:
        return {"message": f"Produto com ID {id} não encontrado"}
  
  
@app.delete("/products/{id}")
async def delete_product(id:int):
  cursor.execute("DELETE FROM product WHERE Id = ?", (id,))
   
  if cursor.rowcount > 0:
        return {"message": "Produto removido com sucesso!"}
  else:
        return {"message": "Produto não encontrado!"} 
