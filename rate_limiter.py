from typing import Dict, Optional, Tuple
import time
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}

    async def is_allowed(self, ip: str) -> Tuple[bool, Optional[int]]:
        current_time = time.time()
        
        # Очистка старых запросов
        if ip in self.requests:
            self.requests[ip] = [t for t in self.requests[ip] if current_time - t < 60]
        
        # Добавление нового запроса
        if ip not in self.requests:
            self.requests[ip] = []
        
        self.requests[ip].append(current_time)
        
        # Проверка лимита
        if len(self.requests[ip]) > self.requests_per_minute:
            oldest_request = self.requests[ip][0]
            wait_time = int(60 - (current_time - oldest_request))
            return False, wait_time
        
        return True, None

# Создаем глобальный экземпляр rate_limiter
rate_limiter = RateLimiter()