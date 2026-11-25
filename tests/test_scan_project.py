import json
from support import TemporaryProject, FIXTURES
from common import Scanner, Limits, SafetyError

class ScanTests(TemporaryProject):
    def test_inventory_types_and_config(self):
        self.write('package.json', '{}')
        self.write('src/main.ts', 'export const value = 1;')
        report = Scanner(self.root).scan().report()
        self.assertEqual(report['file_count'], 2)
        self.assertEqual(report['types']['.ts'], 1)
        self.assertIn('package.json', report['configurations'])

    def test_standard_exclusions(self):
        for name in ['.git', 'node_modules', 'vendor', 'target', 'dist', '.venv']:
            self.write(name + '/hidden.py', 'raise RuntimeError()')
        self.write('main.py', 'x=1')
        scan = Scanner(self.root).scan()
        self.assertEqual(list(scan.contents), ['main.py'])

    def test_sensitive_excluded_even_with_include(self):
        for name in ['.env', '.env.dev', 'server.key', 'credentials.json', 'id_rsa', 'secret.pem']:
            self.write(name, 'not-real-sensitive-content')
        scan = Scanner(self.root, include=['*']).scan()
        self.assertEqual(scan.contents, {})

    def test_gitignore_negation(self):
        self.write('.gitignore', '*.log\n!keep.log\n')
        self.write('drop.log', 'drop')
        self.write('keep.log', 'keep')
        scan = Scanner(self.root).scan()
        self.assertNotIn('drop.log', scan.contents)
        self.assertIn('keep.log', scan.contents)

    def test_nested_gitignore_is_local(self):
        self.write('a/.gitignore', '/local.txt\n')
        self.write('a/local.txt', 'ignored')
        self.write('a/nested/local.txt', 'included')
        self.write('b/local.txt', 'included')
        files = Scanner(self.root).scan().contents
        self.assertNotIn('a/local.txt', files)
        self.assertIn('a/nested/local.txt', files)
        self.assertIn('b/local.txt', files)

    def test_explicit_include_overrides_ordinary_ignore(self):
        self.write('.gitignore', 'generated/\n')
        self.write('generated/schema.py', 'x=1')
        scan = Scanner(self.root, include=['generated/schema.py']).scan()
        self.assertIn('generated/schema.py', scan.contents)

    def test_explicit_exclude(self):
        self.write('src/ignored.py', 'x=1')
        self.assertNotIn('src/ignored.py', Scanner(self.root, exclude=['src/']).scan().contents)

    def test_gitignore_classes_escaped_names_and_double_star(self):
        self.write('.gitignore','file[0-9].txt\n\\#private.txt\n\\!private.txt\nspace\\ \na/**/generated.py\n')
        ignored=['file2.txt','#private.txt','!private.txt','space ','a/generated.py','a/b/c/generated.py']
        for name in ignored:self.write(name,'ignored')
        self.write('filex.txt','included')
        files=Scanner(self.root).scan().contents
        self.assertTrue(all(name not in files for name in ignored))
        self.assertIn('filex.txt',files)

    def test_ignore_rule_budget_is_bounded_and_reported(self):
        self.write('.gitignore','a'*600+'\n'+'\n'.join('ignored'+str(i) for i in range(2010)))
        self.write('visible.py','x=1')
        scan=Scanner(self.root).scan()
        self.assertTrue(scan.truncated)
        self.assertGreater(scan.skipped['ignore-rule-budget'],0)
        self.assertIn('visible.py',scan.contents)

    def test_malformed_character_class_is_literal(self):
        self.write('.gitignore','bad[\n')
        self.write('good.txt','x')
        self.assertIn('good.txt',Scanner(self.root).scan().contents)

    def test_file_limit_bounds_directory_entries(self):
        for i in range(30): self.write(f'f{i}.py', 'x=1')
        scan = Scanner(self.root, Limits(max_files=7)).scan()
        self.assertLessEqual(scan.entries, 7)
        self.assertTrue(scan.truncated)

    def test_depth_limit(self):
        self.write('a/b/c/deep.py', 'x=1')
        scan = Scanner(self.root, Limits(max_depth=1)).scan()
        self.assertNotIn('a/b/c/deep.py', scan.contents)
        self.assertTrue(scan.truncated)

    def test_single_file_limit(self):
        self.write('large.py', 'x' * 500)
        scan = Scanner(self.root, Limits(max_file_bytes=100)).scan()
        self.assertEqual(scan.contents, {})
        self.assertEqual(scan.total_bytes, 0)

    def test_total_byte_limit(self):
        for i in range(5): self.write(f'{i}.py', 'x' * 80)
        scan = Scanner(self.root, Limits(max_total_bytes=170)).scan()
        self.assertLessEqual(scan.total_bytes, 170)
        self.assertLessEqual(len(scan.contents), 2)

    def test_binary_and_non_utf8_excluded(self):
        (self.root/'image.bin').write_bytes(b'abc\x00def')
        (self.root/'invalid.txt').write_bytes(b'\xff\xfe')
        scan = Scanner(self.root).scan()
        self.assertFalse(scan.contents)
        self.assertEqual(scan.skipped['binary'], 1)

    def test_report_contains_no_file_bodies(self):
        marker='fictional-password-must-not-be-reported'
        self.write('application.yml', 'password: ' + marker)
        report=json.dumps(Scanner(self.root).scan().report())
        self.assertNotIn(marker, report)

    def test_empty_directory(self):
        report=Scanner(self.root).scan().report()
        self.assertEqual(report['file_count'], 0)
        self.assertFalse(report['truncated'])

    def test_invalid_limits(self):
        with self.assertRaises(SafetyError): Limits(max_files=0)
