"""Validate the JSON Schema subset used by this skill without third-party packages."""
from __future__ import annotations
import argparse
import re
from typing import Any
from common import emit, load_json, run_cli


def check(value: Any, schema: dict[str, Any], location: str = '$') -> list[str]:
    errors = []
    types = {'object': lambda x: isinstance(x, dict), 'array': lambda x: isinstance(x, list),
             'string': lambda x: isinstance(x, str), 'number': lambda x: isinstance(x, (int, float)) and not isinstance(x, bool),
             'integer': lambda x: isinstance(x, int) and not isinstance(x, bool), 'boolean': lambda x: isinstance(x, bool),
             'null': lambda x: x is None}
    expected = schema.get('type', [])
    expected = [expected] if isinstance(expected, str) else expected
    if expected and not any(types[t](value) for t in expected):
        return [location + ': wrong type']
    if 'enum' in schema and value not in schema['enum']:
        errors.append(location + ': invalid enum')
    if isinstance(value, dict):
        errors += [location + '.' + key + ': required' for key in schema.get('required', []) if key not in value]
        for key, child in value.items():
            if key in schema.get('properties', {}):
                errors += check(child, schema['properties'][key], location + '.' + key)
    elif isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            errors.append(location + ': too few items')
        for index, item in enumerate(value):
            errors += check(item, schema.get('items', {}), location + '[' + str(index) + ']')
    elif isinstance(value, str):
        if len(value) < schema.get('minLength', 0) or ('pattern' in schema and not re.search(schema['pattern'], value)):
            errors.append(location + ': invalid string')
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < schema.get('minimum', float('-inf')) or value > schema.get('maximum', float('inf')):
            errors.append(location + ': out of range')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', required=True)
    parser.add_argument('--schema', required=True)
    parser.add_argument('--output')
    args = parser.parse_args()
    errors = check(load_json(args.file), load_json(args.schema))
    emit({'valid': not errors, 'errors': errors, 'scope': 'Bundled schema subset, not a general JSON Schema implementation.'}, args.output)
    return 1 if errors else 0


if __name__ == '__main__':
    run_cli(main)
