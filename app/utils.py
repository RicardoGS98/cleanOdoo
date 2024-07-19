import hashlib
import json
import os
import re
from functools import wraps

import redis
import unicodedata

r = redis.Redis(password=os.environ.get('REDIS_PW'), decode_responses=True)


def cache_decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Crear una clave única para la caché basada en el nombre de la función y sus argumentos
        key_base = f"{func.__name__}:{hashlib.md5(str(args).encode() + str(kwargs).encode()).hexdigest()}"

        # Intentar obtener los datos de la caché
        cached_data: str = r.get(key_base)
        if cached_data and os.environ.get('ENVIRONMENT') == 'local':
            return json.loads(cached_data)

        # Si los datos no están en la caché, ejecutar la función original
        result = func(self, *args, **kwargs)

        # Almacenar el resultado en la caché
        r.set(key_base, json.dumps(result))
        return result

    return wrapper


def normalized2upper(text):
    # Normalize the text to NFD (Normalization Form Decomposition)
    normalized_text = unicodedata.normalize('NFD', text).strip()
    # Filter out non-ASCII characters
    ascii_text = ''.join(c for c in normalized_text if unicodedata.category(c) != 'Mn')
    # Remove any remaining non-ASCII characters that might have been left
    return re.sub(r'[^\x00-\x7F]+', '', ascii_text).upper()
