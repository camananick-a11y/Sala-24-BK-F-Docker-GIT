
import time
import json
from django.utils.deprecation import MiddlewareMixin

class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._start_time = time.time()

    def process_response(self, request, response):
        elapsed = (time.time() - getattr(request, "_start_time", time.time())) * 1000
        log = {
            "method": request.method,
            "path": request.get_full_path(),
            "status": getattr(response, "status_code", None),
            "time_ms": round(elapsed, 2),
        }
        print(json.dumps(log))
        return response

class AuthHeaderLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth = request.META.get("HTTP_AUTHORIZATION")
        if auth:
            print(json.dumps({"auth_header": auth}))
