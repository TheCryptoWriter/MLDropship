
import asyncio
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# This is a placeholder for the actual tool call which will be available in the execution environment
def google_web_search(query: str) -> dict:
    # In a real environment, this would make a call to the google_web_search tool
    print(f"Simulating google_web_search for query: {query}")
    return {
        "results": [
            {
                "title": f"Sample result for {query}",
                "link": "https://example.com",
                "snippet": "This is a sample snippet with a price of $19.99 from seller BestSeller."
            }
        ]
    }

# Import the worker function
# In a real scenario, this might be a separate microservice.
from backend.mcp_worker.worker import analyze_product_batch

# --- Pydantic Models ---
class Product(BaseModel):
    title: str
    price: Optional[str] = None
    seller: Optional[str] = None
    source: str
    link: str

class AIAnalysis(BaseModel):
    potential_margin: str
    market_demand: str
    seller_reliability: str

class AnalyzedProduct(Product):
    ai_analysis: AIAnalysis

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Dropshipping Scanner API",
    description="API for finding and analyzing dropshipping products.",
    version="1.0.0"
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- Helper Functions ---
def parse_search_result(result: dict, source: str) -> Optional[Product]:
    """Parses a search result dictionary to extract product information."""
    try:
        title = result.get("title")
        link = result.get("link")
        snippet = result.get("snippet", "")

        if not title or not link:
            return None

        # Simple regex to find prices and seller info - can be improved
        price_match = re.search(r'\$\d+\.\d{2}', snippet)
        price = price_match.group(0) if price_match else None

        seller_match = re.search(r'(?i)(?:seller|by|from)\s+([\w\d]+)', snippet)
        seller = seller_match.group(1) if seller_match else None

        return Product(
            title=title,
            price=price,
            seller=seller,
            source=source,
            link=link
        )
    except Exception:
        return None

# --- API Endpoints ---
@app.get("/api/products/{product_query}", response_model=List[Product])
async def get_product_data(product_query: str):
    """
    Searches major marketplaces for a given product and returns a list of raw product data.
    """
    marketplaces = ["ebay.com", "amazon.com", "facebook.com/marketplace"]
    all_products: List[Product] = []

    search_tasks = []
    for site in marketplaces:
        query = f"site:{site} {product_query}"
        # In a real environment, the tool call would be here.
        # We are simulating the call and its result processing.
        search_results = google_web_search(query=query)
        
        for result in search_results.get("results", []):
            product = parse_search_result(result, site)
            if product:
                all_products.append(product)

    if not all_products:
        raise HTTPException(status_code=404, detail="No products found for this query.")
        
    return all_products

@app.get("/api/products/{product_query}/ai", response_model=List[AnalyzedProduct])
async def get_product_data_ai(product_query: str):
    """
    Fetches product data and enriches it with AI-driven analysis for margin, demand, and reliability.
    """
    # 1. Get raw product data
    products_raw = await get_product_data(product_query)
    
    # 2. Convert Pydantic models to a JSON-serializable list of dicts
    products_json = [product.dict() for product in products_raw]
    
    # 3. Call the AI worker for analysis
    try:
        analyzed_data_json = analyze_product_batch(products_json)
        
        # 4. Convert the results back into Pydantic models
        analyzed_products = [AnalyzedProduct(**item) for item in analyzed_data_json]
        return analyzed_products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Dropshipping Scanner API. See /docs for documentation."}
