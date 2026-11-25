import json
from support import TemporaryProject, FIXTURES, ROOT
from support import rule
from common import Scanner
from evaluate_agents import evaluate
from check_schema import check

class EvaluationTests(TemporaryProject):
    def test_partial_score_not_full_percentage(self):
        result=evaluate((FIXTURES/'existing-agents/AGENTS.md').read_text())
        self.assertEqual(result['coverage_percent'],80)
        self.assertEqual(result['assessed_weight'],80)
        self.assertIsNone(result['total'])
        self.assertIsNone(result['grade'])
        self.assertEqual(result['dimensions']['project_fit']['status'],'unverified')
    def test_reproducibility(self):
        text='# AGENTS.md\n## Project\n- MUST preserve changes and report unverified tests.'
        self.assertEqual(evaluate(text),evaluate(text))
    def test_critical_risk_caps_grade(self):
        text=(FIXTURES/'existing-agents/AGENTS.md').read_text()+'\n```sh\nrm -rf /\n```'
        result=evaluate(text,scan=Scanner(self.root).scan())
        self.assertEqual(result['grade'],'E')
        self.assertTrue(result['high_risk'])
    def test_data_section_only_when_applicable(self):
        a=evaluate('# A',scan=Scanner(self.root).scan())
        b=evaluate('# A',scan=Scanner(FIXTURES/'java-spring-boot-jpa').scan())
        self.assertNotIn('data-access',[c['check'] for c in a['dimensions']['completeness']['checks']])
        self.assertIn('data-access',[c['check'] for c in b['dimensions']['completeness']['checks']])
    def test_oversized_doc_loses_efficiency_points(self):
        text=(FIXTURES/'oversized-agents/AGENTS.md').read_text()
        result=evaluate(text)
        self.assertFalse(result['dimensions']['context_efficiency']['checks'][0]['passed'])
    def test_every_check_is_explainable(self):
        result=evaluate('# A')
        for dimension in result['dimensions'].values():
            for check_item in dimension['checks']:
                self.assertTrue({'check','weight','applicability','deduction','evidence','suggestion'}.issubset(check_item))
    def test_score_schema(self):
        schema=json.loads((ROOT/'assets/schemas/audit-report.schema.json').read_text())
        self.assertEqual(check(evaluate('# A'),schema),[])
    def test_schema_rejects_wrong_coverage(self):
        schema=json.loads((ROOT/'assets/schemas/audit-report.schema.json').read_text())
        data=evaluate('# A');data['coverage_percent']=101
        self.assertTrue(check(data,schema))

    def test_confirmed_structured_conflicts_cap_grade(self):
        rules=[rule(key='orm',value='jpa',exclusive=True),rule('TEST-RULE-002',key='orm',value='mybatis',exclusive=True)]
        result=evaluate('# AGENTS.md',scan=Scanner(self.root).scan(),rules=rules)
        self.assertEqual(result['grade'],'E')
        self.assertTrue(result['high_risk'])
