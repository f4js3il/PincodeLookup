from fastapi import FastAPI
from exceptions import (
    PinCodeNotFoundError, 
    InvalidPinCodeError, 
    pin_code_not_found_exception_handler, 
    invalid_pin_code_exception_handler
)
from models import LocationResponseModel, BulkResponseModel,BulkRequestModel
from data import pincode_db 



app = FastAPI(
    title="zip code look up API",
    description="This API allows you to look up information about zip codes.",
)

app.add_exception_handler(PinCodeNotFoundError, pin_code_not_found_exception_handler)
app.add_exception_handler(InvalidPinCodeError, invalid_pin_code_exception_handler)

@app.get("/")
def root():
    return {"message": "Welcome to the zip code look up API!"}

@app.get("/pincode/{pincode}",response_model=LocationResponseModel)
def get_pincode_info(pincode: str):
    if not pincode.isdigit() or len(pincode) != 6:
        raise InvalidPinCodeError(pincode, "Pin code must be a 6-digit number.")
    if pincode not in pincode_db:
        raise PinCodeNotFoundError(pincode)
    return pincode_db[pincode]

@app.post("/pincode/bulk",response_model=BulkResponseModel)
def get_bulk_pincode_info(request: BulkRequestModel):
    results = []
    missing = []

    for pin_code in request.pincodes:
        if pin_code in pincode_db:
            results.append(pincode_db[pin_code])
        else:
            missing.append(pin_code)
    return BulkResponseModel(
        found=len(results),
        not_found=len(missing),
        results=results,
        missing=missing
    )
