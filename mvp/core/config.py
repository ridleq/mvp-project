from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    app_title: str = 'MVP project'
    DB_USERNAME: str = Field(env='DB_USERNAME')
    DB_PASSWORD: str = Field(env='DB_PASSWORD')
    DB_NAME: str = Field(env='DB_NAME')
    DB_HOST: str = Field(env='DB_HOST')
    DB_PORT: int = Field(env='DB_PORT')
    secret: str = 'SECRET'

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
