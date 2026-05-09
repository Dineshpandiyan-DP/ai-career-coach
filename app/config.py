from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env",
                                    env_file_encoding="utf-8",
                                    case_sensitive=False,
                                    extra="ignore",)
    groq_api_key:str
    groq_model: str = "llama-3.3-70b-versatile"
    app_name:str="AI Career Coach"
    debug:bool=True
    port:int=8000
    app_version: str = "1.0.0"
@lru_cache()
def get_settings()->Settings:
    return Settings()

##print(get_settings())
