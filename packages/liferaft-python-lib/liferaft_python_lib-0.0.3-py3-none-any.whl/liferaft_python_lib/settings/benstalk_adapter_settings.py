from pydantic_settings import BaseSettings

from liferaft_python_lib.settings.config_dict import config_dict


class BeanstalkAdapterSettings(BaseSettings):
    model_config = config_dict

    BEANSTALK_HOST: str
    BEANSTALK_PORT: int
    BEANSTALK_QUEUE_NAME: str


beanstalk_adapter_settings = BeanstalkAdapterSettings()
