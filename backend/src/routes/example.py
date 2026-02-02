from fastapi import APIRouter, HTTPException, Request, Query

router = APIRouter(prefix="/example", tags=["Example"])

@router.get("/simulation")
async def simulation(req: Request):
    """Run a simulation."""
    try:
        return {"message": "Hello, World!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    
@router.get("/lookupdid")
async def lookup_did(req: Request, value: str = Query(..., description="DID to look up")):
    """Look up a DID document in the registry."""
    try:
        return {"message": "Hello, World!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
