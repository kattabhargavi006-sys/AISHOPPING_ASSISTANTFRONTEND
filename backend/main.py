from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="AI Shopping Assistant")


class ProductQuery(BaseModel):
    query: str


# -----------------------------
# Product Search Tool
# -----------------------------
def search_products(query):

    products = [
        {
            "name": "HP Victus",
            "price": 58999,
            "pros": [
                "Powerful Performance",
                "Good Battery",
                "Gaming Support"
            ],
            "cons": [
                "Heavy Weight"
            ]
        },
        {
            "name": "Lenovo IdeaPad Gaming",
            "price": 59999,
            "pros": [
                "Strong Build",
                "Good Display"
            ],
            "cons": [
                "Average Battery"
            ]
        },
        {
            "name": "ASUS Vivobook",
            "price": 56999,
            "pros": [
                "Light Weight",
                "Good Battery"
            ],
            "cons": [
                "Not Suitable For Heavy Gaming"
            ]
        }
    ]

    return products


# -----------------------------
# Recommendation Agent
# -----------------------------
def recommend_best(products):

    best = max(
        products,
        key=lambda x: len(x["pros"])
    )

    return best


# -----------------------------
# API Endpoint
# -----------------------------
@app.post("/recommend")
def recommend(data: ProductQuery):

    products = search_products(data.query)

    best_product = recommend_best(products)

    return {
        "user_query": data.query,
        "best_product": best_product,
        "all_products": products
    }


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )