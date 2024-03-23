from pydantic import BaseModel


class Response201(BaseModel):
    message: str = "Content created sucessfully."


class Response204(BaseModel):
    message: str = "Request sucessfull, no content to show."


class Response400(BaseModel):
    message: str = "Error detected at client side."


class Response404(BaseModel):
    message: str = "Stated content couldn't be located."


class Response406(BaseModel):
    message: str = "The provided value is not acceptable."


class Response422(BaseModel):
    message: str = "Invalid payload. Maybe wrong data type or something."


class Response500(BaseModel):
    message: str = "Internal server error occured."
