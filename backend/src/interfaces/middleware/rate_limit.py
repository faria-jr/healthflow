"""Rate limiting middleware."""

import time
from typing import Dict, Tuple

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware."""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}
    
    async def dispatch(self, request: Request, call_next):
        """Rate limit requests by IP."""
        # Skip rate limiting for health checks
        if request.url.path == "/health":
            return await call_next(request)
        
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        
        # Clean old requests
        if client_ip in self.requests:
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if now - req_time < 60  # Keep only last minute
            ]
        
        # Check rate limit
        request_count = len(self.requests.get(client_ip, []))
        if request_count >= self.requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later.",
            )
        
        # Record request
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        self.requests[client_ip].append(now)
        
        return await call_next(request)
