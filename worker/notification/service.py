import abc
from typing import override

from loguru import logger
from slack_sdk.errors import SlackApiError
from slack_sdk.web.async_client import AsyncWebClient

from worker.notification.config import SlackSettings


class NotificationService(abc.ABC):
    """
    Abstract notification service
    """

    @abc.abstractmethod
    async def send_text_message(self, message: str) -> None:
        """
        Send a simple string message to notification channel
        :param message:
        :return:
        """


class SlackNotificationService(NotificationService):

    def __init__(self, settings: SlackSettings):
        self._settings = settings
        self._client = AsyncWebClient(token=self._settings.bot_token)

    @override
    async def send_text_message(self, message: str) -> None:
        logger.info(f'Sending {message=} to channel: {self._settings.notification_channel_id}')

        try:
            response = await self._client.chat_postMessage(
                channel=self._settings.notification_channel_id,
                text=message,
            )
            logger.debug(f'Slack API status: {response.status_code}')
            logger.debug(response.data)
        except SlackApiError as e:
            logger.exception(e)
            raise NotificationService from e