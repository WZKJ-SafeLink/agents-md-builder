"""Classify reference rules for a target project; private policy stays excluded."""
from __future__ import annotations
import argparse
import json
from typing import Any
from common import emit, load_json, public_source, redact, run_cli
from detect_conflicts import validate_rule


def migrate(rules: list[dict[str, Any]], profile: dict[str, Any],
            authorize_enterprise: bool = False) -> dict[str, Any]:
    names = {t['name'] for t in profile.get('technologies', [])}
    groups: dict[str, list[dict[str, Any]]] = {key: [] for key in ['general', 'technology', 'enterprise', 'project', 'inapplicable']}
    selected = []
    for rule in rules:
        if not isinstance(rule, dict):
            groups['inapplicable'].append({'reason': 'Rule must be an object.'})
            continue
        domain = rule.get('migration_class', 'project')
        if domain not in groups:
            domain = 'project'
        # Public technical citations are not private project endpoints. Only retain
        # citations from domains already recorded in the bundled source registry.
        sources = rule.get('sources', [])
        source_safe = isinstance(sources, list) and all(public_source(source) for source in sources)
        serialized = json.dumps({**rule, 'sources': []}, ensure_ascii=False)
        errors = validate_rule(rule)
        required = set(rule.get('technologies', []))
        if errors or not source_safe or serialized != redact(serialized):
            groups['inapplicable'].append({'id': rule.get('id'), 'reason': 'Invalid structure or private/credential/address content; do not copy.'})
            continue
        if required and not required.issubset(names):
            groups['inapplicable'].append({'id': rule['id'], 'reason': 'Target technology mismatch.'})
            continue
        groups[domain].append(rule)
        if domain in {'general', 'technology'} or (domain == 'enterprise' and authorize_enterprise):
            selected.append(rule)
    return {'groups': groups, 'candidate_rules': selected,
            'limitations': ['Input migration class, scopes and technology tags must first be extracted and reviewed by the agent; project-specific rules never migrate automatically.']}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rules', required=True)
    parser.add_argument('--profile', required=True)
    parser.add_argument('--authorize-enterprise', action='store_true')
    parser.add_argument('--output')
    args = parser.parse_args()
    data = load_json(args.rules)
    emit(migrate(data.get('rules', []) if isinstance(data, dict) else data, load_json(args.profile), args.authorize_enterprise), args.output)
    return 0


if __name__ == '__main__':
    run_cli(main)
