from pydantic import BaseModel, ValidationError
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

# Define validation schemas using Pydantic
class Params(BaseModel):
    param1: int
    param2: str

class Query(BaseModel):
    query_param: Optional[str] = None

class Body(BaseModel):
    body_param: int

class Cookies(BaseModel):
    cookie_param: str

# Middleware-like validate function
def validate(schema):
    def decorator(func):
        async def wrapper(req: Request, *args, **kwargs):
            valid_schema = {key: schema[key] for key in ['params', 'query', 'body', 'cookies'] if key in schema}
            object_data = {key: getattr(req, key) for key in valid_schema.keys()}
            
            try:
                # Validate using Pydantic
                value = {}
                for key, model in valid_schema.items():
                    if key in object_data:
                        value[key] = model.parse_obj(object_data[key])
                
                # Assign parsed values to request
                for key, val in value.items():
                    setattr(req, key, val)
                
            except ValidationError as error:
                error_message = ', '.join([e['msg'] for e in error.errors()])
                raise HTTPException(status_code=400, detail=error_message)

            return await func(req, *args, **kwargs)

        return wrapper
    return decorator

# FastAPI app example
app = FastAPI()

@app.get("/example")
@validate({
    'params': Params,
    'query': Query,
    'body': Body,
    'cookies': Cookies
})
async def example_endpoint(req: Request):
    return JSONResponse(content={"message": "Success", "data": req.query_param})

