from typing import Any

def validate_param(param_name: str, default: Any=None):
    def decorator(func):
        def wrapper(self, objects):
            param = self.cleaned_data.get(param_name) or default
            if not param:
                return objects
            return func(self, objects, param)
        return wrapper
    return decorator