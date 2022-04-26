import redis

from extension.project_config import get_config

# ConnectionError
redis_host = get_config().REDIS_HOST
redis_password = get_config().REDIS_PASSWORD
redis_client = redis.Redis(
    host=redis_host,
    port=6379,
    db=0,
    password=redis_password,
    health_check_interval=30,
    retry=3,
    max_connections=20,
)
