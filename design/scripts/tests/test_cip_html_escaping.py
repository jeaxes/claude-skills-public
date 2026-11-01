import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'cip' / 'render-html.py'
spec = importlib.util.spec_from_file_location('cip_renderer', SCRIPT)
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


class PresentationEscapingTests(unittest.TestCase):
    def test_untrusted_brief_and_deliverable_markup_is_text(self):
        attack = '<script>alert(1)</script> & "quoted"'
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as tmp:
            images = Path(tmp)
            (images / 'sample.png').write_bytes(b'png test data')
            output = images / 'presentation.html'
            brief = {'industry': {'Industry': attack}, 'style': {'Mood': attack, 'Style Name': attack}}
            info = dict.fromkeys(('title', 'concept', 'purpose', 'specs'), attack)
            with patch.object(renderer, 'get_cip_brief', return_value=brief), \
                 patch.object(renderer, 'get_deliverable_info', return_value=info), \
                 contextlib.redirect_stdout(io.StringIO()):
                renderer.generate_html(attack, 'example', images, output_path=output)
            html = output.read_text(encoding='utf-8')
            self.assertNotIn('<script>', html)
            self.assertNotIn('alt="<', html)
            self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', html)
            self.assertIn('&quot;quoted&quot;', html)


if __name__ == '__main__':
    unittest.main()
