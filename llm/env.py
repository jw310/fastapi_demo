import os
import logging
import sys
from pathlib import Path

####################################
# Load .env file
####################################
# the path containing this file
LLM_DIR = Path(__file__).parent
BASE_DIR = LLM_DIR

try:
    from dotenv import find_dotenv, load_dotenv

    load_dotenv(find_dotenv(str(BASE_DIR / ".env")))
except ImportError:
    print("dotenv not installed, skipping...")

####################################
# DATA DIR
####################################
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data")).resolve()

####################################
# Static DIR
####################################
STATIC_DIR = Path(os.getenv("STATIC_DIR", BASE_DIR / "static")).resolve()

####################################
# File Upload DIR
####################################
UPLOAD_DIR = DATA_DIR / "uploads"
# mkdir 建立目錄 exist_ok 表示如果目錄已存在則不建立 parents=True 如果父目錄不存在，會自動建立所有必要的父目錄
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

####################################
# Database
####################################
DATABASE_URL = os.environ.get("DATABASE_URL")
TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")
# .env 檔案中可以設定 TEST_DATABASE_URL 為 true 來切換到測試環境的資料庫，然後 pytest
SWITCH_TEST_DATABASE = os.environ.get("SWITCH_TESTING_DATABASE", "false").lower()

# Check if the file exists
# if os.path.exists(f"{DATA_DIR}/data.db"):
#     pass

# # Replace the postgres:// with postgresql://
# if "postgres://" in DATABASE_URL:
#     DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

# DATABASE_SCHEMA = os.environ.get("DATABASE_SCHEMA", None)

DATABASE_POOL_SIZE = os.environ.get("DATABASE_POOL_SIZE", 0)

if DATABASE_POOL_SIZE == "":
    DATABASE_POOL_SIZE = 0
else:
    try:
        DATABASE_POOL_SIZE = int(DATABASE_POOL_SIZE)
    except Exception:
        DATABASE_POOL_SIZE = 0

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
ACCESS_TOKEN_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1))
REFRESH_TOKEN_SECRET_KEY = os.getenv("REFRESH_TOKEN_SECRET_KEY")
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 1))
ALGORITHM = os.getenv("JWT_ALGORITHM")

####################################
# LLM
####################################
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_CLAUDE_API_KEY = os.getenv("ANTHROPIC_CLAUDE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

####################################
# Vector Database
####################################
VECTOR_DB = os.environ.get("VECTOR_DB", "chroma")

# Chroma
CHROMA_DATA_PATH = f"{DATA_DIR}/vector_db"

# if VECTOR_DB == "chroma":
#     import chromadb

#     CHROMA_TENANT = os.environ.get("CHROMA_TENANT", chromadb.DEFAULT_TENANT)
#     CHROMA_DATABASE = os.environ.get("CHROMA_DATABASE", chromadb.DEFAULT_DATABASE)
#     CHROMA_HTTP_HOST = os.environ.get("CHROMA_HTTP_HOST", "")
#     CHROMA_HTTP_PORT = int(os.environ.get("CHROMA_HTTP_PORT", "8000"))
#     CHROMA_CLIENT_AUTH_PROVIDER = os.environ.get("CHROMA_CLIENT_AUTH_PROVIDER", "")
#     CHROMA_CLIENT_AUTH_CREDENTIALS = os.environ.get(
#         "CHROMA_CLIENT_AUTH_CREDENTIALS", ""
#     )
#     # Comma-separated list of header=value pairs
#     CHROMA_HTTP_HEADERS = os.environ.get("CHROMA_HTTP_HEADERS", "")
#     if CHROMA_HTTP_HEADERS:
#         CHROMA_HTTP_HEADERS = dict(
#             [pair.split("=") for pair in CHROMA_HTTP_HEADERS.split(",")]
#         )
#     else:
#         CHROMA_HTTP_HEADERS = None
#     CHROMA_HTTP_SSL = os.environ.get("CHROMA_HTTP_SSL", "false").lower() == "true"
# this uses the model defined in the Dockerfile ENV variable. If you dont use docker or docker based deployments such as k8s, the default embedding model will be used (sentence-transformers/all-MiniLM-L6-v2)

# Qdrant
QDRANT_URI = os.environ.get("QDRANT_URI", 'http://localhost:6333')
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")

# Pgvector
if "postgres://" in DATABASE_URL:
    # DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")
    PGVECTOR_DB_URL = os.environ.get("PGVECTOR_DB_URL", DATABASE_URL)
    if VECTOR_DB == "pgvector" and not PGVECTOR_DB_URL.startswith("postgres"):
        raise ValueError(
            "Pgvector requires setting PGVECTOR_DB_URL or using Postgres with vector extension as the primary database."
        )

if "postgres://" in DATABASE_URL:
    PGVECTOR_INITIALIZE_MAX_VECTOR_LENGTH = int(
        os.environ.get("PGVECTOR_INITIALIZE_MAX_VECTOR_LENGTH", "1536")
    )


####################################
# LOGGING
####################################

GLOBAL_LOG_LEVEL = os.environ.get("GLOBAL_LOG_LEVEL", "").upper()
if GLOBAL_LOG_LEVEL in logging.getLevelNamesMapping():
    logging.basicConfig(stream=sys.stdout, level=GLOBAL_LOG_LEVEL, force=True)
else:
    GLOBAL_LOG_LEVEL = "INFO"

log = logging.getLogger(__name__)
log.info(f"GLOBAL_LOG_LEVEL: {GLOBAL_LOG_LEVEL}")

# if "cuda_error" in locals():
#     log.exception(cuda_error)
#     del cuda_error

log_sources = [
    "MAIN",
    "MODELS",
]

SRC_LOG_LEVELS = {}

for source in log_sources:
    log_env_var = source + "_LOG_LEVEL"
    SRC_LOG_LEVELS[source] = os.environ.get(log_env_var, "").upper()
    if SRC_LOG_LEVELS[source] not in logging.getLevelNamesMapping():
        SRC_LOG_LEVELS[source] = GLOBAL_LOG_LEVEL
    log.info(f"{log_env_var}: {SRC_LOG_LEVELS[source]}")

# log.setLevel(SRC_LOG_LEVELS["CONFIG"])

####################################
# AUDIT LOGGING
####################################
ENABLE_AUDIT_LOGS = os.getenv("ENABLE_AUDIT_LOGS", "false").lower() == "true"
# Where to store log file
AUDIT_LOGS_FILE_PATH = f"{DATA_DIR}/audit.log"
# Maximum size of a file before rotating into a new log file
AUDIT_LOG_FILE_ROTATION_SIZE = os.getenv("AUDIT_LOG_FILE_ROTATION_SIZE", "10MB")
# METADATA | REQUEST | REQUEST_RESPONSE
AUDIT_LOG_LEVEL = os.getenv("AUDIT_LOG_LEVEL", "REQUEST_RESPONSE").upper()
try:
    MAX_BODY_LOG_SIZE = int(os.environ.get("MAX_BODY_LOG_SIZE") or 2048)
except ValueError:
    MAX_BODY_LOG_SIZE = 2048

# Comma separated list for urls to exclude from audit
AUDIT_EXCLUDED_PATHS = os.getenv("AUDIT_EXCLUDED_PATHS", "/chats,/chat,/folders").split(
    ","
)
AUDIT_EXCLUDED_PATHS = [path.strip() for path in AUDIT_EXCLUDED_PATHS]
AUDIT_EXCLUDED_PATHS = [path.lstrip("/") for path in AUDIT_EXCLUDED_PATHS]


####################################
# TASKS
####################################

DEFAULT_AUTOCOMPLETE_GENERATION_PROMPT_TEMPLATE = """### Task:
You are an autocompletion system. Continue the text in `<text>` based on the **completion type** in `<type>` and the given language.  

### **Instructions**:
1. Analyze `<text>` for context and meaning.
2. Use `<type>` to guide your output:
    - **General**: Provide a natural, concise continuation.
    - **Search Query**: Complete as if generating a realistic search query.
3. Start as if you are directly continuing `<text>`. Do **not** repeat, paraphrase, or respond as a model. Simply complete the text.  
4. Ensure the continuation:
    - Flows naturally from `<text>`.
    - Avoids repetition, overexplaining, or unrelated ideas.
5. If unsure, return: `{ "text": "" }`.

### **Output Rules**:
- Respond only in JSON format: `{ "text": "<your_completion>" }`.

### **Examples**:
#### Example 1:
Input:
<type>General</type>
<text>The sun was setting over the horizon, painting the sky</text>
Output:
{ "text": "with vibrant shades of orange and pink." }

#### Example 2:
Input:
<type>Search Query</type>
<text>Top-rated restaurants in</text>
Output:
{ "text": "New York City for Italian cuisine." }

---
### Context:
<chat_history>
{{MESSAGES:END:6}}
</chat_history>
<type>{{TYPE}}</type>
<text>{{PROMPT}}</text>
#### Output:
"""

DEFAULT_TITLE_GENERATION_PROMPT_TEMPLATE = """### Task:
Generate a concise, 3-5 word title with an emoji summarizing the chat history.
### Guidelines:
- The title should clearly represent the main theme or subject of the conversation.
- Use emojis that enhance understanding of the topic, but avoid quotation marks or special formatting.
- Write the title in the chat's primary language; default to English if multilingual.
- Prioritize accuracy over excessive creativity; keep it clear and simple.
### Output:
JSON format: { "title": "your concise title here" }
### Examples:
- { "title": "📉 Stock Market Trends" },
- { "title": "🍪 Perfect Chocolate Chip Recipe" },
- { "title": "Evolution of Music Streaming" },
- { "title": "Remote Work Productivity Tips" },
- { "title": "Artificial Intelligence in Healthcare" },
- { "title": "🎮 Video Game Development Insights" }
### Chat History:
<chat_history>
{{MESSAGES:END:2}}
</chat_history>"""


DEFAULT_IMAGE_PROMPT_GENERATION_PROMPT_TEMPLATE = """### Task:
Generate a detailed prompt for am image generation task based on the given language and context. Describe the image as if you were explaining it to someone who cannot see it. Include relevant details, colors, shapes, and any other important elements.

### Guidelines:
- Be descriptive and detailed, focusing on the most important aspects of the image.
- Avoid making assumptions or adding information not present in the image.
- Use the chat's primary language; default to English if multilingual.
- If the image is too complex, focus on the most prominent elements.

### Output:
Strictly return in JSON format:
{
    "prompt": "Your detailed description here."
}

### Chat History:
<chat_history>
{{MESSAGES:END:6}}
</chat_history>"""


DEFAULT_TAGS_GENERATION_PROMPT_TEMPLATE = """### Task:
Generate 1-3 broad tags categorizing the main themes of the chat history, along with 1-3 more specific subtopic tags.

### Guidelines:
- Start with high-level domains (e.g. Science, Technology, Philosophy, Arts, Politics, Business, Health, Sports, Entertainment, Education)
- Consider including relevant subfields/subdomains if they are strongly represented throughout the conversation
- If content is too short (less than 3 messages) or too diverse, use only ["General"]
- Use the chat's primary language; default to English if multilingual
- Prioritize accuracy over specificity

### Output:
JSON format: { "tags": ["tag1", "tag2", "tag3"] }

### Chat History:
<chat_history>
{{MESSAGES:END:6}}
</chat_history>"""



DEFAULT_QUERY_GENERATION_PROMPT_TEMPLATE = """### Task:
Analyze the chat history to determine the necessity of generating search queries, in the given language. By default, **prioritize generating 1-3 broad and relevant search queries** unless it is absolutely certain that no additional information is required. The aim is to retrieve comprehensive, updated, and valuable information even with minimal uncertainty. If no search is unequivocally needed, return an empty list.

### Guidelines:
- Respond **EXCLUSIVELY** with a JSON object. Any form of extra commentary, explanation, or additional text is strictly prohibited.
- When generating search queries, respond in the format: { "queries": ["query1", "query2"] }, ensuring each query is distinct, concise, and relevant to the topic.
- If and only if it is entirely certain that no useful results can be retrieved by a search, return: { "queries": [] }.
- Err on the side of suggesting search queries if there is **any chance** they might provide useful or updated information.
- Be concise and focused on composing high-quality search queries, avoiding unnecessary elaboration, commentary, or assumptions.
- Today's date is: {{CURRENT_DATE}}.
- Always prioritize providing actionable and broad queries that maximize informational coverage.

### Output:
Strictly return in JSON format:
{
    "queries": ["query1", "query2"]
}

### Chat History:
<chat_history>
{{MESSAGES:END:6}}
</chat_history>
"""


DEFAULT_TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE = """Available Tools: {{TOOLS}}

Your task is to choose and return the correct tool(s) from the list of available tools based on the query. Follow these guidelines:

- Return only the JSON object, without any additional text or explanation.

- If no tools match the query, return an empty array:
{
    "tool_calls": []
}

- If one or more tools match the query, construct a JSON response containing a "tool_calls" array with objects that include:
    - "name": The tool's name.
    - "parameters": A dictionary of required parameters and their corresponding values.

The format for the JSON response is strictly:
{
    "tool_calls": [
        {"name": "toolName1", "parameters": {"key1": "value1"}},
        {"name": "toolName2", "parameters": {"key2": "value2"}}
    ]
}"""


DEFAULT_EMOJI_GENERATION_PROMPT_TEMPLATE = """Your task is to reflect the speaker's likely facial expression through a fitting emoji. Interpret emotions from the message and reflect their facial expression using fitting, diverse emojis (e.g., 😊, 😢, 😡, 😱).

Message: ```{{prompt}}```"""

DEFAULT_MOA_GENERATION_PROMPT_TEMPLATE = """You have been provided with a set of responses from various models to the latest user query: "{{prompt}}"

Your task is to synthesize these responses into a single, high-quality response. It is crucial to critically evaluate the information provided in these responses, recognizing that some of it may be biased or incorrect. Your response should not simply replicate the given answers but should offer a refined, accurate, and comprehensive reply to the instruction. Ensure your response is well-structured, coherent, and adheres to the highest standards of accuracy and reliability.

Responses from models: {{responses}}"""


DEFAULT_CODE_INTERPRETER_PROMPT = """
#### Tools Available

1. **Code Interpreter**: `<code_interpreter type="code" lang="python"></code_interpreter>`
    - You have access to a Python shell that runs directly in the user's browser, enabling fast execution of code for analysis, calculations, or problem-solving.  Use it in this response.
    - The Python code you write can incorporate a wide array of libraries, handle data manipulation or visualization, perform API calls for web-related tasks, or tackle virtually any computational challenge. Use this flexibility to **think outside the box, craft elegant solutions, and harness Python's full potential**.
    - To use it, **you must enclose your code within `<code_interpreter type="code" lang="python">` XML tags** and stop right away. If you don't, the code won't execute. Do NOT use triple backticks.
    - When coding, **always aim to print meaningful outputs** (e.g., results, tables, summaries, or visuals) to better interpret and verify the findings. Avoid relying on implicit outputs; prioritize explicit and clear print statements so the results are effectively communicated to the user.  
    - After obtaining the printed output, **always provide a concise analysis, interpretation, or next steps to help the user understand the findings or refine the outcome further.**  
    - If the results are unclear, unexpected, or require validation, refine the code and execute it again as needed. Always aim to deliver meaningful insights from the results, iterating if necessary.  
    - **If a link to an image, audio, or any file is provided in markdown format in the output, ALWAYS regurgitate word for word, explicitly display it as part of the response to ensure the user can access it easily, do NOT change the link.**
    - All responses should be communicated in the chat's primary language, ensuring seamless understanding. If the chat is multilingual, default to English for clarity.

Ensure that the tools are effectively utilized to achieve the highest-quality analysis for the user."""

