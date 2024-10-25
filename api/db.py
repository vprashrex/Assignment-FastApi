from motor.motor_asyncio import AsyncIOMotorClient


MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.school_blog
blog_collection = db.get_collection("blogs")