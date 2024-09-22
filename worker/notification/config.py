from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SlackSettings(BaseSettings):
    """
    Slack settings
    """

    model_config = SettingsConfigDict(env_prefix='SLACK__')

    bot_token: str = Field(..., title='Slack bot token')
    notification_channel_id: str = Field(
        ..., title='Slack channel id for notifications'
    )
