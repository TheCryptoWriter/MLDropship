import pytest
import httpx
from backend.app.main import app

# --- Mock Data and Functions ---

def mock_google_web_search(query: str):
    """Mock of the google_web_search tool to return predictable results."""
    return {
        "results": [
            {
                "title": f"Test Product for {query}",
                "link": "https://example.com/test-product",
                "snippet": "A great test product for $25.99 from seller TestSeller."
            }
        ]
    }

# --- Unit Tests ---

@pytest.mark.asyncio
async def test_read_root():
    """Test the root endpoint."""
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Dropshipping Scanner API. See /docs for documentation."}

@pytest.mark.asyncio
async def test_get_product_data(monkeypatch):
    """Test the /api/products/{product_query} endpoint."""
    monkeypatch.setattr("backend.app.main.google_web_search", mock_google_web_search)
    
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/products/widget")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["title"] == "Test Product for site:ebay.com widget"
    assert data[0]["source"] == "ebay.com"
    assert data[0]["price"] == "$25.99"

@pytest.mark.asyncio
async def test_get_product_data_ai(monkeypatch):
    """Test the /api/products/{product_query}/ai endpoint."""
    monkeypatch.setattr("backend.app.main.google_web_search", mock_google_web_search)
    
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/products/gadget/ai")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "ai_analysis" in data[0]
    assert "potential_margin" in data[0]["ai_analysis"]
    assert data[0]["ai_analysis"]["potential_margin"] == "Medium"

@pytest.mark.asyncio
async def test_get_product_data_not_found(monkeypatch):
    """Test the case where no products are found."""
    monkeypatch.setattr("backend.app.main.google_web_search", lambda query: {"results": []})
    
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/products/nonexistentproduct")

    assert response.status_code == 404
    assert response.json() == {"detail": "No products found for this query."}