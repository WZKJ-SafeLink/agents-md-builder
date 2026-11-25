"""Extract bounded implementation observations, never promote them to requirements."""
from __future__ import annotations
import argparse
import re
from pathlib import Path
from typing import Any
from common import Scanner, emit, run_cli, scan_arguments, scanner_from

PATTERNS = {
    'http-client': {'fetch': r'\bfetch\(', 'axios': r'\baxios[.(]', 'RestTemplate': r'\bRestTemplate\b', 'WebClient': r'\bWebClient\b', 'requests': r'\brequests\.(get|post|request)\('},
    'data-access': {'jpa': r'\bJpaRepository\b', 'mybatis': r'\b(?:@Mapper|BaseMapper)\b', 'django-orm': r'\bobjects\.(?:filter|get|all)\('},
    'transaction': {'spring': r'@Transactional\b', 'django': r'transaction\.atomic\(', 'sqlalchemy': r'session\.begin\('},
    'logging': {'slf4j': r'\borg\.slf4j\b', 'python-logging': r'\blogging\.(?:getLogger|info|error)\b', 'console': r'\bconsole\.(?:log|error)\('},
    'error-handling': {'global-spring': r'@(?:RestControllerAdvice|ControllerAdvice)', 'python-handler': r'@\w+\.exception_handler\('},
    'messaging': {'rocketmq': r'@RocketMQMessageListener', 'kafka': r'@KafkaListener', 'rabbitmq': r'@RabbitListener'},
    'reuse': {'spring-utilities': r'\b(?:StringUtils|ObjectUtils|CollectionUtils|NumberUtils)\.'},
}


def extract(scan: Scanner, sample_limit: int = 80) -> dict[str, Any]:
    eligible = [(p, t) for p, t in scan.contents.items() if Path(p).suffix in {'.java', '.kt', '.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs', '.cs'}]
    observations = []
    groups: dict[tuple[str, str], set[str]] = {}
    # Round-robin folders so one large module does not monopolize all samples.
    buckets: dict[str, list[tuple[str, str]]] = {}
    for p, t in eligible:
        buckets.setdefault(Path(p).parent.as_posix(), []).append((p, t))
    samples: list[tuple[str, str]] = []
    while buckets and len(samples) < sample_limit:
        for key in list(buckets):
            samples.append(buckets[key].pop(0))
            if not buckets[key]:
                del buckets[key]
            if len(samples) == sample_limit:
                break
    risks = []
    for path, text in samples:
        for category, patterns in PATTERNS.items():
            for name, pattern in patterns.items():
                match = re.search(pattern, text)
                if match:
                    observations.append({'category': category, 'name': name, 'classification': 'OBSERVED',
                                         'confidence': 'medium', 'evidence': {'path': path, 'locator': 'line:' + str(text.count('\n', 0, match.start()) + 1)}})
                    groups.setdefault((Path(path).parts[0], category), set()).add(name)
        if 'Controller' in Path(path).name and re.search(r'\w*Repository\s+\w+', text):
            risks.append({'path': path, 'status': 'candidate', 'issue': 'Controller contains repository reference; inspect actual calls and project boundary policy.'})
    inconsistencies = [{'scope': scope, 'category': category, 'implementations': sorted(names), 'status': 'candidate',
                        'action': 'Review whether coexistence is intentional before proposing a unified approach.'}
                       for (scope, category), names in groups.items() if len(names) > 1]
    return {'sampled_files': len(samples), 'eligible_files': len(eligible), 'observations': observations,
            'inconsistencies': inconsistencies, 'architecture_candidates': risks,
            'limitations': ['Pattern observations are not best-practice endorsements or full semantic call analysis.']}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    scan_arguments(parser)
    parser.add_argument('--sample-limit', type=int, default=80)
    args = parser.parse_args()
    if not 1 <= args.sample_limit <= 500:
        raise ValueError('sample limit must be between 1 and 500')
    emit(extract(scanner_from(args), args.sample_limit), args.output)
    return 0


if __name__ == '__main__':
    run_cli(main)
