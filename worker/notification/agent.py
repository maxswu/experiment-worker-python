from worker.app import app
from loguru import logger

from worker.notification.config import SlackSettings
from worker.notification.exception import NotificationServiceException
from worker.notification.service import NotificationService, SlackNotificationService

# Using slack
notification_service: NotificationService = SlackNotificationService(
    settings=SlackSettings()
)

# Local channel (not backed by a Kafka topic)
# TODO a dedicated model for notifications
notification_channel = app.channel(value_type=str)


@app.agent(channel=notification_channel)
async def process_notification(stream):
    """
    Agent for notifications
    :param stream:
    """

    async for message in stream:
        try:
            await notification_service.send_text_message(message=message)
        except NotificationServiceException as e:
            # Do nothing but log exceptions from service
            logger.exception(e)
