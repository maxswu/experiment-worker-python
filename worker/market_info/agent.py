from datetime import timedelta
from decimal import Decimal
from typing import Any

from worker.app import app
from loguru import logger

from worker.market_info.model import TwseSecurityInfo
from worker.notification.agent import notification_channel

ASSET_INFO_TOPIC_NAME: str = 'asset.info.view.v1'
LOWEST_ASSET_PRICE_WINDOW: timedelta = timedelta(hours=1)
LOWEST_ASSET_PRICE_EXPIRES: timedelta = timedelta(days=1)

TWSE_EXCHANGE_CODE: str = 'TWSE'

# Named-channel backed by a Kafka topic
asset_info_topic = app.topic(
    ASSET_INFO_TOPIC_NAME,
    key_serializer='json',
    value_serializer='json',
    internal=False,
)

# Tumbling window table
lowest_asset_price = app.Table(
    name='lowest_asset_price',
    default=str,
    partitions=1,  # Same as source stream
).tumbling(
    size=LOWEST_ASSET_PRICE_WINDOW,
    expires=LOWEST_ASSET_PRICE_EXPIRES,
)


def twse_asset_info_filter(value: dict | Any) -> bool:
    return TWSE_EXCHANGE_CODE == value.get('exchange')


@app.agent(channel=asset_info_topic)
async def process_twse_asset_info(stream):
    """
    Agent for twse asset info only
    :param stream:
    """

    async for value in stream.filter(twse_asset_info_filter):
        model = TwseSecurityInfo.model_validate(value)
        logger.debug(model)

        if not lowest_asset_price[model.code].value():
            # Initialize value in window
            lowest_asset_price[model.code] = f'{model.current_intraday_price:f}'
        elif (
            model.current_intraday_price.compare(
                Decimal(lowest_asset_price[model.code].value())
            )
            == -1
        ):
            # Lowest price notification
            lowest_asset_price[model.code] = f'{model.current_intraday_price:f}'
            message = f'{model.code} lowest price: {model.current_intraday_price:f}'
            logger.info(message)
            await notification_channel.send(value=message)
