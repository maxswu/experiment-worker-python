from pydantic import Field, BaseModel
from decimal import Decimal


class TwseSecurityInfo(BaseModel):
    exchange: str = Field(..., title='市場別(交易所)')
    code: str = Field(..., title='代號')
    name: str = Field(..., title='名稱')
    query_time: float = Field(..., title='查詢時間')
    full_name: str = Field(..., title='全名')
    opening_price: Decimal = Field(..., title='開盤價')
    current_intraday_price: Decimal = Field(..., title='當前盤中成交價')
    highest_price: Decimal = Field(..., title='最高價')
    lowest_price: Decimal = Field(..., title='最低價')
    updated_time: float = Field(..., title='資料更新時間')
