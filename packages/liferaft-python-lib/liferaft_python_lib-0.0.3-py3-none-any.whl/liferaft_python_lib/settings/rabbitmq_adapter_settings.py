from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings

from liferaft_python_lib.settings.config_dict import config_dict


class RabbitMQAdapterSettings(BaseSettings):
    model_config = config_dict

    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: SecretStr
    RABBITMQ_HOST: str = Field(alias="RABBITMQ_HOST_1")
    RABBITMQ_PORT: int
    RABBITMQ_CONSUME_QUEUE_NAME: str
    RABBITMQ_ERROR_QUEUE_NAME: str
    RABBITMQ_MAX_RETRIES: int
    RABBITMQ_MESSAGE_CONSUMPTION_LIMIT: int = -1
    RABBITMQ_MESSAGE_AUTO_ACK: bool = False
    RABBITMQ_MESSAGE_PREFETCH_COUNT: int = 0


rabbitmq_adapter_settings = RabbitMQAdapterSettings()
