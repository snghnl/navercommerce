"""Constants for the Naver Commerce SDK."""

from typing import Final

# API Base URL
BASE_URL: Final[str] = "https://api.commerce.naver.com/external"

# OAuth endpoints
OAUTH_TOKEN_URL: Final[str] = "/v1/oauth2/token"

# Timeout settings (in seconds)
DEFAULT_TIMEOUT: Final[int] = 60
DEFAULT_MAX_RETRIES: Final[int] = 2

# Token settings
TOKEN_EXPIRY_SECONDS: Final[int] = 10800  # 3 hours
TOKEN_REFRESH_BUFFER_SECONDS: Final[int] = 1800  # 30 minutes
TOKEN_REFRESH_THRESHOLD_SECONDS: Final[int] = TOKEN_EXPIRY_SECONDS - TOKEN_REFRESH_BUFFER_SECONDS

# HTTP Headers
USER_AGENT: Final[str] = "navercommerce-python/0.1.0"

# Environment variable names
ENV_CLIENT_ID: Final[str] = "NAVER_CLIENT_ID"
ENV_CLIENT_SECRET: Final[str] = "NAVER_CLIENT_SECRET"

# API Response codes
SUCCESS_CODE: Final[str] = "SUCCESS"

# Retry settings
INITIAL_RETRY_DELAY: Final[float] = 0.5  # seconds
MAX_RETRY_DELAY: Final[float] = 8.0  # seconds
RETRY_MULTIPLIER: Final[float] = 2.0
