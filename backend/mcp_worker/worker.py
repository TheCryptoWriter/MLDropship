
import random

def analyze_product_batch(products: list[dict]) -> list[dict]:
    """
    Receives a batch of raw product JSON, uses AI annotation to augment it
    with margin, demand, and reliability scores, and returns the augmented JSON.

    In this simulation, we use simple heuristics. A real implementation would
    use a powerful model like Gemini Pro for more sophisticated analysis.
    """
    augmented_products = []
    for product in products:
        # --- AI Analysis Simulation ---
        
        # 1. Potential Margin Analysis
        price_str = product.get('price', '0').replace('$', '').strip()
        try:
            price = float(price_str)
            if price < 20:
                margin = "High"
            elif price < 100:
                margin = "Medium"
            else:
                margin = "Low"
        except (ValueError, TypeError):
            margin = "Medium" # Default value

        # 2. Market Demand Analysis
        title = product.get('title', '').lower()
        if 'bestseller' in title or 'popular' in title:
            demand = "High"
        elif len(title) > 15: # Simple heuristic
            demand = "Medium"
        else:
            demand = "Low"

        # 3. Seller Reliability Analysis
        seller = product.get('seller', '').lower()
        snippet = product.get('snippet', '').lower()
        if 'top rated' in seller or 'trusted' in snippet:
            reliability = "High"
        elif seller:
            reliability = "Medium"
        else:
            reliability = "Low"

        # --- Augment Product Data ---
        product['ai_analysis'] = {
            "potential_margin": margin,
            "market_demand": demand,
            "seller_reliability": reliability
        }
        augmented_products.append(product)
        
    return augmented_products
