# AGENTS.md Builder

[English](README.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md)

**リポジトリの実際の情報を、AI コーディングエージェントが実行できる開発ルールへ。**

バージョン **1.0.1** · 提供者 **Safe Link** · ライセンス **Apache-2.0**

AGENTS.md Builder は、プロジェクト固有の `AGENTS.md` を生成、監査、採点、改善、保守するローカル Agent Skill です。設定ファイル、モジュールの境界、代表的なコード、ユーザーが確認した要件を分析し、必要な技術資料だけを参照して開発ルールを作成します。

自然言語の理解や意味に関する判断はホストエージェントが担当し、Python ツールは読み取り範囲を制限した静的分析と再現可能なチェックを担当します。基本機能に有料 API、API キー、データベース、バックエンドサービス、Docker 環境、MCP サーバーは不要です。

## 目次

- [主な機能](#主な機能)
- [動作要件](#動作要件)
- [インストール](#インストール)
- [クイックスタート](#クイックスタート)
- [動作モード](#動作モード)
- [コマンドラインでの操作](#コマンドラインでの操作)
- [ナレッジベース](#ナレッジベース)
- [採点とレビュー](#採点とレビュー)
- [安全性とプライバシー](#安全性とプライバシー)
- [リポジトリ構成](#リポジトリ構成)
- [テストとパッケージ作成](#テストとパッケージ作成)
- [トラブルシューティング](#トラブルシューティング)
- [コントリビューション](#コントリビューション)
- [関連ドキュメントとライセンス](#関連ドキュメントとライセンス)

## 主な機能

- **根拠に基づく調査：** プロジェクトのコードを実行せず、技術スタック、宣言されたバージョン、ビルド境界、既存の指示ファイル、代表的な実装パターンを検出します。
- **プロジェクト別の生成：** 確認済みの設計判断、既存の規約、独自要件を尊重し、不明な点は不明のまま明示します。
- **監査と改善：** Markdown、認証情報のリスク、参照先パス、バージョンの不一致、静的に確認できるコマンド宣言を検査し、候補ファイルと差分を作成します。
- **適用範囲を考慮した競合検出：** 構造化ルールの範囲、強度、明示的なキーを比較します。自然文の一致は意味レビューが必要な候補として扱います。
- **複数モジュールへの対応：** プロジェクトの根拠に応じて、全体共通ルールとモジュール固有の差分を分けます。
- **保守と移行：** 更新前後のプロファイルを比較し、他プロジェクトから移すルールの適用可否を確認します。
- **ローカル実行：** Python 標準ライブラリだけを使用します。オフラインでもローカル資料を利用でき、Python がない場合はホストによる手動調査へ切り替えます。

既存コードの書き方は観察結果であり、そのまま推奨実装になるわけではありません。すべてのプロジェクトに同じアーキテクチャを強制したり、未指定のフレームワークバージョンを決定したりしません。

## 動作要件

| 項目 | 要件 |
|---|---|
| エージェントによる実行 | Agent Skills を読み込み、許可されたファイルを参照できるホスト |
| 決定的な補助ツール | Python 3.10 以上。標準ライブラリのみ |
| ファイルの出力 | 指定した候補・レポート用ディレクトリへの書き込み権限 |
| ネットワーク | 任意。ホストが公開の公式資料を確認する場合に使用 |
| OS | クロスプラットフォーム実装。ネイティブ実行の確認済み環境は macOS |

Python がなくても、ホストは同じ安全方針に沿って必要なファイルを限定的に読み取れます。ネットワークを使えない場合はローカル資料で続行し、最新資料で未確認の内容を明示します。

リポジトリの既定 README は英語です。生成する規約の言語設定とは別で、CLI は `--language en` と `--language zh` に対応し、既定値は `zh` です。この日本語 README は日本語専用 CLI 出力モードの追加を意味しません。詳細ガイドとナレッジベースの多くは現在、簡体字中国語で提供しています。

## インストール

### WorkBuddy

`--platform workbuddy` で作成する **WorkBuddy 専用 ZIP** を使います。

1. クライアントのスキルアップロード・インポート画面で `agents-md-builder-workbuddy-v1.0.1.zip` を選択します。
2. ZIP をそのままアップロードします。アーカイブ直下に `SKILL.md` があり、リソースのディレクトリ階層は1段だけです。
3. スキルを有効にし、アクセスを許可するプロジェクトを選択するか、必要なファイルを添付します。
4. 最初は候補の生成、または読み取り専用の監査を依頼します。

フォルダーとして手動導入する場合は、`agents-md-builder` というディレクトリを作り、その直下へ ZIP の内容を展開します。`SKILL.md` がそのディレクトリの直下にある状態にしてください。

1.0.0 の ZIP はディレクトリの階層超過で拒否されました。1.0.1 の WorkBuddy 専用 ZIP はリソースを平坦化し、参照先も書き換えています。再圧縮するときに外側のフォルダーを追加しないでください。修正後のパッケージはローカルで展開・実行を確認していますが、WorkBuddy でのインポート成功やマーケット審査通過は未確認です。[公開ガイド](docs/WORKBUDDY_PUBLISH.md)を参照してください。

### Codex などの Agent Skills 対応ホスト

汎用 ZIP またはソースのスキルディレクトリを使います。汎用 ZIP には `agents-md-builder/` があり、その中に `SKILL.md` があります。このフォルダーをホストが指定するスキル保存先へ配置し、必要に応じて有効化または再読み込みしてください。

`scripts/`、`references/`、`assets/` は `SKILL.md` と一緒に配置します。入口ファイルだけでは、このスキルに必要なリソースが不足します。指示の読み込み、override の扱い、コンテキスト上限はホストによって異なります。

## クイックスタート

インストールとプロジェクトへのアクセス許可が済んだら、ホストに依頼します。以下は英語出力を指定する例です。

> Generate an AGENTS.md candidate for this repository in English. Use actual project evidence, preserve confirmed requirements, and keep the existing file unchanged.

> Audit this AGENTS.md without modifying it. Show issue locations, risks, score coverage, and assumptions that could not be verified.

> Improve the current AGENTS.md. Preserve mandatory rules and exceptions, merge duplicates within the same scope, and provide a candidate plus a diff.

新規プロジェクトでは、決定済みの内容を伝えます。

> Java 21、Spring Boot、Spring Data JPA、PostgreSQL を使うプロジェクトの AI 開発ルールを英語で作成してください。フレームワークのバージョンは未定です。不明と明記し、ビルドコマンドは推測しないでください。

ワークフローは根拠の収集、必要な資料の読み込み、候補作成、実行可能なチェック、未解決事項の報告へ進みます。通常の生成では規約ファイルと簡潔な説明を返します。監査では問題一覧、最適化では候補と変更レポートを返します。スキャン JSON などの中間成果物は任意です。

## 動作モード

| モード | 用途 | 主な出力 |
|---|---|---|
| `CREATE` | 自然言語で説明された新規プロジェクト | 規約候補と重要な未確定事項 |
| `DISCOVER` | 許可された既存リポジトリ | プロジェクトの根拠を反映した規約候補 |
| `AUDIT` | 既存規約の確認・採点 | 読み取り専用の指摘、指標、評価カバレッジ |
| `OPTIMIZE` | 規約の改善・拡張・短縮 | 候補、差分、変更理由、変更前後の指標 |
| `HIERARCHY` | 規約や技術に実質的な違いがあるモジュール | 全体共通と必要なモジュール別の候補 |
| `UPDATE` | フレームワーク・ミドルウェア・コマンド・モジュールの変更 | プロファイル差分と影響を受けるルールの確認 |
| `MIGRATE` | 他プロジェクトの規約の再利用 | 適用可能なルール候補と除外理由 |

`AGENTS.md` に言及しただけ、意味を質問しただけ、業務コードのバグ修正を依頼しただけでは、リポジトリ全体のスキャンを許可したことにはなりません。

## コマンドラインでの操作

コマンドは対象プロジェクトではなく、**スキルのディレクトリ**から実行します。`../your-project` は許可するプロジェクトに、`../agents-builder-output` は別の出力先に置き換えてください。既存のレポートや候補を無断で置き換えないため、未使用の出力パスを選びます。Windows では `python` の代わりに `py -3` を使用できます。

### 調査と生成

```text
python scripts/scan_project.py --root "../your-project" --output "../agents-builder-output/scan.json"
python scripts/detect_stack.py --root "../your-project" --output "../agents-builder-output/profile.json"
python scripts/generate_agents.py --root "../your-project" --output-dir "../agents-builder-output/candidates" --language en --depth standard --hierarchy
```

ルート候補は `AGENTS.candidate.md` です。検出した技術境界に十分な違いがある場合、モジュール別候補も作成します。有効化する前に、ホストが必要性と継承関係を確認してください。

まだコードがない新規プロジェクトでは、明示的な要件を JSON に保存します。

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

自然言語を構造化入力へ変換し、意味を確認して調整するのはホストです。CLI 単体では言語モデルを呼び出しません。CLI の英語ルールは主要技術向けの限定的な内容で、ホストは必要に応じて選択済み資料を翻訳・補完できます。

### 監査と採点

```text
python scripts/validate_agents.py --file "../your-project/AGENTS.md" --root "../your-project"
python scripts/evaluate_agents.py --file "../your-project/AGENTS.md" --root "../your-project" --output "../agents-builder-output/audit.json"
```

規約ファイルだけを持っている場合は `--root` を省略します。プロジェクトへの適合性は未検証として扱います。

### 最適化と差分確認

```text
python scripts/optimize_agents.py --file "../your-project/AGENTS.md" --candidate "../agents-builder-output/AGENTS.optimized.md" --output "../agents-builder-output/changes.json"
python scripts/generate_diff.py --before "../your-project/AGENTS.md" --after "../agents-builder-output/AGENTS.optimized.md"
```

最適化ツールは同じ節の最上位リストで、完全に一致する重複項目だけを保守的に除去します。意味のある書き換え、古い要件の削除、例外の整理はホストがレビューします。安定したルール ID があると変更を対応付けやすくなります。

### 確認済み候補の反映

対象ファイルがまだ存在しない場合：

```text
python scripts/deliver_file.py --candidate "../agents-builder-output/candidates/AGENTS.candidate.md" --target "../your-project/AGENTS.md"
```

既存ファイルの置換には、ユーザーの明示的な許可と、編集前に確認した元ファイルの SHA-256 が必要です。次の `ORIGINAL_SHA256` を、その記録済みハッシュに置き換えます。

```text
python scripts/deliver_file.py --candidate "../agents-builder-output/AGENTS.optimized.md" --target "../your-project/AGENTS.md" --overwrite --expected-sha256 "ORIGINAL_SHA256"
```

元ファイルが変わっていた場合は拒否します。許可された置換では、既定で既存ファイルと競合しない名前のバックアップを作成し、アトミックに置換します。

### その他のツール

| スクリプト | 用途 |
|---|---|
| `discover_agents.py` | 指示ファイル一覧と、許可されたプロジェクト内の Codex 指示チェーンの推定 |
| `analyze_structure.py` | モジュールの根拠、ディレクトリの役割、アーキテクチャ候補 |
| `extract_conventions.py` | 実装パターンと不一致のサンプル調査 |
| `detect_conflicts.py` | 構造化ルールの比較。`--file` では自然文の競合候補を提示 |
| `compare_profiles.py` | 技術・バージョン・モジュール・コマンド・構造観察の比較 |
| `migrate_rules.py` | 対象プロファイルに適合する参照ルールの選別 |
| `safe_extract.py` | ZIP を検証し、新規ディレクトリへ安全に展開 |
| `check_schema.py` | 同梱 JSON 契約が使う schema の部分集合を検証 |
| `route_request.py` | 保守的な意図判定のヒント。スキャンの許可や開始は行わない |
| `validate_skill.py` | メタデータ、リソース、リンク、Python 構文の検証 |
| `package_skill.py` | 許可リストに基づく配布物の作成と再検証 |

各スクリプトの `--help` で引数を確認できます。JSON は標準出力、または新規 `--output` ファイルに出力します。終了コードは成功が `0`、検証不合格や確定した重大競合が `1`、入力不正・安全上の拒否・I/O エラーが `2` です。採点コマンドの成功は高得点を意味しません。

## ナレッジベース

関連する資料だけを読み込みます。

| 分野 | 対象 |
|---|---|
| 言語 | Java、Kotlin、Python、JavaScript、TypeScript、Go、Rust、C#、C/C++、PHP、Ruby、Swift、Dart |
| バックエンド・データアクセス | Spring Boot/Framework、Spring Data JPA、MyBatis、MyBatis-Plus、FastAPI、Django、Flask、NestJS、Express、ASP.NET Core |
| Web・モバイル | Vue、React、Next.js、Nuxt、Angular、Flutter、React Native、Android、iOS、微信ミニプログラム、UniApp |
| データベース | PostgreSQL、MySQL、SQLite、MongoDB、SQL Server |
| ミドルウェア | Redis、RocketMQ、Kafka、RabbitMQ、MQTT、Elasticsearch |
| アーキテクチャ・開発 | モノリス、モジュラーモノリス、マイクロサービス、レイヤード・クリーン・ヘキサゴナル、DDD、イベント、モノレポ、テスト、トランザクション、CI/CD、安全性 |

技術の検出範囲と専用ルールの範囲は異なります。検出できても一般的な指針だけを提供する技術があります。動的ビルド式、リモート親設定、不明なバージョンは追加確認が必要です。バージョン依存 API は実際のプロジェクト版で確認してください。URL にアクセスできたことだけでは、関連するすべてのルールを検証済みとはいえません。

[資料索引](references/INDEX.md)、[出典一覧](references/sources/official-sources.md)、[ルール作成ガイド](docs/RULE_AUTHORING.md)を参照してください。

## 採点とレビュー

決定的な採点モデルは7項目で構成します。

| 項目 | 配点 |
|---|---:|
| 完全性 | 20 |
| プロジェクトへの適合性 | 20 |
| 実行の明確さ | 20 |
| 一貫性 | 10 |
| 安全性とリスク管理 | 10 |
| テストと成果物の検証 | 10 |
| コンテキスト効率 | 10 |
| **合計** | **100** |

プロジェクトの根拠がない場合、適合性の20点は未検証です。評価カバレッジは80%となり、完全な `total` や `grade` は出しません。正規化した参考指標は別に表示します。未解決の高リスク問題がある場合、優秀な評価にはなりません。

これは文書の指標であり、コード品質や安全性の認証ではありません。ホストは技術的正確さ、設計への適合性、暗黙の矛盾、コマンドの実行条件を別途確認します。[評価ガイド](docs/EVALUATION.md)を参照してください。

## 安全性とプライバシー

- 許可されたプロジェクトだけを読み取り、対象のスクリプト、ビルドフック、検出したコマンドは実行しません。
- `.env*`、秘密鍵、認証ファイルなどは除外します。明示的な include 指定でも、この保護は解除しません。
- シンボリックリンクと Windows reparse point を拒否します。制限付き読み取りではハードリンクされた入力も拒否します。
- スキャンレポートにソース本文を出力せず、識別可能な認証情報や非公開 URL をマスクします。すべての秘密情報形式を検出できるとは限りません。
- リポジトリや Web ページの内容は分析対象のデータであり、外部ディレクトリへのアクセスやアップロードを許可する指示として扱いません。
- 候補やレポートを無断で上書きしません。許可済み置換では元ファイルのハッシュを確認し、アトミックに反映します。
- ZIP 展開前にパス、リンク、衝突、項目数、サイズ、圧縮率を検証します。

既定のスキャン上限はディレクトリ深さ12、確認するディレクトリエントリ5,000件、1ファイル512 KiB、合計読み取り20 MiBです。製品側の既定値であり、ホストの制限ではありません。打ち切り時はその状態を報告します。入れ子の fixture/testdata は明示指定しない限り技術スタックの推定から除外しますが、ファイル一覧のスキャンでは数えます。

補助ツールにテレメトリ、ネットワーククライアント、リモートログ、プロジェクトの能動的なアップロード機構はありません。ホスト自身のデータ処理には、そのプラットフォームの方針が適用されます。ハッシュ照合は悪意のある並行書き込みを OS レベルで防ぐロックではありません。[安全性の方針](SECURITY.md)と[プライバシー説明](docs/PRIVACY.md)を参照してください。

## リポジトリ構成

```text
agents-md-builder/
├── SKILL.md                 # ホストのワークフローと入口
├── README.md                # 英語・既定
├── README.ja.md             # 日本語
├── README.zh-CN.md          # 簡体字中国語
├── scripts/                 # 標準ライブラリによる補助ツール
├── references/              # ワークフローと技術資料
├── assets/                  # テンプレートと JSON schema
├── tests/                   # 単体テスト・架空プロジェクト・シナリオ
├── docs/                    # 詳細ガイド
├── release/                 # ソース側の公開資料と記録
├── tools/                   # 開発用ユーティリティ
├── CHANGELOG.md
├── LICENSE
└── VERSION
```

これはソース側の構成です。WorkBuddy 配布物では、例えば `references/core-workflow.md`、`assets/schemas-rule.schema.json` のようにカテゴリ名をファイル名へ付けて平坦化します。`MANIFEST.json` にハッシュと元パスの対応を記録し、実行時の参照は両方の構成に対応します。

## テストとパッケージ作成

ソースディレクトリから実行します。

```text
python -m unittest discover -s tests -v
python scripts/validate_skill.py --root .
python scripts/package_skill.py --root .
python scripts/package_skill.py --root . --platform workbuddy
```

既定の出力名は `VERSION` に従います。

| 形式 | 既定のパス | 構成 |
|---|---|---|
| 汎用 | `dist/agents-md-builder-v1.0.1.zip` | スキルの外側フォルダーと分野別のリソース |
| WorkBuddy | `dist/agents-md-builder-workbuddy-v1.0.1.zip` | ZIP 直下に SKILL.md、リソースのディレクトリは1段まで |

既存出力がある場合は `--output` に新しいパスを指定します。パッケージ作成では実際に一時展開し、構造と manifest のハッシュを再検証します。開発用 `AGENTS.md`、テストデータ、キャッシュ、環境ファイル、内部テスト記録、旧 ZIP は含めません。README の各言語版は両形式に同梱します。`dist/` は Git 管理対象外なので、ローカルでビルドするか、リポジトリのリリース機能に添付してください。

記録済みの1.0.1テストは macOS / Python 3.11.5 で147件すべて成功しています。Windows/Linux のネイティブ実行、完全なホスト対話シナリオ、修正後の WorkBuddy インポート、条件を統一したコーディングエージェント比較は未検証です。ローカル検証はマーケット審査通過を意味しません。ソース側の記録は `release/WORKBUDDY_FIX_v1.0.1.md` と `release/unit-test-output-v1.0.1.txt` にあります。

## トラブルシューティング

| 状況 | 対応 |
|---|---|
| WorkBuddy が階層超過を報告する | 専用 ZIP をそのまま使い、外側フォルダーを追加しない |
| 候補やレポートがすでに存在する | 新しいパスを選ぶ。最終規約の置換には明示的な許可が必要 |
| リンクされたパスが拒否される | 許可した範囲内の実パスを使用する |
| スキャンが途中で打ち切られる | 対象をモジュールに絞るか、上限を明示的に調整する |
| バージョンが `unknown` になる | 設定を追加確認するか、ホストに該当する公式資料の確認を依頼する |
| プロジェクトファイルがない | `CREATE` または添付規約の監査を使い、適合性は未検証とする |
| Python やネットワークがない | ホストの代替手順を使い、実際の制限を報告する |
| 文面に問題がありそうなのに高得点になる | 意味レビューを実施する。指標だけでは正しさを保証しない |

## コントリビューション

変更範囲を限定し、例やテストには架空データを使ってください。新規スキャン入口では制限付き I/O ヘルパーを再利用します。安全性、検出、採点、反映処理を変更する場合は回帰テストを追加してください。資料を拡張する際は、ルール ID、分類、対象バージョン、出典、検証手順を維持します。

利用方法を変更するときは3言語の README を更新し、[CHANGELOG.md](CHANGELOG.md)に記録して、上記のテスト・検証・パッケージコマンドを実行してください。未実行の検証は明記します。ソースの `AGENTS.md` は開発者向け指示であり、実行用配布物には含めません。

## 関連ドキュメントとライセンス

| 資料 | 内容 |
|---|---|
| [ユーザーガイド](docs/USER_GUIDE.md) | 詳細な操作・引数・代替手順 |
| [設計](docs/DESIGN.md) | アーキテクチャとツールの境界 |
| [ルール作成](docs/RULE_AUTHORING.md) | 分類・範囲・出典・検証 |
| [評価](docs/EVALUATION.md) | 採点の解釈と制限 |
| [WorkBuddy 公開](docs/WORKBUDDY_PUBLISH.md) | 配布構成とプラットフォーム検証状況 |
| [ナレッジ索引](references/INDEX.md) | 関連する技術資料 |
| [安全性](SECURITY.md) / [プライバシー](docs/PRIVACY.md) | 安全方針とデータ処理 |

関連ガイドは現在、簡体字中国語です。不具合報告にはバージョン、OS、コマンド、架空データによる最小再現、期待する結果と実際の結果を添えてください。認証情報や非公開コードは含めず、安全性に関わる問題は実際のプロジェクトホスティング先の非公開窓口で報告してください。

本プロジェクトの独自コンテンツは [Apache License 2.0](LICENSE) で公開しています。[NOTICE](NOTICE)と[第三者資料に関する表示](THIRD_PARTY_NOTICES.md)も確認してください。外部文書や商標の権利は各権利者に帰属し、公式な推奨や承認を意味しません。
