import asyncio
import functools
from typing import Callable, Type, Any
from aiohttp.client import ClientConnectionError

def retry_decorator(
    max_retries: int = 5,
    retry_interval: float = 1,
):
    """
    API请求重试装饰器工厂
    
    :param max_retries: 最大重试次数
    :param retry_interval: 重试间隔（秒）
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            retry_count = 0
            while True:
                try:
                    result = await func(*args, **kwargs)
                    return result
                except ClientConnectionError:
                    if retry_count > max_retries:
                        raise
                    retry_count += 1
                    await asyncio.sleep(retry_interval)
        return wrapper
    return decorator