from pydantic import BaseModel

class PromoCodeRequest(BaseModel):
    promo_code: str

class PromoCodeResponse(BaseModel):
    extended_description: str