from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "sua-chave-secreta-segura"  # Troque por uma chave segura em produção
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Tempo de expiração do token

    class Config:
        env_file = ".env"

settings = Settings()