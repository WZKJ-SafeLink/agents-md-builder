from support import TemporaryProject, rule
from detect_conflicts import detect_rules, text_candidates, validate_rule

class ConflictTests(TemporaryProject):
    def test_exclusive_same_scope_is_confirmed(self):
        result=detect_rules([rule(key='orm',value='jpa',exclusive=True),rule('TEST-RULE-002',key='orm',value='mybatis',exclusive=True,requirement='Use MyBatis')])
        self.assertEqual(result['findings'][0]['status'],'confirmed')

    def test_disjoint_modules_do_not_conflict(self):
        result=detect_rules([rule(scope=['api'],key='orm',value='jpa',exclusive=True),rule('TEST-RULE-002',scope=['worker'],key='orm',value='mybatis',exclusive=True)])
        self.assertEqual(result['findings'],[])

    def test_independent_module_is_scope_review(self):
        result=detect_rules([rule(scope=['.'],key='orm',value='jpa',exclusive=True),rule('TEST-RULE-002',independent=True,key='orm',value='mybatis',exclusive=True)])
        self.assertEqual(result['findings'][0]['status'],'candidate')

    def test_polarity_is_critical(self):
        result=detect_rules([rule(key='action',value='direct-access'),rule('TEST-RULE-002',severity='MUST_NOT',key='action',value='direct-access')])
        self.assertEqual(result['findings'][0]['severity'],'critical')

    def test_candidate_text_not_confirmed(self):
        result=text_candidates('- 必须使用 JPA\n- 必须使用 MyBatis','AGENTS.md')
        self.assertEqual(result[0]['status'],'candidate')

    def test_observed_cannot_be_mandatory(self):
        self.assertTrue(validate_rule(rule(classification='OBSERVED')))

    def test_standard_requires_source(self):
        self.assertTrue(validate_rule(rule(classification='STANDARD')))

    def test_duplicate_id_detected(self):
        result=detect_rules([rule(),rule(requirement='Use another mechanism')])
        self.assertEqual(result['findings'][0]['type'],'id-collision')

    def test_conflict_categories_supported(self):
        for category in ['technology','dependency-version','naming','architecture','data-access','transaction','security','user-fact','enterprise-recommendation']:
            with self.subTest(category=category):
                rules=[rule(category=category,key=category,value='a',exclusive=True),rule('TEST-RULE-002',category=category,key=category,value='b',exclusive=True)]
                self.assertTrue(detect_rules(rules)['findings'])

    def test_recommendation_against_required_is_candidate(self):
        result=detect_rules([rule(key='orm',value='jpa',exclusive=True),rule('TEST-RULE-002',classification='RECOMMENDED',severity='SHOULD',key='orm',value='mybatis',exclusive=True)])
        self.assertEqual(result['findings'][0]['status'],'candidate')
