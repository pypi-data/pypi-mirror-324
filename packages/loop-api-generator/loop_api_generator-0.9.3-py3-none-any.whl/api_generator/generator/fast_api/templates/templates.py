INITIALIZE_TEMPLATE = """
from fastapi import FastAPI

app = FastAPI()

"""
GET_TEMPLATE = """
@app.get("/{{ route }}")
async def get_{{ route_safe }}():
    return {"message": "GET {{ route }} called successfully"}
"""
POST_TEMPLATE = """
@app.post("/{{ route }}")
async def post_{{ route_safe }}(data: dict):
    return {"message": "POST {{ route }} called successfully", "data": data}
"""
PUT_TEMPLATE = """
@app.put("/{{ route }}")
async def put_{{ route_safe }}(data: dict):
    return {"message": "PUT {{ route }} called successfully", "updated_data": data}
"""
PATCH_TEMPLATE = """
@app.patch("/{{ route }}")
async def patch_{{ route_safe }}(data: dict):
    return {"message": "PATCH {{ route }} called successfully", "updated_data": data}
"""
DELETE_TEMPLATE = """
@app.delete("/{{ route }}")
async def delete_{{ route_safe }}():
    return {"message": "DELETE {{ route }} called successfully"}
"""
FINALIZE_TEMPLATE = """
if __name__ == "__main__":
    import uvicorn

    # Start the FastAPI server
    uvicorn.run(app, host="{{ host }}", port={{ port }})
"""
