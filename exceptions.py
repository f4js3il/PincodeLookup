from fastapi.responses import JSONResponse
from fastapi.requests import Request


class PinCodeNotFoundError(Exception):
    def __init__(self, pin_code: str):
        self.pin_code = pin_code

class InvalidPinCodeError(Exception):
    def __init__(self, pin_code: str, reason: str = "Invalid pin code format"):
        self.pin_code = pin_code
        self.reason = reason


async def pin_code_not_found_exception_handler(request: Request, exc: PinCodeNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": f"Pin code '{exc.pin_code}' not found.",
            "message": "Please check the pin code and try again.",
            "pin_code": exc.pin_code
            },
    )

async def invalid_pin_code_exception_handler(request: Request, exc: InvalidPinCodeError):
    return JSONResponse(
        status_code=400,
        content={
            "error": f"Pin code '{exc.pin_code}' is invalid.: {exc.reason}",
            "message": exc.reason,
            "pin_code": exc.pin_code
        },
    )
