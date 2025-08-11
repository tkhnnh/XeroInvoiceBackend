import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Union
from datetime import datetime

router = APIRouter()

# Define a Pydantic model for one row of Excel data
class InvoiceRow(BaseModel):
    Invoice_ID: str
    Date: str
    Customer_Name: str
    Item: str
    Quantity: Union[int, float]
    Unit_Price: Union[int, float]
    Total: Union[int, float]

# Xero OAuth2 credentials (replace these with your own values)
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "YOUR_REDIRECT_URI"
AUTHORIZATION_URL = "https://login.xero.com/identity/connect/authorize"
TOKEN_URL = "https://identity.xero.com/connect/token"

# Function to transform the incoming data into Xero-compatible format
def transform_to_xero_format(data: List[InvoiceRow]):
    xero_invoices = []
    
    for invoice in data:
        xero_invoice = {
            "Type": "ACCREC",  # Accounts receivable (default, you can adjust this)
            "Contact": {
                "Name": invoice.Customer_Name
            },
            "Date": invoice.Date,
            "DueDate": "2025-08-15",  # Customize due date as needed
            "LineItems": [
                {
                    "Description": invoice.Item,
                    "Quantity": invoice.Quantity,
                    "UnitAmount": invoice.Unit_Price,
                    "AccountCode": "200",  # Adjust this based on your chart of accounts
                    "TaxType": "NONE"  # You can change this if needed (e.g., "TAX")
                }
            ],
            "Status": "AUTHORISED"  # Default status, can be changed
        }
        xero_invoices.append(xero_invoice)
    
    return xero_invoices

# Function to get the access token (you'll need to handle OAuth2 flow in your app)
async def get_xero_access_token():
    # You'll need to have already obtained the authorization code to exchange for a token
    authorization_code = "YOUR_AUTHORIZATION_CODE"  # Replace with actual code
    token_data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_URL, data=token_data)
        response_data = response.json()

        if response.status_code == 200:
            return response_data['access_token']
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to get access token")

# Function to send data to Xero
async def send_to_xero(xero_data):
    access_token = await get_xero_access_token()  # Get the access token
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    xero_url = "https://api.xero.com/api.xro/2.0/Invoices"  # Xero Invoices endpoint
    
    async with httpx.AsyncClient() as client:
        response = await client.post(xero_url, json=xero_data, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to send to Xero: {response.text}")

# POST endpoint that accepts a list of rows
@router.post("/upload")
async def upload(data: List[InvoiceRow]):
    # Print the received data for debugging
    print("Received data:", data)

    # Transform the data into Xero-compatible format
    xero_ready_data = transform_to_xero_format(data)

    # Send the data to Xero
    try:
        response_data = await send_to_xero(xero_ready_data)
        print("Response from Xero:", response_data)
        return {"message": f"Received {len(data)} invoices and sent to Xero successfully."}
    except HTTPException as e:
        return {"error": f"An error occurred: {e.detail}"}

