import json
import subprocess
import sys
from pathlib import Path
from support import TemporaryProject, ROOT, FIXTURES
from route_request import route

class CliTests(TemporaryProject):
    def cli(self,script,*args):
        return subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],capture_output=True,text=True)

    def test_all_tools_help(self):
        for path in sorted((ROOT/'scripts').glob('*.py')):
            if path.stem=='common':continue
            with self.subTest(script=path.name):
                result=self.cli(path.name,'--help')
                self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                self.assertIn('usage:',result.stdout)

    def test_generation_audit_delivery_roundtrip(self):
        output=self.root/'candidate'
        generated=self.cli('generate_agents.py','--root',FIXTURES/'java-spring-boot-jpa','--output-dir',output)
        self.assertEqual(generated.returncode,0,generated.stdout+generated.stderr)
        candidate=output/'AGENTS.candidate.md'
        audit=self.cli('validate_agents.py','--file',candidate,'--root',FIXTURES/'java-spring-boot-jpa')
        self.assertEqual(audit.returncode,0,audit.stdout)
        target=self.root/'AGENTS.md'
        delivery=self.cli('deliver_file.py','--candidate',candidate,'--target',target)
        self.assertEqual(delivery.returncode,0,delivery.stdout)
        self.assertEqual(target.read_bytes(),candidate.read_bytes())
        refusal=self.cli('deliver_file.py','--candidate',candidate,'--target',target)
        self.assertEqual(refusal.returncode,2)

    def test_optimization_cli_keeps_original(self):
        original=self.write('AGENTS.md','# A\n## Rules\n- MUST preserve.\n- MUST preserve.\n')
        before=original.read_bytes()
        result=self.cli('optimize_agents.py','--file',original,'--candidate',self.root/'candidate.md')
        self.assertEqual(result.returncode,0,result.stdout)
        self.assertEqual(original.read_bytes(),before)
        self.assertEqual(len(json.loads(result.stdout)['automatic_removals']),1)

    def test_invalid_json_does_not_leak_raw_input(self):
        file=self.write('broken.json','{"apiKey": "not-real-but-private"')
        result=self.cli('generate_agents.py','--requirements',file,'--output-dir',self.root/'out')
        self.assertEqual(result.returncode,2)
        self.assertNotIn('not-real-but-private',result.stdout+result.stderr)
        json.loads(result.stdout)

    def test_existing_report_fails_safely(self):
        report=self.write('report.json','user original')
        result=self.cli('scan_project.py','--root',FIXTURES/'python-fastapi','--output',report)
        self.assertEqual(result.returncode,2)
        self.assertEqual(report.read_text(),'user original')

    def test_context_routing(self):
        cases=[('帮我生成 AGENTS.md',False,'CREATE'),('帮我生成 AGENTS.md',True,'DISCOVER'),
               ('Review and improve my AGENTS.md',True,'OPTIMIZE'),('Audit my AI coding instructions',False,'AUDIT'),
               ('生成多模块 AGENTS.md',True,'HIERARCHY'),('升级后检查 AGENTS.md',True,'UPDATE'),('迁移 AGENTS.md',True,'MIGRATE')]
        for text,has_project,mode in cases:
            with self.subTest(text=text):
                result=route(text,has_project)
                self.assertEqual(result['mode'],mode)
                self.assertFalse(result['scan_authorized'])

    def test_explanations_mentions_and_business_bugs_do_not_trigger(self):
        for text in ['AGENTS.md 是什么？','解释 Spring 的语法','修复登录 Bug，AGENTS.md 在根目录。','项目包含 AGENTS.md']:
            self.assertIsNone(route(text,True)['mode'])

    def test_twenty_scenarios_have_acceptance_contracts(self):
        records=json.loads((ROOT/'tests/scenarios/scenarios.json').read_text())
        self.assertEqual(len(records),20)
        for item in records:
            self.assertTrue(all(item.get(k) for k in ['user_input','preconditions','expected_mode','expected_output','assertions','forbidden']))
            self.assertEqual(item['host_execution'],'not-executed')
