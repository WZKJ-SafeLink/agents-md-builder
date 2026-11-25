# AGENTS.md Builder

[English](README.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md)

**Turn repository evidence into actionable instructions for AI coding agents.**

Version **1.0.1** · Publisher **Safe Link** · License **Apache-2.0**

AGENTS.md Builder is a local Agent Skill for generating, auditing, scoring, improving, and maintaining project-specific `AGENTS.md` files. It combines repository configuration, module boundaries, representative code, and confirmed user requirements with a selectively loaded engineering knowledge base.

The host agent handles natural-language requests and semantic decisions. Python helpers perform bounded static analysis and reproducible checks. No paid API, API key, database, backend service, Docker deployment, or MCP server is required for the core workflow.

## Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Working modes](#working-modes)
- [Command-line workflows](#command-line-workflows)
- [Knowledge base](#knowledge-base)
- [Scoring and review](#scoring-and-review)
- [Safety and privacy](#safety-and-privacy)
- [Repository structure](#repository-structure)
- [Testing and packaging](#testing-and-packaging)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Documentation and license](#documentation-and-license)

## Features

- **Evidence-based discovery:** identify technologies, version declarations, build boundaries, instruction files, and representative implementation patterns without running project code.
- **Project-specific generation:** preserve confirmed architectural decisions, existing conventions, and custom requirements; keep unknown decisions explicit.
- **Review and improvement:** check Markdown, credential risks, referenced paths, version mismatches, and statically recognizable command declarations; produce candidates and explainable diffs.
- **Scoped conflict analysis:** compare structured rules by scope, strength, and explicit keys. Free-form matches remain candidates for semantic review.
- **Multi-module instructions:** separate common root rules from module-specific differences when the project evidence warrants it.
- **Maintenance and migration:** compare profiles after upgrades and filter reference rules before transferring them to another project.
- **Local operation:** use Python's standard library, support offline knowledge-base use, and provide a host-agent fallback when Python is unavailable.

Existing code is an observation, not an automatic best-practice endorsement. The tool does not prescribe one architecture or select an unspecified framework version for every project.

## Requirements

| Component | Requirement |
|---|---|
| Agent-assisted workflow | A host that can load Agent Skills and read the files you authorize |
| Deterministic helpers | Python 3.10 or later; standard library only |
| Local output | Write access to a chosen candidate/report directory |
| Network | Optional; the host may verify public official documentation |
| Operating systems | Cross-platform implementation; native execution tested on macOS |

If Python is unavailable, the host can follow the same workflow using bounded manual file inspection. If network access is unavailable, it can use the local references and state which claims were not checked against current documentation.

English is the default language of this README. Generated-document language is configured separately: the CLI supports `--language en` and `--language zh`, with `zh` as its default. A Japanese README does not add a dedicated Japanese CLI output mode. Most supporting documents and knowledge-base articles are currently written in Simplified Chinese.

## Installation

### WorkBuddy

Use the **WorkBuddy-specific archive** built with `--platform workbuddy`.

1. Open the client's skill upload/import interface and select `agents-md-builder-workbuddy-v1.0.1.zip`.
2. Upload the ZIP directly. It places `SKILL.md` at the archive root and uses only one directory level for resources.
3. Enable the skill and select an authorized project or provide the relevant attachments.
4. Start with a request for a candidate or a read-only audit.

For manual folder installation, create a directory named `agents-md-builder` and extract the archive contents into it. Keep `SKILL.md` directly inside that directory.

The original 1.0.0 archive was rejected for excessive directory nesting. The 1.0.1 WorkBuddy archive flattens resource paths and rewrites their references; avoid adding another wrapper folder when repacking it. The fixed archive has passed local extraction and runtime checks; successful WorkBuddy import and marketplace approval have not yet been verified. See the [publishing guide](docs/WORKBUDDY_PUBLISH.md).

### Codex and other Agent Skills hosts

Use the generic archive or the source skill directory. The generic ZIP contains an `agents-md-builder/` folder with `SKILL.md` inside it. Place that folder in the skill location supported by your host, then enable or reload it as the host requires.

Keep `scripts/`, `references/`, and `assets/` alongside `SKILL.md`; installing only the entrypoint omits resources required by this skill. Instruction loading, override behavior, and context budgets vary by host.

## Quick start

After installing the skill and authorizing the project, ask the host:

> Generate an AGENTS.md candidate for this repository in English. Use actual project evidence, preserve confirmed requirements, and keep the existing file unchanged.

> Audit this AGENTS.md without modifying it. Show issue locations, risks, score coverage, and assumptions that could not be verified.

> Improve the current AGENTS.md. Preserve mandatory rules and exceptions, merge duplicates within the same scope, and provide a candidate plus a diff.

For a new project, provide the decisions you have already made:

> Create AI coding instructions for a Java 21 project using Spring Boot, Spring Data JPA, and PostgreSQL. Framework versions are undecided. Keep them unknown and do not invent build commands.

The workflow discovers evidence, loads applicable references, creates a candidate, runs available checks, and reports unresolved decisions. Normal generation returns the instruction file and a concise explanation. Audit mode returns findings. Optimization returns a candidate and a change report. Intermediate scan JSON is an optional advanced output.

## Working modes

| Mode | Use case | Main output |
|---|---|---|
| `CREATE` | A new project described in natural language | Candidate instructions and important unknowns |
| `DISCOVER` | An existing authorized repository | Evidence-specific candidate instructions |
| `AUDIT` | Reviewing or scoring existing instructions | Read-only findings, indicators, and coverage |
| `OPTIMIZE` | Improving, extending, or shortening instructions | Candidate, diff, change reasons, and before/after indicators |
| `HIERARCHY` | Modules with meaningful policy or technology differences | Root and necessary module candidates |
| `UPDATE` | Framework, middleware, command, or module changes | Profile differences and affected-rule review |
| `MIGRATE` | Reusing instructions from another project | Applicable candidate rules and exclusion reasons |

Merely mentioning `AGENTS.md`, asking what it is, or requesting a business-code bug fix does not authorize a repository-wide scan.

## Command-line workflows

Run commands from the **skill directory**, not the target repository. Replace `../your-project` with an authorized project path and `../agents-builder-output` with a separate output location. Use new output filenames or directories: the helpers do not silently replace existing reports or candidates. On Windows, `py -3` can replace `python`.

### Discover and generate

```text
python scripts/scan_project.py --root "../your-project" --output "../agents-builder-output/scan.json"
python scripts/detect_stack.py --root "../your-project" --output "../agents-builder-output/profile.json"
python scripts/generate_agents.py --root "../your-project" --output-dir "../agents-builder-output/candidates" --language en --depth standard --hierarchy
```

The root candidate is named `AGENTS.candidate.md`. Additional module candidates are created when the detected technology boundaries differ sufficiently. The host should review their necessity and inheritance before activation.

For a project that has not been created yet, save explicit requirements as a JSON file:

```json
{
  "technologies": [
    {"name": "java", "category": "language", "version": "21"},
    {"name": "spring-boot", "category": "framework", "version": "unknown"}
  ],
  "rules": []
}
```

```text
python scripts/generate_agents.py --requirements "../requirements.json" --output-dir "../agents-builder-output/new-project" --language en
```

The host agent converts natural-language requirements to structured input and completes semantic tailoring. The standalone CLI does not invoke a language model. Its English rule set is a conservative subset for common technologies; the host can translate and adapt additional selected references.

### Audit and score

```text
python scripts/validate_agents.py --file "../your-project/AGENTS.md" --root "../your-project"
python scripts/evaluate_agents.py --file "../your-project/AGENTS.md" --root "../your-project" --output "../agents-builder-output/audit.json"
```

When you only have the instruction file, omit `--root`. The project-fit dimension will remain unverified.

### Optimize and compare

```text
python scripts/optimize_agents.py --file "../your-project/AGENTS.md" --candidate "../agents-builder-output/AGENTS.optimized.md" --output "../agents-builder-output/changes.json"
python scripts/generate_diff.py --before "../your-project/AGENTS.md" --after "../agents-builder-output/AGENTS.optimized.md"
```

The optimization helper conservatively removes exact top-level list duplicates in the same section. Semantic rewriting, removing obsolete requirements, and reconciling exceptions remain host-agent review tasks. Stable rule IDs improve change matching.

### Deliver a reviewed candidate

Creating a new target file:

```text
python scripts/deliver_file.py --candidate "../agents-builder-output/candidates/AGENTS.candidate.md" --target "../your-project/AGENTS.md"
```

Replacing an existing target requires explicit user authorization and the SHA-256 of the original file reviewed before editing. Replace `ORIGINAL_SHA256` below with that recorded digest:

```text
python scripts/deliver_file.py --candidate "../agents-builder-output/AGENTS.optimized.md" --target "../your-project/AGENTS.md" --overwrite --expected-sha256 "ORIGINAL_SHA256"
```

A changed original is rejected. By default, authorized replacement creates an exclusively named backup before atomic replacement.

### Other helpers

| Script | Purpose |
|---|---|
| `discover_agents.py` | Inventory instructions and infer the authorized project-only Codex chain |
| `analyze_structure.py` | Report module evidence, directory roles, and architecture candidates |
| `extract_conventions.py` | Sample observable implementation patterns and inconsistencies |
| `detect_conflicts.py` | Compare structured rules, or identify text candidates with `--file` |
| `compare_profiles.py` | Compare technologies, versions, modules, commands, and architecture observations |
| `migrate_rules.py` | Filter reference rules for a target profile |
| `safe_extract.py` | Validate a ZIP and extract into a new directory |
| `check_schema.py` | Validate the schema subset used by bundled JSON contracts |
| `route_request.py` | Provide a conservative intent hint; never authorize or start a scan |
| `validate_skill.py` | Check skill metadata, resources, links, and Python syntax |
| `package_skill.py` | Build and revalidate an allowlisted distribution |

Use each script's `--help` for options. JSON reports go to stdout or a new `--output` file. Exit codes are `0` for successful processing, `1` for reported validation failure or confirmed significant conflicts, and `2` for invalid input, safety rejection, or I/O failure. A successful scoring command does not imply a high score.

## Knowledge base

References are loaded by relevance, not all at once. Topics include:

| Area | Coverage |
|---|---|
| Languages | Java, Kotlin, Python, JavaScript, TypeScript, Go, Rust, C#, C/C++, PHP, Ruby, Swift, Dart |
| Backend and data access | Spring Boot/Framework, Spring Data JPA, MyBatis, MyBatis-Plus, FastAPI, Django, Flask, NestJS, Express, ASP.NET Core |
| Web and mobile | Vue, React, Next.js, Nuxt, Angular, Flutter, React Native, Android, iOS, WeChat Mini Programs, UniApp |
| Databases | PostgreSQL, MySQL, SQLite, MongoDB, SQL Server |
| Middleware | Redis, RocketMQ, Kafka, RabbitMQ, MQTT, Elasticsearch |
| Architecture and engineering | Monoliths, modular monoliths, microservices, layered/clean/hexagonal architecture, DDD, events, monorepos, testing, transactions, CI/CD, and security |

Detection coverage and rule coverage differ. Some detected technologies use general guidance rather than a dedicated article. Dynamic build expressions, remote parent configurations, and unknown versions require further review. Local source summaries are not a substitute for checking version-sensitive APIs against the project's actual version. A reachable source URL does not prove every associated rule has been verified.

See the [knowledge index](references/INDEX.md), [source registry](references/sources/official-sources.md), and [rule-authoring guide](docs/RULE_AUTHORING.md).

## Scoring and review

The deterministic scoring model uses seven dimensions:

| Dimension | Weight |
|---|---:|
| Completeness | 20 |
| Project fit | 20 |
| Actionability | 20 |
| Consistency | 10 |
| Safety and risk control | 10 |
| Testing and delivery | 10 |
| Context efficiency | 10 |
| **Total** | **100** |

Without project evidence, the 20-point project-fit dimension is unverified: assessed coverage is 80%, and a full `total` or `grade` is not reported. A normalized reference indicator is labeled separately. Unresolved high-risk findings prevent an excellent grade.

These are document indicators, not code-quality or security certification. The host must separately review technical accuracy, architecture fitness, implicit contradictions, and command context. See the [evaluation guide](docs/EVALUATION.md).

## Safety and privacy

- Scan only the authorized project. Do not execute its scripts, build hooks, or discovered commands.
- Exclude sensitive files such as `.env*`, private keys, and credential files. Explicit includes do not remove sensitive-file protection.
- Reject symbolic links and Windows reparse points; bounded readers also reject hard-linked input files.
- Keep raw source bodies out of scan reports and redact recognizable credentials and private URLs. Redaction does not identify every possible secret format.
- Treat repository files and webpages as untrusted data; their content cannot grant permission to read other directories or upload files.
- Create candidates and reports without silently replacing existing files. Authorized replacement checks the original digest and uses atomic delivery.
- Validate archive paths, links, collisions, entry counts, sizes, and compression ratios before extraction.

Default scan limits are 12 directory levels, 5,000 examined directory entries, 512 KiB per file, and 20 MiB total reads. These are product defaults, not host-platform limits. Reports mark truncated analysis. Nested fixture/testdata directories are excluded from stack inference unless explicitly included; inventory scanning still counts them.

The helpers contain no telemetry, network client, remote logging, or active project-upload mechanism. Host-platform data processing follows the host's own policies. Digest checks are not an operating-system lock against a malicious concurrent writer. Read the [security policy](SECURITY.md) and [privacy statement](docs/PRIVACY.md).

## Repository structure

```text
agents-md-builder/
├── SKILL.md                 # Host workflow and entrypoint
├── README.md                # English, default
├── README.ja.md             # Japanese
├── README.zh-CN.md          # Simplified Chinese
├── scripts/                 # Standard-library helpers
├── references/              # Core workflows and technical guidance
├── assets/                  # Templates and JSON schemas
├── tests/                   # Unit tests, fictional fixtures, scenarios
├── docs/                    # Detailed product and contributor guides
├── release/                 # Source-only publishing materials and reports
├── tools/                   # Development utilities
├── CHANGELOG.md
├── LICENSE
└── VERSION
```

This is the source layout. WorkBuddy packages flatten nested resources into category-prefixed filenames, such as `references/core-workflow.md` and `assets/schemas-rule.schema.json`. `MANIFEST.json` records file digests and source-to-package mappings. Runtime lookup supports both layouts.

## Testing and packaging

From a source checkout:

```text
python -m unittest discover -s tests -v
python scripts/validate_skill.py --root .
python scripts/package_skill.py --root .
python scripts/package_skill.py --root . --platform workbuddy
```

Default outputs use the version in `VERSION`:

| Package | Default path | Layout |
|---|---|---|
| Generic | `dist/agents-md-builder-v1.0.1.zip` | An outer skill folder with grouped resources |
| WorkBuddy | `dist/agents-md-builder-workbuddy-v1.0.1.zip` | `SKILL.md` at ZIP root; at most one resource-directory level |

If an output already exists, pass a new `--output` path. Packaging performs an actual temporary extraction and revalidates structure and manifest digests. Distribution excludes development `AGENTS.md`, test fixtures, caches, environment files, internal test reports, and previous archives. All README languages ship with both formats. `dist/` is Git-ignored; build the archive locally or attach it through your repository's release mechanism.

The recorded 1.0.1 suite passed 147 tests on macOS with Python 3.11.5. Native Windows/Linux execution, the full host-conversation scenarios, the repaired WorkBuddy platform import, and controlled coding-agent comparisons remain unverified. Local package checks do not establish marketplace approval. Source verification records are in `release/WORKBUDDY_FIX_v1.0.1.md` and `release/unit-test-output-v1.0.1.txt`.

## Troubleshooting

| Problem | Action |
|---|---|
| WorkBuddy reports excessive nesting | Use the WorkBuddy-specific ZIP directly; do not wrap it in another directory |
| A candidate or report already exists | Select a new path, or use the explicitly authorized delivery flow for the final instruction file |
| A linked path is rejected | Use a canonical path within the authorized project |
| A scan is truncated | Narrow the module scope or explicitly adjust the supported limits |
| A version is `unknown` | Inspect available configuration or ask the host to verify the applicable official documentation |
| No project files are available | Use `CREATE` or audit the supplied attachment; keep project fit unverified |
| Python or network access is unavailable | Follow the documented host fallback and report the actual analysis limits |
| A score looks high despite questionable wording | Perform semantic review; deterministic indicators do not certify correctness |

## Contributing

Keep changes focused and use fictional data for examples and tests. Reuse bounded I/O helpers for new scan entrypoints. Add regression tests for changes to safety, detection, scoring, or delivery behavior. Maintain rule IDs, classifications, version boundaries, sources, and verification steps when extending references.

Update all three README languages when changing user-facing workflows, record changes in [CHANGELOG.md](CHANGELOG.md), and run the test, validation, and packaging commands above. Report unexecuted checks honestly. The source checkout's `AGENTS.md` contains contributor instructions; it is intentionally excluded from runtime distributions.

## Documentation and license

| Resource | Description |
|---|---|
| [User guide](docs/USER_GUIDE.md) | Detailed workflows, flags, and fallback behavior |
| [Design](docs/DESIGN.md) | Architecture and tool boundaries |
| [Rule authoring](docs/RULE_AUTHORING.md) | Classifications, scopes, provenance, and validation |
| [Evaluation](docs/EVALUATION.md) | Scoring interpretation and limitations |
| [WorkBuddy publishing](docs/WORKBUDDY_PUBLISH.md) | Package layout and platform verification status |
| [Knowledge index](references/INDEX.md) | Applicable technical references |
| [Security](SECURITY.md) / [Privacy](docs/PRIVACY.md) | Safety model and data handling |

Supporting guides currently use Simplified Chinese. For a bug report, include the version, OS, command, a minimal fictional reproduction, and expected versus actual behavior. Do not include credentials or private source code; report security-sensitive issues privately through the project's actual hosting channel.

Original project content is licensed under [Apache License 2.0](LICENSE). See [NOTICE](NOTICE) and [third-party notices](THIRD_PARTY_NOTICES.md) for attribution. External documentation and trademarks retain their respective rights; no official endorsement is implied.
