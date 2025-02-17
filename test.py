from server import do_POST, do_GET
import unittest
import json

class TestServerRequests(unittest.TestCase):
    def test_get_request(self):
        # Simular una solicitud GET
        test_data = {
            'method': 'GET',
            'path': '/test',
            'headers': {'Content-Type': 'application/json'},
            'body': ''
        }
        
        # Ejecutar la solicitud
        response = do_GET(test_data)
        
        # Verificar la respuesta
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.body, dict)

if __name__ == '__main__':
    unittest.main()

