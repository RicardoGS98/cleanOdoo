import hashlib
import json
import unittest
from unittest.mock import patch

# Asumiendo que utils.py está en el mismo directorio
from app.utils import cache_decorator, normalized2upper


class TestUtils(unittest.TestCase):

    @patch('app.utils.r', autospec=True)
    def test_cache_decorator_with_cache_hit(self, mock_redis):
        # Simular un hit en la caché
        mock_redis.get.return_value = json.dumps({'result': 'cached'})

        class TestClass:
            @cache_decorator
            def method_to_cache(self, _):
                return {'result': 'original'}

        instance = TestClass()
        result = instance.method_to_cache('test')

        self.assertEqual(result, {'result': 'cached'})
        mock_redis.get.assert_called_once()

    @patch('app.utils.r', autospec=True)
    def test_cache_decorator_with_cache_miss(self, mock_redis):
        # Simular un miss en la caché
        mock_redis.get.return_value = None

        class TestClass:
            @cache_decorator
            def method_to_cache(self, _):
                return {'result': 'original'}

        instance = TestClass()
        result = instance.method_to_cache('test')

        self.assertEqual(result, {'result': 'original'})
        mock_redis.set.assert_called_once_with(
            f'method_to_cache:{hashlib.md5(str(("test",)).encode() + str({}).encode()).hexdigest()}',
            json.dumps({'result': 'original'})
        )

    def test_normalized2upper(self):
        # Prueba con un texto normal
        text = "Café"
        result = normalized2upper(text)
        self.assertEqual(result, "CAFE")

        # Prueba con un texto con caracteres especiales
        text = "El niño jugó fútbol"
        result = normalized2upper(text)
        self.assertEqual(result, "EL NINO JUGO FUTBOL")

        # Prueba con un texto con caracteres no ASCII
        text = "こんにちは"
        result = normalized2upper(text)
        self.assertEqual(result, "")

        # Prueba con un texto ya en mayúsculas
        text = "HELLO WORLD"
        result = normalized2upper(text)
        self.assertEqual(result, "HELLO WORLD")


if __name__ == '__main__':
    unittest.main()
