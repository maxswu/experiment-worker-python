from datetime import timedelta
from decimal import Decimal

from worker.app import app
from loguru import logger

from worker.market_info.model import TwseSecurityInfo

ASSET_INFO_TOPIC_NAME: str = 'asset.info.view.v1'

asset_info_topic = app.topic(
    ASSET_INFO_TOPIC_NAME,
    key_serializer='json',
    value_serializer='json',
    internal=False,
)

lowest_asset_price = app.Table(
    name='lowest_asset_price',
    default=lambda: '0',
).tumbling(
    size=timedelta(hours=1),
    expires=timedelta(days=1),
)


@app.agent(channel=asset_info_topic)
async def process_asset_info(stream):
    async for value in stream:
        model = TwseSecurityInfo.model_validate(value)
        logger.debug(model)

        if model.current_intraday_price < Decimal(
            lowest_asset_price[model.code].value()
        ):
            lowest_asset_price[model.code] = str(model.current_intraday_price)
            logger.warning(f'Lowest price: {model.current_intraday_price}')

        yield value
