from pydantic import BaseModel, field_validator


class PinCodeModel(BaseModel):
    pincode: str

    @field_validator("pincode")
    @classmethod
    def validate_pin_code(cls, value: str) -> str:
        if not value.isdigit() or len(value) != 6:
            raise ValueError("Pin code must be a 6-digit number.")
        return value

class LocationResponseModel(BaseModel):
    pincode: str
    city: str
    state: str
    district: str

class BulkRequestModel(BaseModel):
    pincodes: list[str]

    @field_validator("pincodes")
    @classmethod
    def validate_pin_codes(cls, value: list[str]) -> list[str]:
        if len(value) == 0:
            raise ValueError("The list of pin codes cannot be empty.")
        if len(value) > 20:
            raise ValueError("The list of pin codes cannot contain more than 20 items.")
        for pin_code in value:
            if not pin_code.isdigit() or len(pin_code) != 6:
                raise ValueError(f"Pin code '{pin_code}' must be a 6-digit number.")
        return value

class BulkResponseModel(BaseModel):
    status: str = "success"
    found: int
    not_found: int
    results: list[LocationResponseModel]
    missing: list[str]    