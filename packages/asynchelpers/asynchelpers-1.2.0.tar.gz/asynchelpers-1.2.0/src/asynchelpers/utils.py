import asyncio  
import json  
import aiohttp  

async def async_request(urls):  
    """Batch HTTP requests"""  
    async with aiohttp.ClientSession() as session:  
        tasks = [session.get(url) for url in urls]  
        return await asyncio.gather(*tasks)  

def validate_json(data):  
    """Validate JSON data"""  
    try:  
        json.loads(data)  
        return True  
    except:  
        return False  

def generate_tempname(prefix="tmp"):  
    """Generate random temp IDs"""  
    from secrets import token_hex  
    return f"{prefix}_{token_hex(4)}"  