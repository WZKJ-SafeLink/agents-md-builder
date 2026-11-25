from support import TemporaryProject, FIXTURES
from common import Scanner, SafetyError
from discover_agents import discover
from analyze_structure import analyze
from extract_conventions import extract

class DiscoveryTests(TemporaryProject):
    def test_codex_override_chain(self):
        scan=Scanner(FIXTURES/'existing-agents').scan()
        result=discover(scan,'codex','api')
        self.assertEqual([i['path'] for i in result['effective_project_chain']],['AGENTS.md','api/AGENTS.override.md'])
        self.assertEqual(result['chain_bytes'],sum(x['bytes'] for x in result['effective_project_chain'])+2)

    def test_workbuddy_loading_not_assumed(self):
        result=discover(Scanner(FIXTURES/'existing-agents').scan(),'workbuddy','api')
        self.assertEqual(result['loading_status'],'unknown')
        self.assertEqual(result['effective_project_chain'],[])
        self.assertEqual(len(result['files']),3)

    def test_empty_override_falls_back(self):
        self.write('AGENTS.override.md','   ')
        self.write('AGENTS.md','# Policy')
        self.assertEqual(discover(Scanner(self.root).scan(),'codex')['effective_project_chain'][0]['path'],'AGENTS.md')

    def test_cwd_outside_scope(self):
        with self.assertRaises(SafetyError):discover(Scanner(self.root).scan(),'codex','../outside')

    def test_custom_fallback(self):
        self.write('TEAM.md','# Team')
        self.assertEqual(discover(Scanner(self.root).scan(),'codex',fallback=['TEAM.md'])['effective_project_chain'][0]['path'],'TEAM.md')

    def test_structure_uses_existing_anchors(self):
        scan=Scanner(FIXTURES/'java-spring-boot-jpa').scan()
        result=analyze(scan)
        self.assertTrue(result['anchors'])
        self.assertTrue(all((scan.root/a['path']).exists() for a in result['anchors']))

    def test_directory_names_do_not_confirm_architecture(self):
        self.write('domain/model.py','x=1')
        result=analyze(Scanner(self.root).scan())
        self.assertEqual(result['architecture'],[])
        self.assertEqual(result['directory_roles'][0]['confidence'],'low')

    def test_conventions_detect_multiple_clients_as_candidates(self):
        self.write('src/a.ts','fetch(url)')
        self.write('src/b.ts','axios.get(url)')
        result=extract(Scanner(self.root).scan())
        self.assertEqual(result['inconsistencies'][0]['status'],'candidate')
        self.assertTrue(all(o['classification']=='OBSERVED' for o in result['observations']))

    def test_convention_sample_is_bounded(self):
        for i in range(20):self.write(f'src/{i}.py','requests.get(url)')
        self.assertEqual(extract(Scanner(self.root).scan(),3)['sampled_files'],3)
