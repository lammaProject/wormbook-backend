from decouple import config

MAIL_CONFIG = {
    "MAIL_USERNAME": config("MAIL_USERNAME"),
    "MAIL_PASSWORD": config("MAIL_PASSWORD"),
    "MAIL_FROM": config("MAIL_FROM"),
    "MAIL_PORT": config("MAIL_PORT", cast=int),
    "MAIL_SERVER": config("MAIL_SERVER"),
    "MAIL_STARTTLS": config("MAIL_STARTTLS", cast=bool),
    "MAIL_SSL_TLS": config("MAIL_SSL_TLS", cast=bool),
    "USE_CREDENTIALS": config("USE_CREDENTIALS", cast=bool),
    "VALIDATE_CERTS": config("VALIDATE_CERTS", cast=bool),
}

TOKEN_CONFIG = {
    "SECRET_KEY": config("SECRET_KEY", cat=str),
    "ALGORITHM": config("ALGORITHM", cat=str),
}
