"""Detect declared dependencies, versions and commands without executing builds."""
from __future__ import annotations
import argparse
import json
import posixpath
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
from common import Scanner, VERSION, emit, run_cli, scan_arguments, scanner_from

# Exact dependency identifiers. File text is not searched for arbitrary marketing names.
DEPENDENCIES: dict[str, tuple[str, str]] = {}
for category, entries in {
    'framework': {
        'spring-boot': ['spring-boot-starter-parent', 'spring-boot-dependencies', 'spring-boot', 'spring-boot-starter-web', 'spring-boot-starter-webflux'],
        'spring-framework': ['spring-context', 'spring-web', 'spring-webmvc'],
        'spring-data-jpa': ['spring-data-jpa', 'spring-boot-starter-data-jpa'],
        'mybatis': ['mybatis', 'mybatis-spring-boot-starter'],
        'mybatis-plus': ['mybatis-plus', 'mybatis-plus-boot-starter', 'mybatis-plus-spring-boot3-starter'],
        'vue': ['vue'], 'react': ['react'], 'nextjs': ['next'], 'nuxt': ['nuxt'],
        'angular': ['@angular/core'], 'fastapi': ['fastapi'], 'django': ['django'], 'flask': ['flask'],
        'nestjs': ['@nestjs/core'], 'express': ['express'], 'flutter': ['flutter'],
        'react-native': ['react-native'], 'uniapp': ['@dcloudio/uni-app'],
        'dotnet': ['microsoft.aspnetcore.app', 'microsoft.net.sdk.web']},
    'database': {
        'postgresql': ['postgresql', 'psycopg', 'psycopg2', 'psycopg2-binary', 'asyncpg', 'pg', 'npgsql', 'github.com/lib/pq', 'github.com/jackc/pgx/v5'],
        'mysql': ['mysql-connector-j', 'mysql-connector-java', 'mysql2', 'pymysql', 'mysqlclient', 'github.com/go-sql-driver/mysql'],
        'mariadb': ['mariadb-java-client', 'mariadb'], 'sqlite': ['sqlite-jdbc', 'better-sqlite3', 'sqlite3', 'rusqlite'],
        'mongodb': ['mongodb-driver-sync', 'mongodb', 'pymongo', 'mongoose', 'go.mongodb.org/mongo-driver'],
        'sqlserver': ['mssql-jdbc', 'microsoft.data.sqlclient', 'mssql'], 'oracle': ['ojdbc8', 'ojdbc11', 'oracledb'],
        'tdengine': ['taos-jdbcdriver', 'taospy']},
    'middleware': {'redis': ['redis', 'ioredis', 'jedis', 'lettuce-core', 'spring-boot-starter-data-redis', 'stackexchange.redis', 'github.com/redis/go-redis/v9'],
                   'rocketmq': ['rocketmq-client', 'rocketmq-spring-boot-starter', 'rocketmq-client-java'],
                   'kafka': ['kafka-clients', 'spring-kafka', 'kafkajs', 'confluent-kafka', 'kafka-python'],
                   'rabbitmq': ['amqp-client', 'spring-boot-starter-amqp', 'amqplib', 'pika'],
                   'mqtt': ['org.eclipse.paho.client.mqttv3', 'mqtt', 'paho-mqtt'],
                   'elasticsearch': ['elasticsearch', 'elasticsearch-java', '@elastic/elasticsearch']}
}.items():
    for name, aliases in entries.items():
        for alias in aliases:
            DEPENDENCIES[alias.lower()] = (name, category)

EXTENSIONS = {'.java': 'java', '.kt': 'kotlin', '.kts': 'kotlin', '.py': 'python',
              '.js': 'javascript', '.jsx': 'javascript', '.ts': 'typescript', '.tsx': 'typescript',
              '.go': 'go', '.rs': 'rust', '.cs': 'csharp', '.c': 'c', '.h': 'cpp', '.cc': 'cpp',
              '.cpp': 'cpp', '.hpp': 'cpp', '.php': 'php', '.rb': 'ruby', '.swift': 'swift', '.dart': 'dart'}


def version_status(version: str | None, inherited: bool = False) -> str:
    if not version or version in {'*', 'workspace:*', 'latest'} or '${' in version or version.startswith(('file:', 'git', 'http')):
        return 'unknown'
    if len(version) > 128 or not re.fullmatch(r'[A-Za-z0-9_.^~+!<>=|,():*\[\]/ -]+', version):
        return 'unknown'
    tokens = re.split(r'[\s,|]+', version.strip('[]()'))
    if any(token and not re.fullmatch(r'[<>=^~!]*v?\d[\w.*+-]*[\])]?|[-*]', token) for token in tokens):
        return 'unknown'
    if inherited:
        return 'inherited'
    if re.fullmatch(r'v?\d+(?:\.\d+)*(?:[-+][\w.-]+)?', version):
        return 'confirmed'
    return 'range'


def xml_tree(text: str) -> ET.Element:
    if re.search(r'<!DOCTYPE|<!ENTITY', text, re.I):
        raise ValueError('XML entities are excluded')
    root = ET.fromstring(text)
    for node in root.iter():
        node.tag = node.tag.rsplit('}', 1)[-1]
    return root


def toml_data(text: str) -> dict[str, Any]:
    try:
        import tomllib
    except ImportError:
        # Deliberately limited static fallback for 3.10, never evaluate TOML as code.
        result: dict[str, Any] = {}
        current = result
        for line in text.splitlines():
            section = re.fullmatch(r'\s*\[([\w.-]+)]\s*', line)
            if section:
                current = result
                for part in section[1].split('.'):
                    current = current.setdefault(part, {})
            pair = re.match(r'\s*([\w-]+)\s*=\s*[\"\x27]([^\"\x27]+)[\"\x27]', line)
            if pair:
                current[pair[1]] = pair[2]
        # Multiline dependency arrays are separately parsed as bounded strings.
        match = re.search(r'(?ms)^dependencies\s*=\s*\[(.*?)]', text)
        if match and 'project' in result:
            result['project']['dependencies'] = re.findall(r'[\"\x27]([^\"\x27]+)[\"\x27]', match[1])
        return result
    try:
        return tomllib.loads(text)
    except ValueError:
        return {}


def detect(scan: Scanner, include_fixtures: bool = False) -> dict[str, Any]:
    fixture_parts = {'fixtures', '__fixtures__', 'testdata', '__mocks__'}
    def fixture(path: str) -> bool:
        return any(part.lower() in fixture_parts for part in Path(path).parts[:-1])
    contents = {path: text for path, text in scan.contents.items() if include_fixtures or not fixture(path)}
    excluded_fixtures = sum(path not in contents for path in scan.contents)
    found: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    commands: list[dict[str, Any]] = []
    modules: dict[str, dict[str, Any]] = {}
    notes: list[dict[str, str]] = []
    dependencies: list[dict[str, str]] = []
    manifests: dict[str, Any] = {}

    def add(name: str, category: str, version: str | None, path: str, locator: str,
            status: str | None = None, confidence: str = 'high') -> None:
        state = status or version_status(version)
        if version and (len(version) > 128 or re.search(r'[\r\n`{};]|<[^=\d]', version)):
            state = 'unknown'
        ver = (version or 'unknown') if state != 'unknown' else 'unknown'
        key = (name, category, ver or 'unknown', str(Path(path).parent))
        evidence = {'path': path, 'locator': locator, 'type': 'source-file' if confidence == 'low' else 'declared-dependency'}
        if key not in found:
            found[key] = {'name': name, 'category': category, 'version': ver,
                          'status': state, 'confidence': confidence, 'evidence': []}
        if evidence not in found[key]['evidence']:
            found[key]['evidence'].append(evidence)

    def dep(name: str, version: str | None, path: str, locator: str, status: str | None = None) -> None:
        dependencies.append({'name': name.lower(), 'version': version or 'unknown', 'path': path})
        canonical = DEPENDENCIES.get(name.lower())
        if canonical:
            add(*canonical, version, path, locator, status)

    def command(text: str, path: str, purpose: str, platform: str = 'all') -> None:
        commands.append({'command': text, 'cwd': Path(path).parent.as_posix(), 'purpose': purpose,
                         'platform': platform, 'evidence': {'path': path, 'locator': purpose},
                         'execution': 'not-run', 'verification': 'declared-not-executed'})

    # Parse XML once and resolve only local parents that were included in the scan.
    poms: dict[str, ET.Element] = {}
    for path, text in contents.items():
        if Path(path).name == 'pom.xml':
            try:
                poms[path] = xml_tree(text)
            except (ValueError, ET.ParseError):
                notes.append({'path': path, 'issue': 'XML invalid or entity declaration excluded'})

    def pom_context(path: str, seen: set[str] | None = None) -> tuple[dict[str, str], dict[str, str]]:
        seen = set() if seen is None else set(seen)
        if path in seen or len(seen) >= 12:
            return {}, {}
        seen.add(path)
        tree = poms[path]
        properties: dict[str, str] = {}
        managed: dict[str, str] = {}
        parent = tree.find('parent')
        if parent is not None:
            relative_node = parent.find('relativePath')
            relative = '../pom.xml' if relative_node is None else (relative_node.text or '')
            local = posixpath.normpath(posixpath.join(posixpath.dirname(path), relative))
            if relative and local in poms:
                properties, managed = pom_context(local, seen)
            properties['project.parent.version'] = parent.findtext('version', '')
        for node in tree.findall('properties/*'):
            properties[node.tag] = node.text or ''
        properties['project.version'] = tree.findtext('version', properties.get('project.parent.version', ''))
        for node in tree.findall('dependencyManagement/dependencies/dependency'):
            managed[node.findtext('artifactId', '')] = node.findtext('version', '')
        return properties, managed

    def resolve(value: str | None, properties: dict[str, str]) -> str | None:
        for _ in range(10):
            if not value or '${' not in value:
                break
            new = re.sub(r'\$\{([^}]+)}', lambda m: properties.get(m[1], m[0]), value)
            if new == value:
                break
            value = new
        return value

    for path, text in contents.items():
        file = Path(path)
        name = file.name
        folder = file.parent.as_posix()
        if file.suffix in EXTENSIONS:
            add(EXTENSIONS[file.suffix], 'language', None, path, 'extension', 'inferred', 'low')
        try:
            if name == 'pom.xml' and path in poms:
                tree = poms[path]
                props, managed = pom_context(path)
                add('java', 'language', resolve(props.get('maven.compiler.release') or props.get('java.version') or props.get('maven.compiler.source'), props), path, 'properties/compiler')
                nodes = tree.findall('dependencies/dependency') + tree.findall('dependencyManagement/dependencies/dependency')
                parent = tree.find('parent')
                if parent is not None:
                    nodes.append(parent)
                for node in nodes:
                    artifact = node.findtext('artifactId', '')
                    raw = node.findtext('version')
                    inherited = raw is None and artifact in managed
                    value = resolve(raw or managed.get(artifact), props)
                    dep(artifact, value, path, 'dependency/' + artifact, version_status(value, inherited))
                for module in tree.findall('modules/module'):
                    value = posixpath.normpath(posixpath.join(folder, module.text or ''))
                    if not value.startswith('../') and value != '.' and (value + '/pom.xml') in contents:
                        modules[value] = {'path': value, 'evidence': path, 'kind': 'maven-module', 'confidence': 'high'}
                wrapper = posixpath.join(folder, 'mvnw').removeprefix('./')
                windows = posixpath.join(folder, 'mvnw.cmd').removeprefix('./')
                if wrapper in contents:
                    command('./mvnw test', path, 'test', 'posix')
                if windows in contents:
                    command('mvnw.cmd test', path, 'test', 'windows')
                if wrapper not in contents and windows not in contents:
                    command('mvn test', path, 'test')
            elif name == 'package.json':
                data = json.loads(text)
                manifests[path] = data
                add('javascript', 'language', None, path, 'package.json')
                for group in ('dependencies', 'devDependencies', 'peerDependencies'):
                    for identifier, value in data.get(group, {}).items():
                        dep(identifier, str(value), path, group + '/' + identifier)
                        if identifier == 'typescript':
                            add('typescript', 'language', str(value), path, group + '/typescript')
                manager = data.get('packageManager', '').split('@')[0]
                if manager not in {'npm', 'pnpm', 'yarn', 'bun'}:
                    lock_managers = {'pnpm-lock.yaml': 'pnpm', 'yarn.lock': 'yarn', 'bun.lock': 'bun'}
                    manager = next((m for lock, m in lock_managers.items() if posixpath.join(folder, lock).removeprefix('./') in contents), 'npm')
                for script in data.get('scripts', {}):
                    if re.fullmatch(r'(?:test|lint|build|typecheck|check)(?::[\w-]+)?', script):
                        command(f'{manager} run {script}', path, script)
                workspaces = data.get('workspaces', [])
                patterns = workspaces if isinstance(workspaces, list) else workspaces.get('packages', [])
                for candidate in contents:
                    if Path(candidate).name != 'package.json' or candidate == path:
                        continue
                    parent_dir = Path(candidate).parent
                    try:
                        local = parent_dir.relative_to(file.parent).as_posix()
                    except ValueError:
                        continue
                    if any(parent_dir.match(posixpath.join(folder, pat)) or Path(local).match(pat) for pat in patterns):
                        modules[parent_dir.as_posix()] = {'path': parent_dir.as_posix(), 'evidence': path, 'kind': 'workspace', 'confidence': 'high'}
            elif name in {'pyproject.toml', 'Cargo.toml'}:
                data = toml_data(text)
                language = 'python' if name == 'pyproject.toml' else 'rust'
                version = data.get('project', {}).get('requires-python') if language == 'python' else data.get('package', {}).get('rust-version')
                if language == 'rust' and version:
                    version = '>=' + str(version)
                add(language, 'language', version, path, 'project/runtime')
                if language == 'python':
                    values = list(data.get('project', {}).get('dependencies', []))
                    for group in data.get('project', {}).get('optional-dependencies', {}).values():
                        values += group
                    for identifier, value in data.get('tool', {}).get('poetry', {}).get('dependencies', {}).items():
                        dep(identifier, str(value) if isinstance(value, str) else value.get('version'), path, 'tool/poetry/dependencies/' + identifier)
                    for value in values:
                        match = re.match(r'([\w.-]+)(?:\[[^]]*])?\s*(.*)', value)
                        if match:
                            dep(match[1], match[2].strip().removeprefix('==') or None, path, 'project/dependencies/' + match[1])
                else:
                    for identifier, value in data.get('dependencies', {}).items():
                        dep(identifier, value if isinstance(value, str) else value.get('version'), path, 'dependencies/' + identifier)
                    command('cargo test', path, 'test')
                    for pattern in data.get('workspace', {}).get('members', []):
                        for candidate in contents:
                            if Path(candidate).name == 'Cargo.toml' and candidate != path and Path(candidate).parent.match(posixpath.join(folder, pattern)):
                                value = Path(candidate).parent.as_posix()
                                modules[value] = {'path': value, 'evidence': path, 'kind': 'cargo-workspace', 'confidence': 'high'}
            elif name.startswith('requirements') and file.suffix == '.txt':
                add('python', 'language', None, path, 'requirements')
                for line in text.splitlines():
                    match = re.match(r'\s*([A-Za-z][\w.-]+)(?:\[[^]]*])?\s*((?:==|>=|<=|~=|>|<|!=)[^;#\s]+)?', line)
                    if match:
                        dep(match[1], (match[2] or '').removeprefix('==') or None, path, 'requirement/' + match[1])
            elif name == 'go.mod':
                version = re.search(r'(?m)^go\s+([\d.]+)', text)
                add('go', 'language', version[1] if version else None, path, 'go')
                for match in re.finditer(r'(?m)^\s*(?:require\s+)?([\w./-]+)\s+(v[\w.+-]+)', text):
                    dep(match[1], match[2], path, 'require/' + match[1])
                command('go test ./...', path, 'test')
            elif name in {'build.gradle', 'build.gradle.kts'}:
                add('kotlin' if '.kts' in name or 'org.jetbrains.kotlin' in text else 'java', 'language', None, path, 'gradle')
                for match in re.finditer(r'[\"\x27]([\w.-]+):([\w.-]+):([^\"\x27]+)[\"\x27]', text):
                    dep(match[2], match[3] if '$' not in match[3] else None, path, 'dependency/' + match[2])
                for match in re.finditer(r'id\s*\(?[\"\x27]org.springframework.boot[\"\x27]\)?\s*version\s*[\"\x27]([^\"\x27]+)', text):
                    add('spring-boot', 'framework', match[1], path, 'plugin/org.springframework.boot')
                for wrapper, cmd, platform in [('gradlew', './gradlew test', 'posix'), ('gradlew.bat', 'gradlew.bat test', 'windows')]:
                    if posixpath.join(folder, wrapper).removeprefix('./') in contents:
                        command(cmd, path, 'test', platform)
            elif name in {'settings.gradle', 'settings.gradle.kts'}:
                for line in text.splitlines():
                    if re.match(r'\s*include\b', line):
                        for item in re.findall(r'[\"\x27]:?([\w:-]+)[\"\x27]', line):
                            module_path = posixpath.normpath(posixpath.join(folder, item.replace(':', '/')))
                            if any(p.startswith(module_path + '/') for p in contents):
                                modules[module_path] = {'path': module_path, 'evidence': path, 'kind': 'gradle-module', 'confidence': 'high'}
            elif file.suffix == '.csproj':
                tree = xml_tree(text)
                add('csharp', 'language', tree.findtext('.//LangVersion'), path, 'LangVersion')
                dep(tree.attrib.get('Sdk', ''), None, path, 'Sdk')
                if tree.findtext('.//TargetFramework'):
                    add('dotnet', 'framework', tree.findtext('.//TargetFramework'), path, 'TargetFramework', 'confirmed')
                for node in tree.findall('.//PackageReference'):
                    dep(node.attrib.get('Include', ''), node.attrib.get('Version') or node.findtext('Version'), path, 'PackageReference')
                command('dotnet test', path, 'test')
            elif name == 'composer.json':
                data = json.loads(text)
                add('php', 'language', data.get('require', {}).get('php'), path, 'require/php')
            elif name == 'Gemfile':
                add('ruby', 'language', None, path, 'Gemfile')
            elif name == 'Package.swift':
                match = re.search(r'swift-tools-version:\s*([\d.]+)', text)
                add('swift', 'language', '>=' + match[1] if match else None, path, 'tools-version')
                add('ios', 'framework', None, path, 'platforms', 'inferred', 'low') if '.iOS(' in text else None
            elif name == 'pubspec.yaml':
                add('dart', 'language', None, path, 'pubspec')
                if re.search(r'(?m)^\s+sdk:\s*flutter\s*$', text):
                    add('flutter', 'framework', None, path, 'dependencies/flutter/sdk')
            elif name == 'tsconfig.json':
                add('typescript', 'language', None, path, 'tsconfig')
            elif file.suffix == '.sln':
                add('csharp', 'language', None, path, 'solution', 'inferred', 'medium')
            elif file.suffix == '.pbxproj' and any(part.endswith('.xcodeproj') for part in file.parts):
                match = re.search(r'SWIFT_VERSION\s*=\s*([\d.]+)', text)
                add('swift', 'language', match[1] if match else None, path, 'SWIFT_VERSION')
                if 'IPHONEOS_DEPLOYMENT_TARGET' in text:
                    add('ios', 'framework', None, path, 'IPHONEOS_DEPLOYMENT_TARGET')
            elif name in {'CMakeLists.txt', 'Makefile'}:
                add('cpp', 'language', None, path, 'build-file', 'inferred', 'low')
            elif name == 'project.config.json' and 'miniprogram' in text.lower():
                add('wechat-miniprogram', 'framework', None, path, 'compileType')
            elif name == 'pnpm-workspace.yaml':
                patterns = re.findall(r'(?m)^\s*-\s*[\"\x27]?([^\"\x27\n]+)', text)
                for candidate in contents:
                    if Path(candidate).name == 'package.json' and candidate != posixpath.join(folder, 'package.json').removeprefix('./'):
                        value = Path(candidate).parent.as_posix()
                        if any(Path(value).match(posixpath.join(folder, pat.strip())) for pat in patterns):
                            modules[value] = {'path': value, 'evidence': path, 'kind': 'workspace', 'confidence': 'high'}
        except (ValueError, TypeError, AttributeError, ET.ParseError):
            notes.append({'path': path, 'issue': 'manifest could not be fully parsed; semantic review required'})

    # Necessary config signatures: retain only the technology, never raw URLs or values.
    signatures = {'postgresql': 'postgresql', 'mysql': 'mysql', 'mariadb': 'mariadb',
                  'sqlite': 'sqlite', 'sqlserver': 'sqlserver', 'oracle': 'oracle', 'mongodb': 'mongodb'}
    for path, text in contents.items():
        if Path(path).suffix in {'.yaml', '.yml', '.properties', '.json', '.toml'}:
            for scheme, name in signatures.items():
                if re.search(r'(?:jdbc:|[\"\x27\s:=])' + scheme + r'(?:\+\w+)?:(?://)?', text, re.I):
                    add(name, 'database', None, path, 'connection-scheme')
        if Path(path).suffix in {'.gradle', '.kts'} and 'com.android.application' in text:
            add('android', 'framework', None, path, 'android-plugin')

    # Detect independently buildable folders as candidates, not confirmed services.
    for item in scan.files:
        if not include_fixtures and fixture(item['path']):
            continue
        path = Path(item['path'])
        if path.name in {'pom.xml', 'package.json', 'pyproject.toml', 'go.mod', 'Cargo.toml', 'pubspec.yaml'} or path.suffix == '.csproj':
            folder = path.parent.as_posix()
            if folder != '.':
                modules.setdefault(folder, {'path': folder, 'evidence': item['path'], 'kind': 'build-boundary', 'confidence': 'medium'})
    if any('unittest' in text for p, text in contents.items() if Path(p).name.startswith('test_') and p.endswith('.py')):
        evidence = next(p for p, text in contents.items() if Path(p).name.startswith('test_') and 'unittest' in text)
        test_dir = Path(evidence).parent.as_posix()
        commands.append({'command': 'python -m unittest discover -v', 'cwd': test_dir,
                         'purpose': 'test', 'platform': 'all', 'evidence': {'path': evidence, 'locator': 'unittest import'},
                         'execution': 'not-run', 'verification': 'observed-not-executed'})
    stack = sorted(found.values(), key=lambda item: (item['category'], item['name'], item['version'], item['evidence'][0]['path']))
    # Explicit declarations supersede low-confidence extension entries of the same module/language.
    stack = [entry for entry in stack if not (entry['confidence'] == 'low' and any(
        other['name'] == entry['name'] and other['confidence'] == 'high' and
        Path(other['evidence'][0]['path']).parent == Path(entry['evidence'][0]['path']).parent for other in stack))]
    architecture: list[dict[str, Any]] = []
    if any(m['kind'] in {'workspace', 'maven-module', 'gradle-module', 'cargo-workspace'} for m in modules.values()):
        architecture.append({'name': 'monorepo', 'classification': 'OBSERVED', 'confidence': 'high',
                             'evidence': sorted({m['evidence'] for m in modules.values()})})
    if len(modules) >= 2:
        architecture.append({'name': 'multiple-build-boundaries', 'classification': 'OBSERVED', 'confidence': 'medium',
                             'evidence': sorted({m['evidence'] for m in modules.values()})})
    return {'schema_version': VERSION, 'technologies': stack, 'modules': sorted(modules.values(), key=lambda x: x['path']),
            'commands': sorted(commands, key=lambda x: (x['cwd'], x['command'])), 'architecture': architecture,
            'dependencies': sorted(dependencies, key=lambda x: (x['path'], x['name'])),
            'scan': {'file_count': len(scan.files), 'truncated': scan.truncated, 'bytes_read': scan.total_bytes},
            'notes': notes, 'fixture_files_excluded_from_stack': excluded_fixtures,
            'limitations': ['Static declarations only; fixture/testdata paths are excluded unless requested. Dynamic builds, remote parents, lock resolution and semantic architecture require review.']}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    scan_arguments(parser)
    parser.add_argument('--include-fixtures', action='store_true', help='Explicitly include nested fixture/testdata dependencies')
    args = parser.parse_args()
    emit(detect(scanner_from(args), args.include_fixtures), args.output)
    return 0


if __name__ == '__main__':
    run_cli(main)
