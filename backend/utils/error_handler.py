from fastapi import HTTPException

def safe_raise(status: int, message: str):
    raise HTTPException(status_code=status, detail=message)
