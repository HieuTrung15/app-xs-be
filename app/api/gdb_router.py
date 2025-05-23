from fastapi import APIRouter, HTTPException
from app.services.gdb_service import get_gdb_data

router = APIRouter()

@router.get("/gdb")
async def get_gdb_endpoint():
    try:
        return await get_gdb_data()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
