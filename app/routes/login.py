from fastapi import FastAPI, RedirectResponse

app = FastAPI()

# Xero OAuth2 credentials
CLIENT_ID = "YOUR_CLIENT_ID"
REDIRECT_URI = "http://localhost:8000/callback"  # Replace with your actual redirect URI

# Step 1: Redirect the user to the Xero authorization URL
@app.get("/login")
async def login():
    # Xero OAuth2 Authorization URL
    authorization_url = f"https://login.xero.com/identity/connect/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=offline_access+accounting.transactions"
    return RedirectResponse(authorization_url)