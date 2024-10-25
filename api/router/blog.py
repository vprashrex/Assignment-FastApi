from fastapi import APIRouter,HTTPException
from api.schema.schema import BlogModel,ObjectId
from api.db import blog_collection
from bson import ObjectId
router = APIRouter()

@router.post("/blogs",response_model=BlogModel)
async def create_blog(blog:BlogModel):
    try:
        blog = blog.model_dump(by_alias=True)
        result = await blog_collection.insert_one(blog)
        blog["_id"] = result.inserted_id
        return blog
    
    except Exception as e:
        return {"status":f"error occured : {e}"}
    

@router.get("/blogs/{id}", response_model=BlogModel)
async def get_blog(id: str):
    blog = await blog_collection.find_one({"_id": ObjectId(id)})
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.get("/blogs", response_model=list[BlogModel])
async def get_blogs():
    blogs = await blog_collection.find().to_list(100)
    return blogs


@router.put("/blogs/{id}", response_model=BlogModel)
async def update_blog(id: str, blog: BlogModel):
    blog = blog.model_dump(by_alias=True)
    blog.pop("_id", None)
    result = await blog_collection.update_one({"_id": ObjectId(id)}, {"$set": blog})
    if result.modified_count == 1:
        updated_blog = await blog_collection.find_one({"_id": ObjectId(id)})
        return updated_blog
    raise HTTPException(status_code=404, detail="Blog not found")


@router.delete("/blogs/{id}", response_model=dict)
async def delete_blog(id: str):
    result = await blog_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"message": "Blog deleted successfully"}
    raise HTTPException(status_code=404, detail="Blog not found")