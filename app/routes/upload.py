from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Union

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

# POST endpoint that accepts a list of rows
@router.post("/upload")
async def upload(data: List[InvoiceRow]):
    # For now, just print or log the received data
    print("Received data:", data)

    # You can now forward this to Xero API or process it however you like
    return {"message": f"Received {len(data)} invoices successfully."}
