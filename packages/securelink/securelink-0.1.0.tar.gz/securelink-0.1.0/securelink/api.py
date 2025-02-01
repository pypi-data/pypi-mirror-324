from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from .config import config
from . import sign

# Define the FastAPI app
app = FastAPI()


class SecureLinkRequestBase(BaseModel):
    url: str
    clientip: Optional[str] = "127.0.0.1"

class SecureLinkRequest(SecureLinkRequestBase):
    expire_seconds: Optional[int] = 20


@app.post("/generate-secure-md5-link/")
async def generate_secure_link(request: SecureLinkRequest):
    try:
        secure_url = sign.generate_md5_base64_url(
            request.url, config.SECRET_KEY, request.expire_seconds, request.clientip
        )
        return {"secure_url": secure_url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating URL: {str(e)}")


@app.post("/validate-secure-link/")
async def validate_secure_link(request: SecureLinkRequestBase):
    try:
        is_valid = sign.validate_md5_base64_url(
            request.url, config.SECRET_KEY, request.clientip
        )
        if is_valid:
            return {"message": "The secure link is valid."}
        else:
            raise HTTPException(
                status_code=403, detail="Invalid or expired secure link."
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error validating URL: {str(e)}")
