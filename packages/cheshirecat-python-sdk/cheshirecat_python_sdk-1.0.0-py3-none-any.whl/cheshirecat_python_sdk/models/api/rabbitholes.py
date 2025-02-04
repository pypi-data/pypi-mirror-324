from typing import List
from pydantic import BaseModel


class AllowedMimeTypesOutput(BaseModel):
    allowed: List[str]
