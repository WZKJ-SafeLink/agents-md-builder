from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests' / 'fixtures'
sys.path.insert(0, str(ROOT / 'scripts'))

class TemporaryProject(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='agents-test-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')
        return target


def rule(identifier='TEST-RULE-001', **changes):
    return {'id': identifier, 'title': 'Data access boundary', 'category': 'data-access',
            'classification': 'USER_REQUIRED', 'severity': 'MUST', 'scope': ['backend'],
            'condition': 'Adding persistence code', 'requirement': 'Use JPA for persistence',
            'verification': {'type': 'review', 'description': 'Inspect persistence imports'},
            'sources': [], 'confidence': 'high', **changes}
