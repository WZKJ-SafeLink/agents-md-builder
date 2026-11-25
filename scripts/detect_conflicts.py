"""Detect explicit structured conflicts; text matches remain review candidates."""
from __future__ import annotations
import argparse
import re
from pathlib import Path
from typing import Any
from common import emit, load_json, read_text, redact, run_cli

CLASSIFICATIONS = {'STANDARD', 'RECOMMENDED', 'PROJECT_REQUIRED', 'USER_REQUIRED', 'OBSERVED', 'PROPOSED'}
STRENGTHS = {'MUST', 'MUST_NOT', 'SHOULD', 'MAY'}


def validate_rule(rule: dict[str, Any]) -> list[str]:
    if not isinstance(rule, dict):
        return ['rule must be an object']
    errors = []
    for name in ('id', 'title', 'category', 'condition', 'requirement'):
        if not isinstance(rule.get(name), str) or not rule[name].strip():
            errors.append(name + ': required non-empty string')
    if rule.get('classification') not in CLASSIFICATIONS:
        errors.append('classification: invalid')
    if rule.get('severity') not in STRENGTHS:
        errors.append('severity: invalid')
    if not isinstance(rule.get('id'), str) or not re.fullmatch(r'[A-Z][A-Z0-9-]+-\d{3}', rule.get('id', '')):
        errors.append('id: stable uppercase rule ID required')
    if rule.get('confidence') not in {'high', 'medium', 'low'}:
        errors.append('confidence: invalid')
    if not isinstance(rule.get('sources'), list) or any(not isinstance(source, str) for source in rule.get('sources', [])):
        errors.append('sources: string array required')
    if not isinstance(rule.get('scope'), list) or not rule['scope'] or any(not isinstance(s, str) or not s for s in rule['scope']):
        errors.append('scope: non-empty string array required')
    if rule.get('classification') in {'OBSERVED', 'PROPOSED'} and rule.get('severity') in {'MUST', 'MUST_NOT'}:
        errors.append('observations and proposals cannot be mandatory')
    if rule.get('classification') == 'STANDARD' and not rule.get('sources'):
        errors.append('STANDARD requires sources')
    if not isinstance(rule.get('verification'), dict) or not rule['verification'].get('description'):
        errors.append('verification.description: required')
    return errors


def scope_overlap(left: list[str], right: list[str]) -> bool:
    for a in left:
        for b in right:
            a, b = a.rstrip('/'), b.rstrip('/')
            if a in {'.', '*', 'global'} or b in {'.', '*', 'global'} or a == b or a.startswith(b + '/') or b.startswith(a + '/'):
                return True
    return False


def detect_rules(rules: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(rules, list) or len(rules) > 2000:
        raise ValueError('rules must be an array of at most 2000 entries')
    findings = []
    valid = []
    for index, rule in enumerate(rules):
        errors = validate_rule(rule)
        if errors:
            findings.append({'type': 'invalid-rule', 'status': 'confirmed', 'severity': 'high',
                             'rules': [rule.get('id', str(index)) if isinstance(rule, dict) else str(index)], 'locations': [rule.get('evidence', {}) if isinstance(rule, dict) else {}],
                             'evidence': errors, 'impact': 'Rule provenance or execution contract is invalid.',
                             'suggestion': 'Repair the structured rule before conflict comparison.'})
        else:
            valid.append(rule)
    for i, left in enumerate(valid):
        for right in valid[i + 1:]:
            overlap = scope_overlap(left['scope'], right['scope'])
            strong = all(item['severity'] in {'MUST', 'MUST_NOT'} for item in (left, right))
            kind = None
            status, severity = 'candidate', 'medium'
            if left['id'] == right['id'] and left != right:
                kind, status, severity = 'id-collision', 'confirmed', 'high'
            elif overlap and left.get('key') and left.get('key') == right.get('key'):
                if left.get('value') == right.get('value') and {left['severity'], right['severity']} == {'MUST', 'MUST_NOT'}:
                    kind, status, severity = left['category'] + '-polarity', 'confirmed', 'critical'
                elif left.get('value') != right.get('value') and left.get('exclusive') and right.get('exclusive'):
                    independent = left.get('independent') or right.get('independent')
                    if strong and not independent:
                        kind, status, severity = left['category'] + '-exclusive', 'confirmed', 'high'
                    else:
                        kind = left['category'] + ('-scope-review' if independent else '-preference')
            elif overlap and re.sub(r'\s+', '', left['requirement']).casefold() == re.sub(r'\s+', '', right['requirement']).casefold():
                kind = 'duplicate-rule'
            if kind:
                findings.append({'type': kind, 'status': status, 'severity': severity,
                                 'rules': [left['id'], right['id']],
                                 'locations': [left.get('evidence', {}), right.get('evidence', {})],
                                 'scope': [left['scope'], right['scope']],
                                 'evidence': [redact(left['requirement']), redact(right['requirement'])],
                                 'impact': 'Instructions may disagree or waste context within overlapping scope.',
                                 'suggestion': 'Make scope and exceptions explicit; preserve confirmed requirements and resolve with the user when needed.'})
    return {'findings': findings, 'rule_count': len(rules),
            'limitations': ['Only explicit structured keys, polarity, scopes and duplicate text are compared. Natural-language semantics require agent review.']}


def text_candidates(text: str, path: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    findings = []
    # No automatic assertion that two framework names alone form a conflict.
    mandatory = [(i, line) for i, line in enumerate(lines, 1) if re.search(r'\bMUST\b|必须|不得|禁止', line)]
    for (a, left), (b, right) in zip(mandatory, mandatory[1:]):
        if any(x in left.lower() for x in ('jpa', 'mybatis')) and any(x in right.lower() for x in ('jpa', 'mybatis')) and ('jpa' in left.lower()) != ('jpa' in right.lower()):
            findings.append({'type': 'data-access-scope-review', 'status': 'candidate', 'severity': 'medium',
                             'path': path, 'line': a, 'related_line': b, 'evidence': redact(left),
                             'impact': 'Different ORM requirements may overlap.',
                             'suggestion': 'Extract structured scopes and exclusive keys before confirming a conflict.'})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--rules', help='JSON array or object containing rules')
    group.add_argument('--file', help='Markdown; produces candidates only')
    parser.add_argument('--output')
    args = parser.parse_args()
    if args.rules:
        data = load_json(args.rules)
        result = detect_rules(data.get('rules', []) if isinstance(data, dict) else data)
    else:
        result = {'findings': text_candidates(read_text(Path(args.file)), Path(args.file).name),
                  'limitations': ['Text mode identifies candidates only; agent semantic review required.']}
    emit(result, args.output)
    return 1 if any(f['status'] == 'confirmed' and f['severity'] in {'critical', 'high'} for f in result['findings']) else 0


if __name__ == '__main__':
    run_cli(main)
