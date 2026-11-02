import re
import struct
import unittest
from pathlib import Path

from docsite import DIST

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / 'src/content/docs/dms'
SHOTS = ROOT / 'src/assets/screenshots'
IMAGE = re.compile(r'!\[([^\]]*)\]\(((?:\.\./)+assets/screenshots/([^)]+))\)')
DENY = re.compile(
    r'\bDMS_[A-Z_]+|kubernetes|kubectl|\bk3s\b|\bhelm\b|docker|postgres|opensearch|minio|alembic|webhook|openapi'
    r'|verapdf|euro-office|bagit|e-ark|grant-admin|environment variable|\bworker\b|\bcron\b|x-sdms|surogates runtime'
    r'|hash chain',
    re.I,
)


def pages():
    return sorted(PAGES.rglob('*.md'))


def split(path):
    text = path.read_text(encoding='utf-8')
    front, body = re.match(r'\A---\n(.*?)\n---\n(.*)\Z', text, re.S).groups()
    return front, body


class DmsContent(unittest.TestCase):
    def test_front_matter(self):
        for p in pages():
            front, _ = split(p)
            self.assertRegex(front, r'(?m)^title:\s*\S', p)
            self.assertRegex(front, r'(?m)^sidebar:\n\s+label:\s*\S', p)

    def test_no_em_dash_and_no_internals(self):
        for p in pages():
            text = p.read_text(encoding='utf-8')
            self.assertNotIn('\u2014', text, p)
            self.assertIsNone(DENY.search(text), f'{p}: {DENY.search(text)}')

    def test_opening_is_a_short_paragraph(self):
        for p in pages():
            _, body = split(p)
            first = body.strip().split('\n\n')[0]
            self.assertFalse(first.startswith(('#', '!', '|', '-', '1.', ':::', '<')), p)
            self.assertLessEqual(len(re.sub(r'[*`]|\[([^\]]*)\]\([^)]*\)', r'\1', first)), 250, p)

    def test_images(self):
        used = set()
        for p in pages():
            for alt, _, name in IMAGE.findall(p.read_text(encoding='utf-8')):
                self.assertTrue(alt.strip(), f'{p}: {name} has no alt text')
                self.assertRegex(name, r'^dms-[a-z0-9-]+\.png$')
                self.assertTrue((SHOTS / name).exists(), f'{p}: {name} missing')
                used.add(name)
        files = sorted(SHOTS.glob('dms-*.png'))
        for f in files:
            width, height = struct.unpack('>II', f.read_bytes()[16:24])
            self.assertEqual((width, height), (1600, 900), f.name)
            self.assertLessEqual(f.stat().st_size, 300_000, f.name)
            self.assertIn(f.name, used, f'{f.name} is used by no page')
        self.assertLessEqual(len(files), 120)
        self.assertLessEqual(len(pages()), 40)

    def test_llms_txt_names_the_product(self):
        self.assertIn('Surogate DMS', (DIST / 'llms.txt').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
