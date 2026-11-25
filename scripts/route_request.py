"""Give a conservative intent hint; the host agent resolves contextual ambiguity."""
from __future__ import annotations
import argparse
import re
from typing import Any
from common import emit, run_cli


def route(text: str, has_project: bool = False, has_agents: bool = False) -> dict[str, Any]:
    relevant = bool(re.search(r'agents\.md|研发规范|工程规范|开发规范|代码规范|ai.*规范|规范|coding instructions', text, re.I))
    if not relevant:
        return {'mode': None, 'scan_authorized': False, 'status': 'not-applicable'}
    mode = None
    for candidate, pattern in [('MIGRATE', r'迁移|参考.*(?:其他|另一个)项目|migrat'),
                               ('UPDATE', r'升级|替换.*(?:框架|中间件)|新增模块|维护|update|upgrade'),
                               ('HIERARCHY', r'多模块|模块级|根目录和|hierarch|monorepo'),
                               ('OPTIMIZE', r'优化|精简|补充|统一|去重|optimi|improve|shorten'),
                               ('AUDIT', r'审查|检查|评分|打分|audit|review|score')]:
        if re.search(pattern, text, re.I):
            mode = candidate
            break
    if mode is None and re.search(r'生成|建立|创建|generate|create|build', text, re.I):
        mode = 'DISCOVER' if has_project else 'CREATE'
    # Mentioning a file does not authorize scanning. Explicit scope must be supplied separately.
    return {'mode': mode, 'scan_authorized': False,
            'status': 'intent-hint-only' if mode else 'not-applicable',
            'has_project': has_project, 'has_agents': has_agents,
            'next_action': 'Host agent confirms supplied scope and capability; this helper never scans.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request', required=True)
    parser.add_argument('--has-project', action='store_true')
    parser.add_argument('--has-agents', action='store_true')
    parser.add_argument('--output')
    args = parser.parse_args()
    emit(route(args.request, args.has_project, args.has_agents), args.output)
    return 0


if __name__ == '__main__':
    run_cli(main)
