import io
from types import SimpleNamespace
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer

SCRIPT = Path(__file__).resolve().parents[1] / 'dashboard.py'
spec = importlib.util.spec_from_file_location('dashboard', SCRIPT)
dashboard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dashboard)


class DashboardBoundaryTests(unittest.TestCase):
    port = 8765

    def request(self, body, headers=None):
        values = {'Host': f'127.0.0.1:{self.port}',
                  'Content-Type': 'application/json',
                  'Content-Length': str(len(body.encode()))}
        values.update(headers or {})
        request = 'POST /api/scan HTTP/1.0\r\n' + ''.join(
            f'{key}: {value}\r\n' for key, value in values.items())
        raw = (request + '\r\n' + body).encode()

        class Connection:
            output = bytearray()
            def makefile(self, *args):
                return io.BytesIO(raw)
            def sendall(self, data):
                self.output.extend(data)

        connection = Connection()
        dashboard.Handler(connection, ('127.0.0.1', 12345),
                          SimpleNamespace(server_port=self.port))
        head, payload = bytes(connection.output).split(b'\r\n\r\n', 1)
        return int(head.split()[1]), json.loads(payload)

    def test_host_rebinding_rejected(self):
        status, _ = self.request('{}', {'Host': f'evil.example:{self.port}'})
        self.assertEqual(status, 403)

    def test_cross_origin_rejected(self):
        status, _ = self.request('{}', {'Origin': 'https://evil.example'})
        self.assertEqual(status, 403)

    def test_simple_content_type_rejected(self):
        status, _ = self.request('{}', {'Content-Type': 'text/plain'})
        self.assertEqual(status, 400)

    def test_excessive_length_rejected_before_read(self):
        status, _ = self.request('{}', {'Content-Length': str(dashboard.MAX_BODY_BYTES + 1)})
        self.assertEqual(status, 400)

    def test_non_object_rejected(self):
        self.assertEqual(self.request('[]')[0], 400)

    def test_local_scan_still_works(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as tmp:
            target = Path(tmp) / 'demo.txt'
            target.write_text('ordinary text', encoding='utf-8')
            status, result = self.request(json.dumps({'path': str(target)}), {
                'Origin': f'http://127.0.0.1:{self.port}'})
            self.assertEqual(status, 200)
            self.assertTrue(result['ok'])
            self.assertEqual(result['findings'], [])


if __name__ == '__main__':
    unittest.main()

