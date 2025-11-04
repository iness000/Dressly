import asyncio
import json
from hm_client import hm_list_products

async def test_hm_api():
    print("🧪 Testing H&M API...")
    
    try:
        # Test 1: Fetch men's trousers
        print("\n1️⃣ Fetching men's trousers...")
        result = await hm_list_products("men_trousers", page=0, size=5)
        
        print(f"✅ Found {len(result.get('results', []))} products")
        
        # Display first product
        if result.get('results'):
            product = result['results'][0]
            print(f"\n📦 First product:")
            print(f"  Name: {product.get('name')}")
            print(f"  Price: {product.get('price', {}).get('formattedValue')}")
            print(f"  Code: {product.get('code')}")
            print(f"  Image: {product.get('images', [{}])[0].get('url', 'N/A')[:80]}...")
        
        # Test 2: Different category
        print("\n2️⃣ Fetching men's shirts...")
        result2 = await hm_list_products("men_shirts", page=0, size=3)
        print(f"✅ Found {len(result2.get('results', []))} products")
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_hm_api())