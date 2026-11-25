import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile
from support import TemporaryProject, ROOT, FIXTURES, rule
from package_skill import flatten_payload, package
from validate_skill import validate_skill, frontmatter
from common import SafetyError
from safe_extract import extract_zip

class PackageTests(TemporaryProject):
    def test_generic_roundtrip_manifest_and_exclusions(self):
        archive=self.root/'generic.zip'
        result=package(ROOT,archive)
        self.assertTrue(result['extracted_validation']['valid'])
        self.assertEqual(result['marketplace_import'],'not-performed')
        with zipfile.ZipFile(archive) as z:
            names=z.namelist()
            prefix='agents-md-builder/'
            self.assertIn(prefix+'SKILL.md',names)
            for readme in ['README.md','README.en.md','README.ja.md','README.zh-CN.md']:
                self.assertIn(prefix+readme,names)
                text=z.read(prefix+readme).decode('utf-8')
                self.assertIn('(README.md)',text)
                self.assertIn('(README.ja.md)',text)
                self.assertIn('(README.zh-CN.md)',text)
            self.assertNotIn(prefix+'AGENTS.md',names)
            self.assertTrue(all('/tests/' not in n and '__pycache__' not in n and '/release/' not in n for n in names))
            manifest=json.loads(z.read(prefix+'MANIFEST.json'))
            for name,info in manifest['files'].items():
                self.assertEqual(hashlib.sha256(z.read(prefix+name)).hexdigest(),info['sha256'])
            metadata,_=frontmatter(z.read(prefix+'SKILL.md').decode())
            self.assertEqual(set(metadata),{'name','description'})

    def test_workbuddy_metadata(self):
        archive=self.root/'workbuddy.zip'
        result=package(ROOT,archive,'workbuddy',{'author':'Safe Link'})
        self.assertTrue(result['extracted_validation']['valid'])
        with zipfile.ZipFile(archive) as z:
            metadata,_=frontmatter(z.read('SKILL.md').decode())
            self.assertEqual(metadata['author'],'Safe Link')
            self.assertEqual(metadata['version'],(ROOT/'VERSION').read_text().strip())
            self.assertIn('display_name_en',metadata)

    def test_workbuddy_archive_has_no_wrapper_or_nested_resource_directories(self):
        archive=self.root/'workbuddy.zip'
        result=package(ROOT,archive,'workbuddy',{'author':'Safe Link'})
        self.assertEqual(result['max_member_path_parts'],2)
        with zipfile.ZipFile(archive) as z:
            names=z.namelist()
            self.assertIn('SKILL.md',names)
            for readme in ['README.md','README.en.md','README.ja.md','README.zh-CN.md']:
                self.assertIn(readme,names)
                text=z.read(readme).decode('utf-8')
                self.assertIn('(README.md)',text)
                self.assertIn('(README.ja.md)',text)
                self.assertIn('(README.zh-CN.md)',text)
            self.assertTrue(all(len(Path(name).parts)<=2 for name in names))
            self.assertFalse(any(name.startswith('agents-md-builder/') for name in names))
            self.assertIn('references/core-workflow.md',names)
            self.assertIn('references/languages-java.md',names)
            self.assertIn('assets/schemas-rule.schema.json',names)
            self.assertIn('assets/templates-AGENTS.template.md',names)
            self.assertEqual(sum(n.startswith('references/') for n in names),len([p for p in (ROOT/'references').rglob('*') if p.is_file()]))
            self.assertEqual(sum(n.startswith('assets/') for n in names),len([p for p in (ROOT/'assets').rglob('*') if p.is_file()]))
            manifest=json.loads(z.read('MANIFEST.json'))
            self.assertEqual(manifest['source_paths']['references/frameworks/spring-data-jpa.md'],'references/frameworks-spring-data-jpa.md')
            for name,info in manifest['files'].items():
                self.assertEqual(hashlib.sha256(z.read(name)).hexdigest(),info['sha256'])

    def test_workbuddy_extracted_cli_generates_same_chinese_and_english_rules(self):
        from pathlib import Path
        from common import Scanner
        from detect_stack import detect
        from generate_agents import generate
        archive=self.root/'workbuddy.zip'
        package(ROOT,archive,'workbuddy',{'author':'Safe Link'})
        installed=self.root/'agents-md-builder'
        extract_zip(archive,installed)
        profile=detect(Scanner(FIXTURES/'java-spring-boot-jpa').scan())
        for language in ['zh','en']:
            output=self.root/language
            result=subprocess.run([sys.executable,'-B',str(installed/'scripts/generate_agents.py'),
                                   '--root',str(FIXTURES/'java-spring-boot-jpa'),'--output-dir',str(output),
                                   '--language',language],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertEqual((output/'AGENTS.candidate.md').read_text(),generate(profile,language)['AGENTS.candidate.md'])
            for reference in json.loads(result.stdout)['references']:
                self.assertTrue((installed/reference).is_file(),reference)

    def test_workbuddy_extracted_schema_and_source_registry_remain_usable(self):
        archive=self.root/'workbuddy.zip'
        package(ROOT,archive,'workbuddy',{'author':'Safe Link'})
        installed=self.root/'agents-md-builder'
        extract_zip(archive,installed)
        source='https://docs.python.org/3/library/pathlib.html'
        rules=self.write('rules.json',json.dumps([rule(sources=[source],migration_class='general')]))
        profile=self.write('profile.json','{"technologies":[]}')
        migrated=subprocess.run([sys.executable,'-B',str(installed/'scripts/migrate_rules.py'),
                                 '--rules',str(rules),'--profile',str(profile)],capture_output=True,text=True)
        self.assertEqual(migrated.returncode,0,migrated.stdout+migrated.stderr)
        self.assertEqual(json.loads(migrated.stdout)['candidate_rules'][0]['sources'],[source])
        one_rule=self.write('one-rule.json',json.dumps(rule()))
        checked=subprocess.run([sys.executable,'-B',str(installed/'scripts/check_schema.py'),
                                '--file',str(one_rule),'--schema',str(installed/'assets/schemas-rule.schema.json')],capture_output=True,text=True)
        self.assertEqual(checked.returncode,0,checked.stdout+checked.stderr)

    def test_flattening_rewrites_relative_links_anchors_and_inline_paths(self):
        payload={
            'SKILL.md':b'[workflow](references/core/workflow.md#steps) assets/templates',
            'references/INDEX.md':b'[workflow](core/workflow.md)',
            'references/core/workflow.md':b'[schema](../../assets/schemas/rule.schema.json) assets/schemas/rule.schema.json',
            'assets/schemas/rule.schema.json':b'{}',
        }
        flattened,mapping=flatten_payload(payload)
        self.assertIn(b'(references/core-workflow.md#steps)',flattened['SKILL.md'])
        self.assertIn(b'(core-workflow.md)',flattened['references/INDEX.md'])
        self.assertIn(b'(../assets/schemas-rule.schema.json)',flattened['references/core-workflow.md'])
        self.assertNotIn(b'assets/schemas/',flattened['references/core-workflow.md'])

    def test_flattening_rejects_resource_name_collisions(self):
        for payload in [
            {'references/core/workflow.md':b'a','references/core-workflow.md':b'b'},
            {'references/core/Guide.md':b'a','references/core-guide.md':b'b'},
        ]:
            with self.assertRaises(SafetyError):flatten_payload(payload)

    def test_workbuddy_validator_rejects_nested_installed_resources(self):
        archive=self.root/'workbuddy.zip'
        package(ROOT,archive,'workbuddy',{'author':'Safe Link'})
        installed=self.root/'agents-md-builder'
        extract_zip(archive,installed)
        extra=installed/'references/extra/nested.md'
        extra.parent.mkdir();extra.write_text('# Nested')
        result=validate_skill(installed,'workbuddy')
        self.assertFalse(result['valid'])
        self.assertTrue(any('two' in e['issue'] or 'one resource directory' in e['issue'] for e in result['errors']))

    def test_workbuddy_reproducible_bytes(self):
        first=self.root/'first.zip';second=self.root/'second.zip'
        package(ROOT,first,'workbuddy',{'author':'Safe Link'})
        package(ROOT,second,'workbuddy',{'author':'Safe Link'})
        self.assertEqual(first.read_bytes(),second.read_bytes())

    def test_publisher_required(self):
        with self.assertRaises(SafetyError):package(ROOT,self.root/'invalid.zip','workbuddy',{})
        self.assertFalse((self.root/'invalid.zip').exists())

    def test_reproducible_bytes(self):
        a=self.root/'a.zip';b=self.root/'b.zip'
        package(ROOT,a);package(ROOT,b)
        self.assertEqual(a.read_bytes(),b.read_bytes())

    def test_archive_not_overwritten(self):
        archive=self.write('existing.zip','user archive')
        with self.assertRaises(SafetyError):package(ROOT,archive)
        self.assertEqual(archive.read_text(),'user archive')

    def test_reject_link_in_runtime(self):
        copied=self.root/'agents-md-builder'
        shutil.copytree(ROOT,copied,ignore=shutil.ignore_patterns('dist','__pycache__','.git'))
        (copied/'assets/linked.txt').symlink_to(copied/'LICENSE')
        with self.assertRaises(SafetyError):package(copied,self.root/'invalid.zip')

    def test_reject_known_credential_in_runtime(self):
        copied=self.root/'agents-md-builder'
        shutil.copytree(ROOT,copied,ignore=shutil.ignore_patterns('dist','__pycache__','.git'))
        (copied/'assets/accidental.txt').write_text('sk-'+'z'*30)
        with self.assertRaises(SafetyError):package(copied,self.root/'invalid.zip')

    def test_source_skill_validation(self):
        result=validate_skill(ROOT)
        self.assertTrue(result['valid'],result['errors'])

    def test_generic_secret_assignment_rejected(self):
        from package_skill import secret_literal
        self.assertTrue(secret_literal('apiKey: "fictional-release-secret"','.yml'))
        self.assertTrue(secret_literal('CLIENT_SECRET = "fictional-release-secret"','.py'))
        self.assertFalse(secret_literal('credential=[REDACTED]','.md'))
