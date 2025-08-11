from fastapi import Request, HTTPException

@app.get("/callback")
async def callback(request: Request):
    code = request.query_params.get('code')
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code missing")

    # Step 2: Exchange the code for an access token
    access_token = await get_xero_access_token(code)
    return {"message": "Successfully authenticated", "access_token": access_token}