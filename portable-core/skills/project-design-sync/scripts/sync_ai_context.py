from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

AUTO_BEGIN = "<!-- AUTO-SYNC:BEGIN -->"
AUTO_END = "<!-- AUTO-SYNC:END -->"
COMMON_SOURCE_ROOTS = ("src", "app", "apps", "packages", "services", "modules", "backend", "frontend", "server", "client", "lib")
APP_ROOT_MARKER_FILES = (
    "package.json",
    "go.mod",
    "Cargo.toml",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "pyproject.toml",
    "requirements.txt",
    "setup.py",
    "vite.config.ts",
    "vite.config.js",
)
APP_ROOT_MARKER_DIRS = ("src", "app", "cmd", "internal", "web")
DESIGN_SOURCE_HINTS = ("docs", "doc", "design", "architecture", "adr", "spec", "specs", "rfcs", "openspec")
DEFAULT_IGNORE_PATHS = (".git", "ai-context", "node_modules", "dist", "build", "coverage", "target", "bin", "obj", "out", ".next", ".turbo", ".venv", "venv")
SKIP_MODULE_NAMES = {"assets", "common", "components", "config", "core", "fixtures", "generated", "hooks", "i18n", "images", "lib", "locales", "migrations", "public", "shared", "styles", "test", "tests", "types", "utils"}
ENTRYPOINT_FILES = {"main.py", "app.py", "manage.py", "server.js", "server.ts", "index.js", "index.ts", "main.go", "Program.cs", "main.rs"}
INTERFACE_KEYWORDS = ("route", "router", "controller", "resolver", "endpoint", "api", "webhook")
RUNTIME_KEYWORDS = ("worker", "job", "queue", "cron", "schedule", "scheduler", "background", "event", "listener")
SEAM_KEYWORDS = ("adapter", "strategy", "factory", "provider", "repository", "policy", "gateway", "handler", "plugin", "middleware")
TEXT_EVIDENCE_SUFFIXES = {".md", ".mdx", ".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".kt", ".go", ".rs", ".cs", ".json", ".yaml", ".yml", ".toml", ".xml", ".sql", ".proto", ".graphql", ".gql", ".sh", ".ps1", ".txt", ".rst"}
TEXT_EVIDENCE_FILENAMES = {"dockerfile", "makefile", "procfile"}


def render_evidence_sections(
    high_confidence: Sequence[str],
    heuristic: Sequence[str],
    review_needed: Sequence[str],
) -> list[str]:
    lines: list[str] = []
    sections = (
        ("### High-Confidence Evidence", [item for item in high_confidence if item]),
        ("### Heuristic Signals", [item for item in heuristic if item]),
        ("### Needs Human Review", [item for item in review_needed if item]),
    )
    for heading, items in sections:
        if not items:
            continue
        if lines:
            lines.append("")
        lines.append(heading)
        lines.append("")
        lines.extend(items)
    return lines or ["- no evidence captured"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync ai-context design docs from repository evidence.")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--mode", choices=("full", "local"), default="full")
    parser.add_argument("--layer", choices=("auto", "architecture", "detail", "all"), default="auto")
    parser.add_argument("--targets", nargs="*", default=[], help="Module targets for local sync")
    parser.add_argument("--config", default="ai-context/repo-layout.json", help="Repo-relative layout config path")
    parser.add_argument("--source-roots", nargs="*", default=[], help="Explicit repo-relative source roots")
    parser.add_argument("--design-sources", nargs="*", default=[], help="Explicit repo-relative design sources")
    parser.add_argument("--ignore-paths", nargs="*", default=[], help="Explicit repo-relative ignore paths")
    parser.add_argument(
        "--module-path",
        action="append",
        default=[],
        help="Declare or override module mapping as module=path1,path2 using repo-relative paths",
    )
    parser.add_argument("--include-design-sources", action="store_true", help="Include declared or detected design sources as auxiliary evidence")
    return parser.parse_args()


def expand_cli_values(values: Iterable[str]) -> list[str]:
    expanded: list[str] = []
    for value in values:
        for part in str(value).split(","):
            cleaned = part.strip()
            if cleaned:
                expanded.append(cleaned)
    return expanded


def normalize_path_string(value: str) -> str:
    cleaned = value.strip().replace("\\", "/")
    while "//" in cleaned:
        cleaned = cleaned.replace("//", "/")
    if cleaned in ("", ".", "./"):
        return "."
    return cleaned.rstrip("/")


def to_repo_relative(root: Path, value: str) -> str:
    candidate = Path(value)
    if candidate.is_absolute():
        try:
            return normalize_path_string(str(candidate.resolve().relative_to(root.resolve())))
        except ValueError:
            return normalize_path_string(str(candidate))
    return normalize_path_string(value)


def relative_path(root: Path, path: Path) -> str:
    try:
        rel = path.resolve().relative_to(root.resolve())
    except ValueError:
        return normalize_path_string(str(path))
    return normalize_path_string(str(rel))


def dedupe(values: Iterable[str]) -> list[str]:
    seen: dict[str, None] = {}
    for value in values:
        cleaned = normalize_path_string(value)
        if cleaned not in seen:
            seen[cleaned] = None
    return list(seen.keys())


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return ""
    except OSError:
        return ""


def line_count(path: Path) -> int:
    return len(read_text(path).splitlines())


def config_file_path(root: Path, value: str) -> Path:
    candidate = Path(value)
    return candidate if candidate.is_absolute() else root / normalize_path_string(value)


def is_initial_sync(root: Path) -> bool:
    sync_status = root / "ai-context" / "sync-status.md"
    if not sync_status.exists():
        return True
    text = read_text(sync_status)
    return "last_sync_mode: init-only" in text or "last_sync_at: not yet synced" in text


def resolve_sync_layer(root: Path, requested_layer: str, mode: str, targets: Sequence[str]) -> str:
    if requested_layer != "auto":
        return requested_layer
    if is_initial_sync(root):
        if mode == "local" and targets:
            return "detail"
        return "architecture"
    if mode == "local":
        return "detail"
    return "all"


def looks_like_app_root(path: Path) -> bool:
    return any((path / name).is_file() for name in APP_ROOT_MARKER_FILES) or any((path / name).is_dir() for name in APP_ROOT_MARKER_DIRS)


def is_text_evidence_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EVIDENCE_SUFFIXES or path.name.lower() in TEXT_EVIDENCE_FILENAMES


def has_module_evidence(path: Path) -> bool:
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            dirnames[:] = [name for name in dirnames if name not in DEFAULT_IGNORE_PATHS and name not in SKIP_MODULE_NAMES]
            for filename in filenames:
                candidate = Path(dirpath) / filename
                if candidate.is_file() and is_text_evidence_file(candidate):
                    return True
    except OSError:
        return False
    return False


def load_repo_layout(root: Path, config_path: Path) -> dict:
    result = {
        "path": relative_path(root, config_path),
        "exists": False,
        "valid": False,
        "error": "",
        "source_roots": [],
        "design_sources": [],
        "ignore_paths": [],
        "modules": {},
    }
    if not config_path.exists():
        return result

    result["exists"] = True
    try:
        payload = json.loads(read_text(config_path) or "{}")
    except json.JSONDecodeError as exc:
        result["error"] = f"invalid json: {exc.msg}"
        return result

    if not isinstance(payload, dict):
        result["error"] = "config root must be an object"
        return result

    def read_string_list(key: str) -> list[str]:
        raw = payload.get(key) or []
        if not isinstance(raw, list):
            return []
        return dedupe(str(item) for item in raw if isinstance(item, str))

    modules: dict[str, list[str]] = {}
    raw_modules = payload.get("modules") or {}
    if isinstance(raw_modules, dict):
        for name, spec in raw_modules.items():
            if not isinstance(name, str):
                continue
            paths: list[str] = []
            if isinstance(spec, dict):
                raw_paths = spec.get("paths") or []
                if isinstance(raw_paths, list):
                    paths = [str(item) for item in raw_paths if isinstance(item, str)]
            elif isinstance(spec, list):
                paths = [str(item) for item in spec if isinstance(item, str)]
            module_name = normalize_module(name)
            if module_name:
                modules[module_name] = dedupe(paths)

    result["valid"] = True
    result["source_roots"] = [to_repo_relative(root, item) for item in read_string_list("source_roots")]
    result["design_sources"] = [to_repo_relative(root, item) for item in read_string_list("design_sources")]
    result["ignore_paths"] = [to_repo_relative(root, item) for item in read_string_list("ignore_paths")]
    result["modules"] = {name: [to_repo_relative(root, path) for path in paths] for name, paths in modules.items()}
    return result


def detect_source_roots_heuristically(root: Path) -> list[str]:
    found: list[str] = []
    for name in COMMON_SOURCE_ROOTS:
        candidate = root / name
        if candidate.is_dir():
            found.append(relative_path(root, candidate))

    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name.startswith(".") or child.name in DEFAULT_IGNORE_PATHS:
            continue
        if looks_like_app_root(child):
            found.append(relative_path(root, child))

    if not found and looks_like_app_root(root):
        found.append(".")
    return dedupe(found)


def detect_design_sources_heuristically(root: Path, source_root_paths: Sequence[Path]) -> list[str]:
    detected: list[str] = []

    def looks_like_design_source(path: Path) -> bool:
        lowered = path.name.lower()
        return any(hint in lowered for hint in DESIGN_SOURCE_HINTS)

    def maybe_add(path: Path) -> None:
        rel = relative_path(root, path)
        if rel not in detected:
            detected.append(rel)

    for child in sorted(root.iterdir()):
        if child.is_dir() and not child.name.startswith(".") and looks_like_design_source(child):
            maybe_add(child)

    for source_root in source_root_paths:
        if not source_root.exists() or not source_root.is_dir():
            continue
        for child in sorted(source_root.iterdir()):
            if child.is_dir() and looks_like_design_source(child):
                maybe_add(child)

    return detected


def parse_module_path_specs(root: Path, values: Iterable[str]) -> dict[str, list[str]]:
    parsed: dict[str, list[str]] = {}
    for value in values:
        raw = str(value).strip()
        if "=" not in raw:
            continue
        name, raw_paths = raw.split("=", 1)
        module_name = normalize_module(name)
        paths = [to_repo_relative(root, part) for part in expand_cli_values([raw_paths])]
        if not module_name or not paths:
            continue
        parsed.setdefault(module_name, [])
        parsed[module_name].extend(paths)
    return {name: dedupe(paths) for name, paths in parsed.items()}


def merge_module_maps(*maps: dict[str, list[str]]) -> dict[str, list[str]]:
    merged: dict[str, list[str]] = {}
    for mapping in maps:
        for name, paths in mapping.items():
            merged.setdefault(name, [])
            merged[name].extend(paths)
    return {name: dedupe(paths) for name, paths in merged.items()}


def normalize_module(name: str) -> str:
    return name.strip().replace("_", "-").replace(" ", "-")


def should_treat_source_root_as_module(root: Path, source_root: Path) -> bool:
    return source_root != root and source_root.parent == root and looks_like_app_root(source_root)


def detect_modules_from_roots(root: Path, source_root_paths: Sequence[Path]) -> dict[str, list[str]]:
    modules: dict[str, list[str]] = {}
    for source_root in source_root_paths:
        if not source_root.exists() or not source_root.is_dir():
            continue
        if should_treat_source_root_as_module(root, source_root):
            module_name = normalize_module(source_root.name)
            modules.setdefault(module_name, [])
            modules[module_name].append(relative_path(root, source_root))
            continue

        for child in sorted(source_root.iterdir()):
            if not child.is_dir():
                continue
            lowered = child.name.lower()
            if lowered.startswith(".") or lowered in SKIP_MODULE_NAMES:
                continue
            if not has_module_evidence(child):
                continue
            module_name = normalize_module(child.name)
            modules.setdefault(module_name, [])
            modules[module_name].append(relative_path(root, child))
    return {name: dedupe(paths) for name, paths in modules.items()}


def resolve_existing_paths(root: Path, rel_paths: Sequence[str]) -> list[Path]:
    resolved: list[Path] = []
    for rel in rel_paths:
        path = root if rel == "." else root / rel
        if path.exists():
            resolved.append(path)
    return resolved


def should_skip_rel_path(rel_path: str, skipped_roots: Sequence[str]) -> bool:
    for skipped in skipped_roots:
        if skipped == ".":
            continue
        if rel_path == skipped or rel_path.startswith(skipped + "/"):
            return True
    return False


def walk_declared_paths(root: Path, include_paths: Sequence[str], ignore_paths: Sequence[str]) -> list[Path]:
    collected: list[Path] = []
    seen: set[str] = set()
    ignored = dedupe(ignore_paths)

    for rel in dedupe(include_paths):
        path = root if rel == "." else root / rel
        if not path.exists():
            continue

        if path.is_file():
            rel_file = relative_path(root, path)
            if not should_skip_rel_path(rel_file, ignored) and rel_file not in seen:
                seen.add(rel_file)
                collected.append(path)
            continue

        for dirpath, dirnames, filenames in os.walk(path):
            current = Path(dirpath)
            dirnames[:] = [
                name
                for name in dirnames
                if not should_skip_rel_path(relative_path(root, current / name), ignored)
            ]
            for filename in filenames:
                candidate = current / filename
                rel_file = relative_path(root, candidate)
                if should_skip_rel_path(rel_file, ignored):
                    continue
                if rel_file in seen:
                    continue
                seen.add(rel_file)
                collected.append(candidate)

    return collected


def collect_root_level_files(root: Path, ignore_paths: Sequence[str], design_sources: Sequence[str]) -> list[Path]:
    collected: list[Path] = []
    skipped = dedupe(list(ignore_paths) + list(design_sources))
    for child in root.iterdir():
        if not child.is_file():
            continue
        rel = relative_path(root, child)
        if should_skip_rel_path(rel, skipped):
            continue
        collected.append(child)
    return collected


def dedupe_paths(root: Path, paths: Sequence[Path]) -> list[Path]:
    seen: set[str] = set()
    unique: list[Path] = []
    for path in paths:
        rel = relative_path(root, path)
        if rel in seen:
            continue
        seen.add(rel)
        unique.append(path)
    return unique


def select_repo_scan_paths(context: dict, mode: str, targets: Sequence[str], layer: str) -> list[str]:
    if layer == "detail" and mode == "local":
        requested = [normalize_module(name) for name in targets if normalize_module(name)]
        if requested:
            selected: list[str] = []
            for module in requested:
                selected.extend(context["module_map"].get(module, []))
            if selected:
                return dedupe(selected)

    selected = list(context["source_roots"])
    for paths in context["module_map"].values():
        for rel in paths:
            if rel == ".":
                continue
            if should_skip_rel_path(rel, context["ignore_paths"]):
                continue
            if any(rel == source or rel.startswith(source + "/") for source in context["source_roots"] if source != "."):
                continue
            if any(rel == source or rel.startswith(source + "/") for source in context["design_sources"] if source != "."):
                continue
            selected.append(rel)
    return dedupe(selected)


def iter_repo_files(context: dict) -> Iterable[Path]:
    yield from context["repo_files"]


def iter_design_files(context: dict) -> Iterable[Path]:
    yield from context["design_files"]


def build_layout_context(root: Path, args: argparse.Namespace, resolved_layer: str) -> dict:
    layout = load_repo_layout(root, config_file_path(root, args.config))
    explicit_source_roots = [to_repo_relative(root, value) for value in expand_cli_values(args.source_roots)]
    explicit_design_sources = [to_repo_relative(root, value) for value in expand_cli_values(args.design_sources)]
    explicit_ignore_paths = [to_repo_relative(root, value) for value in expand_cli_values(args.ignore_paths)]
    explicit_module_map = parse_module_path_specs(root, args.module_path)

    source_roots = dedupe(explicit_source_roots or layout["source_roots"] or detect_source_roots_heuristically(root))
    source_root_paths = resolve_existing_paths(root, source_roots)
    design_sources = dedupe(explicit_design_sources or layout["design_sources"] or detect_design_sources_heuristically(root, source_root_paths))
    ignore_paths = dedupe(list(DEFAULT_IGNORE_PATHS) + layout["ignore_paths"] + explicit_ignore_paths)
    declared_modules = merge_module_maps(layout["modules"], explicit_module_map)
    heuristic_modules = detect_modules_from_roots(root, source_root_paths)
    all_modules = merge_module_maps(heuristic_modules, declared_modules)
    include_design_sources = bool(args.include_design_sources)

    base_context = {
        "layout": layout,
        "source_roots": source_roots,
        "source_root_paths": source_root_paths,
        "design_sources": design_sources,
        "ignore_paths": ignore_paths,
        "module_map": all_modules,
        "include_design_sources": include_design_sources,
        "resolved_layer": resolved_layer,
    }

    repo_scan_paths = select_repo_scan_paths(base_context, args.mode, args.targets, resolved_layer)
    repo_files = walk_declared_paths(root, repo_scan_paths, dedupe(list(ignore_paths) + list(design_sources)))
    repo_files.extend(collect_root_level_files(root, ignore_paths, design_sources))
    repo_files = dedupe_paths(root, repo_files)
    design_scan_paths = design_sources
    design_files = walk_declared_paths(root, design_scan_paths, ignore_paths) if include_design_sources and design_scan_paths else []
    design_files = dedupe_paths(root, design_files)

    base_context["repo_scan_paths"] = repo_scan_paths
    base_context["design_scan_paths"] = design_scan_paths
    base_context["repo_files"] = repo_files
    base_context["design_files"] = design_files
    return base_context


def find_tests(root: Path, context: dict) -> list[str]:
    found: list[str] = []
    names = {"test", "tests", "__tests__", "spec", "e2e", "cypress"}
    for path in iter_repo_files(context):
        rel = relative_path(root, path)
        if any(part.lower() in names for part in Path(rel).parts):
            parent = normalize_path_string(str(Path(rel).parent))
            if parent not in found:
                found.append(parent)
    return found[:12]


def detect_stack(root: Path, context: dict) -> dict[str, list[str]]:
    package_managers: list[str] = []
    frameworks: list[str] = []
    langs: list[str] = []

    def add_unique(bucket: list[str], value: str) -> None:
        if value not in bucket:
            bucket.append(value)

    package_files: list[Path] = []
    java_markers = False
    python_markers = False
    dotnet_markers = False

    for path in iter_repo_files(context):
        name = path.name
        lowered = name.lower()
        if name == "package.json":
            package_files.append(path)
            add_unique(langs, "JavaScript/TypeScript")
            add_unique(package_managers, "npm")
        elif lowered in {"pnpm-lock.yaml", "pnpm-workspace.yaml"}:
            add_unique(package_managers, "pnpm")
        elif lowered == "yarn.lock":
            add_unique(package_managers, "yarn")
        elif lowered in {"pyproject.toml", "requirements.txt", "setup.py"}:
            python_markers = True
            add_unique(langs, "Python")
        elif lowered == "go.mod":
            add_unique(langs, "Go")
        elif lowered in {"pom.xml", "build.gradle", "build.gradle.kts"}:
            java_markers = True
            add_unique(langs, "Java/Kotlin")
        elif lowered == "cargo.toml":
            add_unique(langs, "Rust")
        elif lowered.endswith(".csproj") or lowered.endswith(".fsproj") or lowered.endswith(".sln"):
            dotnet_markers = True
            add_unique(langs, ".NET")

    dependency_mapping = {
        "react": "React",
        "next": "Next.js",
        "vue": "Vue",
        "@angular/core": "Angular",
        "express": "Express",
        "fastify": "Fastify",
        "nestjs": "NestJS",
        "@nestjs/core": "NestJS",
    }

    for package_file in package_files[:12]:
        try:
            package = json.loads(read_text(package_file) or "{}")
        except json.JSONDecodeError:
            continue
        deps = set((package.get("dependencies") or {}).keys()) | set((package.get("devDependencies") or {}).keys())
        for dep, label in dependency_mapping.items():
            if dep in deps:
                add_unique(frameworks, label)

    if python_markers:
        python_text = "\n".join(
            read_text(path)
            for path in iter_repo_files(context)
            if path.name.lower() in {"pyproject.toml", "requirements.txt", "setup.py"}
        ).lower()
        if "fastapi" in python_text:
            add_unique(frameworks, "FastAPI")
        if "django" in python_text:
            add_unique(frameworks, "Django")
        if "flask" in python_text:
            add_unique(frameworks, "Flask")

    if java_markers:
        java_text = "\n".join(
            read_text(path)
            for path in iter_repo_files(context)
            if path.name.lower() in {"pom.xml", "build.gradle", "build.gradle.kts"}
        ).lower()
        if "spring" in java_text:
            add_unique(frameworks, "Spring")

    if dotnet_markers:
        add_unique(langs, ".NET")

    return {"languages": langs, "package_managers": package_managers, "frameworks": frameworks}


def repo_profile(source_roots: Sequence[str], modules: Sequence[str]) -> list[str]:
    profile: list[str] = []
    if len(source_roots) > 2:
        profile.append("- repository_shape: multi-root or workspace-style layout")
    elif len(modules) > 6:
        profile.append("- repository_shape: modular codebase with several named capabilities")
    elif len(source_roots) == 0:
        profile.append("- repository_shape: source roots not obvious; layout config or human review recommended")
    else:
        profile.append("- repository_shape: compact or moderately layered application layout")
    return profile


def find_entrypoints(root: Path, context: dict) -> list[str]:
    results: list[str] = []
    for path in iter_repo_files(context):
        rel = relative_path(root, path)
        if path.name in ENTRYPOINT_FILES:
            results.append(rel)
        if path.name == "package.json":
            try:
                package = json.loads(read_text(path) or "{}")
            except json.JSONDecodeError:
                continue
            scripts = package.get("scripts") or {}
            package_label = relative_path(root, path)
            for key in ("start", "dev", "build", "test"):
                if key in scripts:
                    results.append(f"{package_label} script `{key}`")
    return list(dict.fromkeys(results))[:16]


def find_keyword_paths(root: Path, keywords: Sequence[str], context: dict, limit: int = 20) -> list[str]:
    found: list[str] = []
    for path in iter_repo_files(context):
        if not is_text_evidence_file(path):
            continue
        lowered = relative_path(root, path).lower()
        if any(keyword in lowered for keyword in keywords):
            found.append(relative_path(root, path))
            if len(found) >= limit:
                break
    return found


def largest_files(root: Path, context: dict, limit: int = 10) -> list[str]:
    scored = []
    for path in iter_repo_files(context):
        if not is_text_evidence_file(path):
            continue
        scored.append((line_count(path), path))
    scored.sort(reverse=True, key=lambda item: item[0])
    return [f"{relative_path(root, path)} ({count} lines)" for count, path in scored[:limit] if count > 0]


def find_design_signal_paths(root: Path, context: dict, limit: int = 12, module: str | None = None) -> list[str]:
    if not context["include_design_sources"]:
        return []

    target = module.lower() if module else ""
    found: list[str] = []
    for path in iter_design_files(context):
        rel = relative_path(root, path)
        lowered = rel.lower()
        if target and target not in lowered and target.replace("-", " ") not in lowered:
            continue
        found.append(rel)
        if len(found) >= limit:
            break
    return found


def module_paths(root: Path, module: str, context: dict) -> tuple[list[str], list[Path]]:
    declared = context["module_map"].get(module, [])
    if declared:
        return declared, resolve_existing_paths(root, declared)

    detected = detect_modules_from_roots(root, context["source_root_paths"]).get(module, [])
    return detected, resolve_existing_paths(root, detected)


def summarize_module(root: Path, module: str, context: dict, all_modules: Sequence[str]) -> list[str]:
    declared_paths, existing_paths = module_paths(root, module, context)
    if not declared_paths:
        return render_evidence_sections(
            [],
            ["- status: module path not detected from layout config or source-root heuristics"],
            ["- evidence: declare this module in `ai-context/repo-layout.json` if it is a real capability"],
        )

    files = [path for path in walk_declared_paths(root, declared_paths, context["ignore_paths"]) if is_text_evidence_file(path)]
    rel_paths = [relative_path(root, path) for path in files]
    key_files = sorted(files, key=line_count, reverse=True)[:5]
    key_entries = [relative_path(root, path) for path in key_files if line_count(path) > 0]
    seams = [path for path in rel_paths if any(keyword in path.lower() for keyword in SEAM_KEYWORDS)][:10]
    interfaces = [path for path in rel_paths if any(keyword in path.lower() for keyword in INTERFACE_KEYWORDS)][:10]
    tests = [path for path in rel_paths if "test" in path.lower() or "spec" in path.lower()][:10]
    design_hits = find_design_signal_paths(root, context, limit=8, module=module)

    import_hits: Counter[str] = Counter()
    patterns = [normalize_module(candidate).replace("-", "/") for candidate in all_modules if normalize_module(candidate) != normalize_module(module)]
    for path in files[:80]:
        text = read_text(path).lower()
        for candidate in patterns:
            if candidate and candidate in text:
                import_hits[candidate.replace("/", "-")] += 1

    high_confidence = [
        f"- declared_paths: {', '.join(declared_paths)}",
        f"- existing_paths: {', '.join(relative_path(root, path) for path in existing_paths) if existing_paths else 'none detected'}",
        f"- file_count: {len(files)}",
        f"- key_files: {', '.join(key_entries) if key_entries else 'none detected'}",
        f"- tests: {', '.join(tests) if tests else 'none detected'}",
    ]
    heuristic = [
        f"- interface_signals: {', '.join(interfaces) if interfaces else 'none detected'}",
        f"- seam_signals: {', '.join(seams) if seams else 'none detected'}",
        f"- design_signal_paths: {', '.join(design_hits) if design_hits else 'none detected'}",
    ]
    if import_hits:
        top_deps = ", ".join(f"{name} ({count})" for name, count in import_hits.most_common(5))
        heuristic.append(f"- dependency_clues: {top_deps}")
    else:
        heuristic.append("- dependency_clues: no strong cross-module import pattern detected")
    review_needed = [
        "- confirm the module's real business purpose and stable boundary before turning these clues into architecture decisions",
        "- if this module spans multiple paths, verify the aggregation still matches current repository reality",
    ]
    return render_evidence_sections(high_confidence, heuristic, review_needed)


def ensure_marked_file(path: Path, title: str, human_note: str) -> None:
    if path.exists() and AUTO_BEGIN in read_text(path):
        return
    content = "\n".join(
        [
            f"# {title}",
            "",
            "## Auto-Synced",
            "",
            AUTO_BEGIN,
            "- not yet synced",
            AUTO_END,
            "",
            "## Human Notes",
            "",
            human_note,
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def replace_auto_section(path: Path, title: str, auto_lines: Sequence[str], human_note: str) -> None:
    ensure_marked_file(path, title, human_note)
    text = read_text(path)
    rendered = "\n".join(auto_lines).rstrip()
    pattern = re.compile(re.escape(AUTO_BEGIN) + r".*?" + re.escape(AUTO_END), re.S)
    replacement = f"{AUTO_BEGIN}\n{rendered}\n{AUTO_END}"
    updated = pattern.sub(lambda _: replacement, text, count=1)
    path.write_text(updated, encoding="utf-8")


def doc_lines_for_project(root: Path, mode: str, targets: Sequence[str], context: dict) -> list[str]:
    stack = detect_stack(root, context)
    tests = find_tests(root, context)
    entrypoints = find_entrypoints(root, context)
    modules = sorted(context["module_map"].keys())
    design_signals = find_design_signal_paths(root, context, limit=10)
    layout = context["layout"]

    high_confidence = [
        f"- synced_at: {datetime.now(timezone.utc).isoformat()}",
        f"- sync_mode: {mode}",
        f"- sync_layer: {context['resolved_layer']}",
        f"- repo_root: {root}",
        f"- layout_config: {layout['path'] if layout['exists'] else 'not found'}",
        f"- source_roots: {', '.join(context['source_roots']) if context['source_roots'] else 'none detected'}",
        f"- design_sources: {', '.join(context['design_sources']) if context['design_sources'] else 'none detected'}",
        f"- repo_scan_paths: {', '.join(context['repo_scan_paths']) if context['repo_scan_paths'] else 'none detected'}",
        f"- test_locations: {', '.join(tests) if tests else 'none detected'}",
        f"- entrypoints: {', '.join(entrypoints) if entrypoints else 'none detected'}",
    ]
    heuristic = [
        f"- languages: {', '.join(stack['languages']) if stack['languages'] else 'not confidently detected'}",
        f"- frameworks: {', '.join(stack['frameworks']) if stack['frameworks'] else 'not confidently detected'}",
        f"- package_managers: {', '.join(stack['package_managers']) if stack['package_managers'] else 'not confidently detected'}",
        f"- module_inventory: {', '.join(modules) if modules else 'none detected'}",
        f"- design_signal_paths: {', '.join(design_signals) if design_signals else 'none detected'}",
    ]
    heuristic.extend(repo_profile(context["source_roots"], modules))
    if mode == "local":
        heuristic.append(f"- local_targets: {', '.join(targets) if targets else 'none provided'}")

    review_needed = [
        "- confirm business capability boundaries before treating directory layout or layout config as the final module map",
        "- reconcile implementation evidence with proposal or design sources when they disagree",
    ]
    if layout["exists"] and not layout["valid"]:
        review_needed.append(f"- fix `{layout['path']}` before relying on declared layout: {layout['error']}")
    return render_evidence_sections(high_confidence, heuristic, review_needed)


def doc_lines_for_architecture(root: Path, context: dict) -> list[str]:
    modules = sorted(context["module_map"].keys())
    seams = find_keyword_paths(root, SEAM_KEYWORDS, context)
    design_signals = find_design_signal_paths(root, context, limit=10)
    high_confidence = [
        f"- module_map: {', '.join(modules) if modules else 'none detected'}",
        f"- source_roots: {', '.join(context['source_roots']) if context['source_roots'] else 'none detected'}",
    ]
    heuristic = [
        f"- extension_seam_signals: {', '.join(seams) if seams else 'none detected'}",
        f"- design_boundary_signals: {', '.join(design_signals) if design_signals else 'none detected'}",
        "- dependency_direction: infer from module docs, imports, and runtime wiring before treating as final truth",
    ]
    review_needed = [
        "- confirm which boundaries are intentionally stable versus just historical folder placement",
        "- verify declared module mappings still reflect the current codebase",
    ]
    return render_evidence_sections(high_confidence, heuristic, review_needed)


def doc_lines_for_interfaces(root: Path, context: dict) -> list[str]:
    interface_paths = find_keyword_paths(root, INTERFACE_KEYWORDS, context)
    design_signals = find_design_signal_paths(root, context, limit=8)
    high_confidence = [
        f"- design_sources: {', '.join(context['design_sources']) if context['design_sources'] else 'none detected'}",
    ]
    heuristic = [
        f"- interface_signals: {', '.join(interface_paths) if interface_paths else 'none detected'}",
        f"- interface_design_signals: {', '.join(design_signals) if design_signals else 'none detected'}",
    ]
    review_needed = [
        "- review public API, message, and integration boundaries manually where compatibility is sensitive",
    ]
    return render_evidence_sections(high_confidence, heuristic, review_needed)


def doc_lines_for_runtime(root: Path, context: dict) -> list[str]:
    runtime_paths = find_keyword_paths(root, RUNTIME_KEYWORDS, context)
    entrypoints = find_entrypoints(root, context)
    design_signals = find_design_signal_paths(root, context, limit=8)
    high_confidence = [
        f"- startup_or_entry_signals: {', '.join(entrypoints) if entrypoints else 'none detected'}",
    ]
    heuristic = [
        f"- runtime_signals: {', '.join(runtime_paths) if runtime_paths else 'none detected'}",
        f"- runtime_design_signals: {', '.join(design_signals) if design_signals else 'none detected'}",
    ]
    review_needed = [
        "- confirm retries, jobs, scheduler behavior, and observability paths manually when they matter",
    ]
    return render_evidence_sections(high_confidence, heuristic, review_needed)


def doc_lines_for_hotspots(root: Path, context: dict) -> list[str]:
    large = largest_files(root, context)
    suspicious = find_keyword_paths(root, ("legacy", "migration", "shared", "core"), context)
    high_confidence = [
        f"- large_files: {', '.join(large) if large else 'none detected'}",
    ]
    heuristic = [
        f"- hotspot_path_signals: {', '.join(suspicious) if suspicious else 'none detected'}",
    ]
    review_needed = [
        "- large or cross-cutting files deserve human review before major structural change",
    ]
    return render_evidence_sections(high_confidence, heuristic, review_needed)


def doc_lines_for_decisions(root: Path, context: dict) -> list[str]:
    seams = find_keyword_paths(root, SEAM_KEYWORDS, context)
    design_signals = find_design_signal_paths(root, context, limit=10)
    high_confidence = [
        f"- layout_config: {context['layout']['path'] if context['layout']['exists'] else 'not found'}",
    ]
    heuristic = [
        "- inferred_decisions: generated from naming, layout config, and structure only; confirm important ones manually",
        f"- seam_signals: {', '.join(seams[:12]) if seams else 'none detected'}",
        f"- decision_design_signals: {', '.join(design_signals) if design_signals else 'none detected'}",
    ]
    review_needed = [
        "- use alongside $design-pattern-engineering for real pattern judgment",
    ]
    return render_evidence_sections(high_confidence, heuristic, review_needed)


def doc_lines_for_sync_status(mode: str, targets: Sequence[str], updated_docs: Sequence[str], updated_modules: Sequence[str], context: dict) -> list[str]:
    layout = context["layout"]
    high_confidence = [
        f"- last_sync_at: {datetime.now(timezone.utc).isoformat()}",
        f"- last_sync_mode: {mode}",
        f"- last_sync_layer: {context['resolved_layer']}",
        f"- targets: {', '.join(targets) if targets else 'all detected modules'}",
        f"- updated_docs: {', '.join(updated_docs)}",
        f"- updated_modules: {', '.join(updated_modules) if updated_modules else 'none'}",
        f"- layout_config: {layout['path'] if layout['exists'] else 'not found'}",
        f"- repo_files_scanned: {len(context['repo_files'])}",
        f"- design_files_scanned: {len(context['design_files'])}",
        f"- repo_scan_paths: {', '.join(context['repo_scan_paths']) if context['repo_scan_paths'] else 'none detected'}",
        f"- evidence_sources: code, config, tests, layout config, and {'design sources' if context['include_design_sources'] else 'code-only repository evidence'}",
    ]
    heuristic = [
        "- confidence_model: trust direct file and config facts first, declared layout second, and inferred boundaries only after human review",
        "- precedence_rule: cli overrides beat layout config, and layout config beats heuristic discovery",
        "- freshness_rule: treat this record as stale after meaningful structural, interface, workflow, or runtime changes",
    ]
    review_needed = [
        "- review generated sections before treating them as perfect truth",
        "- if current code changed after this sync, refresh `ai-context/` before making large design decisions",
    ]
    if layout["exists"] and not layout["valid"]:
        review_needed.append(f"- fix `{layout['path']}` before relying on declared source roots or modules: {layout['error']}")
    return render_evidence_sections(high_confidence, heuristic, review_needed)


def sync_general_docs(root: Path, mode: str, targets: Sequence[str], context: dict) -> list[str]:
    docs = {
        "project.md": ("Project Design Record", doc_lines_for_project(root, mode, targets, context), "- Capture project intent, long-lived design tradeoffs, and context a future engineer should know."),
        "architecture.md": ("Architecture", doc_lines_for_architecture(root, context), "- Record why boundaries exist, which dependency directions matter, and which seams are intentionally stable."),
        "interfaces.md": ("Interfaces", doc_lines_for_interfaces(root, context), "- Record compatibility-sensitive contracts, API guarantees, and integration assumptions."),
        "runtime.md": ("Runtime", doc_lines_for_runtime(root, context), "- Record runtime behavior that matters to future changes: jobs, retries, workers, schedulers, and observability expectations."),
        "hotspots.md": ("Hotspots", doc_lines_for_hotspots(root, context), "- Record why these areas are fragile, which refactors are risky, and what constraints future work should respect."),
        "decisions.md": ("Decisions", doc_lines_for_decisions(root, context), "- Record intentional design decisions, tradeoffs, and unresolved tensions."),
    }
    updated: list[str] = []
    ai_context = root / "ai-context"
    for name, (title, lines, note) in docs.items():
        replace_auto_section(ai_context / name, title, lines, note)
        updated.append(f"ai-context/{name}")
    return updated


def sync_modules(root: Path, mode: str, targets: Sequence[str], context: dict) -> list[str]:
    ai_modules = root / "ai-context" / "modules"
    ai_modules.mkdir(parents=True, exist_ok=True)
    detected = sorted(context["module_map"].keys())
    if mode == "full":
        target_modules = detected
    else:
        requested = [normalize_module(name) for name in targets if normalize_module(name)]
        target_modules = requested or detected
    target_modules = list(dict.fromkeys([name for name in target_modules if name]))
    updated: list[str] = []
    for module in target_modules:
        title = module.replace("-", " ").title()
        note = "- Record the module's business purpose, stable boundaries, tradeoffs, and design debt worth tracking."
        replace_auto_section(ai_modules / f"{module}.md", title, summarize_module(root, module, context, detected), note)
        updated.append(f"ai-context/modules/{module}.md")
    return updated


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    ai_context = root / "ai-context"
    if not ai_context.exists():
        raise SystemExit("ai-context does not exist. Run $project-design-init first.")

    resolved_layer = resolve_sync_layer(root, args.layer, args.mode, args.targets)
    context = build_layout_context(root, args, resolved_layer)
    general = sync_general_docs(root, args.mode, args.targets, context) if resolved_layer in {"architecture", "all"} else []
    modules = sync_modules(root, args.mode, args.targets, context) if resolved_layer in {"detail", "all"} else []
    replace_auto_section(
        ai_context / "sync-status.md",
        "Sync Status",
        doc_lines_for_sync_status(args.mode, args.targets, general, modules, context),
        "- Record known drift, review outcomes, and whether the generated view is trustworthy enough for downstream skills.",
    )

    print(f"Synced ai-context under: {root}")
    print(f"Mode: {args.mode}")
    print(f"Resolved layer: {resolved_layer}")
    print(f"Layout config: {context['layout']['path'] if context['layout']['exists'] else 'not found'}")
    print(f"Design-source scan: {'enabled' if context['include_design_sources'] else 'disabled'}")
    print(f"Repo files scanned: {len(context['repo_files'])}")
    print(f"Design files scanned: {len(context['design_files'])}")
    print(f"Scan scope: {', '.join(context['repo_scan_paths']) if context['repo_scan_paths'] else 'none detected'}")
    print("Resolved source roots:")
    for item in context["source_roots"]:
        print(f"  - {item}")
    print("Updated docs:")
    for item in general:
        print(f"  - {item}")
    print("Updated modules:")
    for item in modules:
        print(f"  - {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
