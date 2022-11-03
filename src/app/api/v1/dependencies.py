from fastapi import Query


async def paginator(skip: int = 0, limit: int = Query(100, gt=0)):
    return {"skip": skip, "limit": limit}
