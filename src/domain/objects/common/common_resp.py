from datetime import datetime
from pydantic import BaseModel


class CommonResponse(BaseModel):
    item_id:int
    event_date:datetime