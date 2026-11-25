"""Reproducible evidence-based document checks; semantic quality is not certified."""
from __future__ import annotations
import argparse
import re
from pathlib import Path
from typing import Any
from common import Scanner, emit, read_text, run_cli
from detect_stack import detect
from detect_conflicts import detect_rules
from validate_agents import validate

SCORING_VERSION = '1.0.0'
WEIGHTS = {'completeness': 20, 'project_fit': 20, 'actionability': 20, 'consistency': 10,
           'security': 10, 'testing_delivery': 10, 'context_efficiency': 10}


def evaluate(text: str, path: str = 'AGENTS.md', scan: Scanner | None = None,
             depth: str = 'standard', rules: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    audit = validate(text, path, scan)
    issues = audit['issues']
    if rules is not None:
        issues += detect_rules(rules)['findings']
    profile = detect(scan) if scan is not None else None
    dimensions: dict[str, Any] = {}

    def dimension(name: str, checks: list[tuple[str, float, bool, str, str]],
                  status: str = 'assessed') -> None:
        items = [{'check': title, 'weight': weight, 'applicability': status, 'passed': passed if status == 'assessed' else None,
                  'deduction': 0 if passed or status != 'assessed' else weight,
                  'evidence': evidence, 'suggestion': suggestion if not passed else ''}
                 for title, weight, passed, evidence, suggestion in checks]
        dimensions[name] = {'weight': WEIGHTS[name], 'status': status,
                            'score': round(sum(c[1] for c in checks if c[2]), 2) if status == 'assessed' else None,
                            'checks': items}

    data_relevant = bool(profile and any(t['category'] == 'database' or t['name'] in {'spring-data-jpa', 'mybatis', 'mybatis-plus'} for t in profile['technologies']))
    sections = [('project', r'项目|职责|overview|purpose|project'), ('stack', r'技术栈|language|framework|stack|运行环境|python|java|rust|typescript'),
                ('boundaries', r'边界|架构|boundary|boundaries|architecture|scope'), ('coding', r'编码|命名|开发规范|coding|style|naming'),
                ('errors', r'异常|错误|error|exception'), ('security', r'安全|密钥|隐私|security|secret|privacy'),
                ('testing', r'测试|验收|test|verification|acceptance')]
    if data_relevant:
        sections.append(('data-access', r'数据库|持久|repository|database|persistence|data access'))
    dimension('completeness', [(title, 20 / len(sections), bool(re.search(pattern, text, re.I)),
                                'Applicable document topic scan', 'Add only this applicable topic with executable constraints.') for title, pattern in sections])
    fit: list[tuple[str, float, bool, str, str]] = []
    if profile is not None:
        names = sorted({t['name'] for t in profile['technologies'] if t['category'] != 'language' and t['confidence'] == 'high'})
        stack_match = not names or all(name in text.lower() or name.replace('-', ' ') in text.lower() for name in names)
        fit = [('declared-technologies-mentioned', 4, stack_match, ', '.join(names) or 'No declared frameworks/databases', 'Align document with detected declarations; agent must review mismatches.'),
               ('declared-versions', 4, not any(i.get('code') == 'version-mismatch' for i in issues), 'Compared explicit nearby versions to exact static declarations', 'Resolve version mismatches and scope.'),
               ('path-anchors', 4, not any(i.get('code') == 'missing-reference' for i in issues), 'Checked backtick path candidates', 'Repair missing paths.'),
               ('commands-have-evidence', 4, not any(i.get('code') == 'unverified-command' for i in issues), 'Compared recognized commands to static declarations', 'Verify command and working directory.'),
               ('scan-coverage', 4, not scan.truncated, 'Scan truncated: ' + str(scan.truncated), 'Provide sufficient bounded evidence before claiming full fit.')]
    else:
        fit = [('project-evidence', 20, False, 'No authorized project evidence', 'Provide project files to assess fit.')]
    dimension('project_fit', fit, 'assessed' if profile is not None else 'unverified')
    rules = [line for line in text.splitlines() if re.match(r'^\s*[-*+]\s+', line)]
    actionable = sum(bool(re.search(r'必须|不得|禁止|应|检查|验证|复用|使用|运行|保留|报告|\b(?:must|should|may|use|run|verify|check|preserve|report|avoid|never)\b', line, re.I)) for line in rules)
    vague = sum(bool(re.search(r'最佳实践|高质量代码|best practices|clean code', line, re.I)) and not bool(re.search(r'验证|检查|when|verify|check', line, re.I)) for line in rules)
    dimension('actionability', [('has-rule-actions', 12, bool(rules) and actionable / len(rules) >= .65, f'{actionable}/{len(rules)} list items have action markers', 'Express conditions, actions and verification.'),
                                ('vague-rule-control', 8, bool(rules) and vague <= max(0, len(rules) // 10), f'{vague} vague candidate rules', 'Replace generic quality claims with measurable actions.')])
    dimension('consistency', [('explicit-conflict-candidates', 6, not any(i.get('type', '').endswith('scope-review') or (i.get('status') == 'confirmed' and i['severity'] in {'high', 'critical'}) for i in issues), 'Text candidates and optional structured rules; semantics unverified', 'Resolve candidate scopes through structured rules.'),
                             ('duplicate-control', 4, not any(i.get('code') == 'duplicate' for i in issues), 'Same-section exact duplicate checks', 'Merge exact duplicates.')])
    critical = [i for i in issues if i['severity'] in {'critical', 'high'} and (i.get('code') in {'credential', 'credential-assignment', 'destructive-command', 'instruction-injection', 'unauthorized-external-action', 'remote-execution'} or (i.get('type') and i.get('status') == 'confirmed'))]
    dimension('security', [('no-detected-high-risk', 6, not critical, f'{len(critical)} high-risk findings', 'Resolve high-risk findings before use.'),
                          ('privacy-and-change-boundaries', 4, bool(re.search(r'密钥|凭据|secret|credential', text, re.I)) and bool(re.search(r'授权|覆盖|用户.*改动|approval|overwrite|authorization', text, re.I)), 'Privacy and authorization markers', 'Document concrete secret and change protections.')])
    dimension('testing_delivery', [('test-command-or-honest-unknown', 4, bool(re.search(r'\b(?:test|unittest|pytest)\b|未确认.*(?:命令|测试)|没有.*测试|unknown.*test|not.*configured', text, re.I)), 'Test command or stated limitation', 'Use a real test command or state the missing evidence.'),
                                  ('acceptance', 3, bool(re.search(r'验收|交付|acceptance|delivery', text, re.I)), 'Acceptance topic', 'State change-specific acceptance requirements.'),
                                  ('honest-execution', 3, bool(re.search(r'未(?:执行|运行|验证)|not[- ]run|unverified|not executed', text, re.I)), 'Execution status marker', 'Distinguish recommended commands from executed checks.')])
    budget = {'minimal': 8192, 'standard': 16384, 'enterprise': 24576}[depth]
    dimension('context_efficiency', [('byte-budget', 5, audit['bytes'] <= budget, f"{audit['bytes']}/{budget} bytes; product recommendation", 'Remove tutorials or split meaningful module deltas.'),
                                    ('format-and-placeholders', 5, not any(i.get('code') in {'unclosed-fence', 'placeholder', 'duplicate'} for i in issues), 'Format, placeholder and duplicate checks', 'Repair incomplete or repeated content.')])
    assessed_weight = sum(d['weight'] for d in dimensions.values() if d['status'] == 'assessed')
    earned = round(sum(d['score'] or 0 for d in dimensions.values()), 2)
    normalized = round(100 * earned / assessed_weight, 2) if assessed_weight else None
    grade = next(label for cutoff, label in [(90, 'A'), (80, 'B'), (70, 'C'), (60, 'D'), (0, 'E')] if (normalized or 0) >= cutoff)
    if critical:
        grade = 'E'
    return {'scoring_version': SCORING_VERSION, 'kind': 'deterministic-document-checks',
            'earned': earned, 'assessed_weight': assessed_weight, 'coverage_percent': assessed_weight,
            'total': earned if assessed_weight == 100 else None, 'reference_normalized_score': normalized,
            'grade': grade if assessed_weight == 100 else None, 'reference_grade': grade,
            'high_risk': critical, 'dimensions': dimensions, 'issues': issues,
            'semantic_review': {'status': 'not-performed-by-script', 'required': ['Technical accuracy', 'Architecture fitness', 'Natural-language conflicts', 'Version-specific constraints']},
            'limitations': ['Document indicators only; not code quality, security certification or a full semantic score.']}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', required=True)
    parser.add_argument('--root')
    parser.add_argument('--depth', choices=['minimal', 'standard', 'enterprise'], default='standard')
    parser.add_argument('--output')
    parser.add_argument('--rules', help='Optional structured rules for confirmed conflict risk assessment')
    args = parser.parse_args()
    from common import load_json
    data = load_json(args.rules) if args.rules else None
    rules = data.get('rules', []) if isinstance(data, dict) else data
    emit(evaluate(read_text(Path(args.file)), Path(args.file).name, Scanner(args.root).scan() if args.root else None, args.depth, rules), args.output)
    return 0


if __name__ == '__main__':
    run_cli(main)
