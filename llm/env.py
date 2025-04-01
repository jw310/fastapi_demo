import os
from pathlib import Path

####################################
# Load .env file
####################################

LLM_DIR = Path(__file__).parent  # the path containing this file
# print(LLM_DIR)

BASE_DIR = LLM_DIR
# print(BASE_DIR)

try:
    from dotenv import find_dotenv, load_dotenv

    load_dotenv(find_dotenv(str(BASE_DIR / ".env")))
except ImportError:
    print("dotenv not installed, skipping...")



####################################
# DATA/FRONTEND BUILD DIR
####################################

DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data")).resolve()

####################################
# Database
####################################

# SQLite3
SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_SQLITE_DATABASE_URL")

# Check if the file exists
# if os.path.exists(f"{DATA_DIR}/ollama.db"):
#     # Rename the file
#     os.rename(f"{DATA_DIR}/ollama.db", f"{DATA_DIR}/webui.db")
#     # log.info("Database migrated from Ollama-WebUI successfully.")
# else:
#     pass

# DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DATA_DIR}/webui.db")

# # Replace the postgres:// with postgresql://
# if "postgres://" in DATABASE_URL:
#     DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

# DATABASE_SCHEMA = os.environ.get("DATABASE_SCHEMA", None)

DATABASE_POOL_SIZE = os.environ.get("DATABASE_POOL_SIZE", 0)

# if DATABASE_POOL_SIZE == "":
#     DATABASE_POOL_SIZE = 0
# else:
#     try:
#         DATABASE_POOL_SIZE = int(DATABASE_POOL_SIZE)
#     except Exception:
#         DATABASE_POOL_SIZE = 0

# DATABASE_POOL_MAX_OVERFLOW = os.environ.get("DATABASE_POOL_MAX_OVERFLOW", 0)

# if DATABASE_POOL_MAX_OVERFLOW == "":
#     DATABASE_POOL_MAX_OVERFLOW = 0
# else:
#     try:
#         DATABASE_POOL_MAX_OVERFLOW = int(DATABASE_POOL_MAX_OVERFLOW)
#     except Exception:
#         DATABASE_POOL_MAX_OVERFLOW = 0

# DATABASE_POOL_TIMEOUT = os.environ.get("DATABASE_POOL_TIMEOUT", 30)

# if DATABASE_POOL_TIMEOUT == "":
#     DATABASE_POOL_TIMEOUT = 30
# else:
#     try:
#         DATABASE_POOL_TIMEOUT = int(DATABASE_POOL_TIMEOUT)
#     except Exception:
#         DATABASE_POOL_TIMEOUT = 30

# DATABASE_POOL_RECYCLE = os.environ.get("DATABASE_POOL_RECYCLE", 3600)

# if DATABASE_POOL_RECYCLE == "":
#     DATABASE_POOL_RECYCLE = 3600
# else:
#     try:
#         DATABASE_POOL_RECYCLE = int(DATABASE_POOL_RECYCLE)
#     except Exception:
#         DATABASE_POOL_RECYCLE = 3600

# RESET_CONFIG_ON_START = (
#     os.environ.get("RESET_CONFIG_ON_START", "False").lower() == "true"
# )

# ENABLE_REALTIME_CHAT_SAVE = (
#     os.environ.get("ENABLE_REALTIME_CHAT_SAVE", "False").lower() == "true"
# )

####################################
# REDIS
####################################
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

####################################
# JWT
####################################
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

####################################
# AUDIT LOGGING
####################################
# ENABLE_AUDIT_LOGS = os.getenv("ENABLE_AUDIT_LOGS", "false").lower() == "true"
# # Where to store log file
# AUDIT_LOGS_FILE_PATH = f"{DATA_DIR}/audit.log"
# # Maximum size of a file before rotating into a new log file
# AUDIT_LOG_FILE_ROTATION_SIZE = os.getenv("AUDIT_LOG_FILE_ROTATION_SIZE", "10MB")
# # METADATA | REQUEST | REQUEST_RESPONSE
# AUDIT_LOG_LEVEL = os.getenv("AUDIT_LOG_LEVEL", "REQUEST_RESPONSE").upper()
# try:
#     MAX_BODY_LOG_SIZE = int(os.environ.get("MAX_BODY_LOG_SIZE") or 2048)
# except ValueError:
#     MAX_BODY_LOG_SIZE = 2048

# # Comma separated list for urls to exclude from audit
# AUDIT_EXCLUDED_PATHS = os.getenv("AUDIT_EXCLUDED_PATHS", "/chats,/chat,/folders").split(
#     ","
# )
# AUDIT_EXCLUDED_PATHS = [path.strip() for path in AUDIT_EXCLUDED_PATHS]
# AUDIT_EXCLUDED_PATHS = [path.lstrip("/") for path in AUDIT_EXCLUDED_PATHS]
