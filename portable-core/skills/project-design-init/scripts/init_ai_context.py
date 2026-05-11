from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List

COMMON_SOURCE_ROOTS = (
    "src",
    "app",
    "apps",
    "packages",
    "services",
    "modules",
    "backend",
    "frontend",
    "server",
    "client",
    "lib",
)

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

SKIP_MODULE_NAMES = {
    "assets",
    "common",
    "components",
    "config",
    "core",
    "fixtures",
    "generated",
    "hooks",
    "i18n",
    "images",
    "lib",
    "locales",
    "migrations",
    "public",
    "shared",
    "styles",
    "test",
    "tests",
    "types",
    "utils",
}

TEXT_EVIDENCE_SUFFIXES = {
    ".md",
    ".mdx",
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".kt",
    ".go",
    ".rs",
    ".cs",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".xml",
    ".sql",
    ".proto",
    ".graphql",
    ".gql",
    ".sh",
    ".ps1",
    ".txt",
    ".rst",
}
TEXT_EVIDENCE_FILENAMES = {"dockerfile", "makefile", "procfile"}

GENERAL_DOCS = (
    "project.md",
    "architecture.md",
    "interfaces.md",
    "runtime.md",
    "hotspots.md",
    "decisions.md",
    "sync-status.md",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize ai-context design docs.")
    parser.add_argument("--root", default=".", help="Project root to initialize")
    parser.add_argument("--force", action="store_true", help="Overwrite existing generated files")
    parser.add_argument("--modules", nargs="*", default=[], help="Explicit module names to seed")
    parser.add_argument("--source-roots", nargs="*", default=[], help="Explicit repo-relative source roots")
    parser.add_argument("--design-sources", nargs="*", default=[], help="Explicit repo-relative design sources")
    parser.add_argument("--ignore-paths", nargs="*", default=[], help="Explicit repo-relative paths to ignore")
    parser.add_argument(
        "--module-path",
        action="append",
        default=[],
        help="Declare module mapping as module=path1,path2 using repo-relative paths",
    )
    return parser.parse_args()


def script_dir() -> Path:
    return Path(__file__).resolve().parent


def template_dir() -> Path:
    return script_dir().parent / "assets" / "templates" / "ai-context"


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


def detect_source_roots(root: Path) -> List[Path]:
    found: list[Path] = []
    for name in COMMON_SOURCE_ROOTS:
        candidate = root / name
        if candidate.is_dir():
            found.append(candidate)

    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name.startswith(".") or child.name in DEFAULT_IGNORE_PATHS:
            continue
        if looks_like_app_root(child):
            found.append(child)

    if not found and looks_like_app_root(root):
        found.append(root)

    unique: list[Path] = []
    seen: set[Path] = set()
    for path in found:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(path)
    return unique


def detect_design_sources(root: Path, source_roots: Iterable[Path]) -> list[str]:
    detected: list[str] = []

    def maybe_add(path: Path) -> None:
        rel = relative_path(root, path)
        if rel not in detected:
            detected.append(rel)

    def looks_like_design_source(path: Path) -> bool:
        lowered = path.name.lower()
        return any(hint in lowered for hint in DESIGN_SOURCE_HINTS)

    for child in sorted(root.iterdir()):
        if child.is_dir() and not child.name.startswith(".") and looks_like_design_source(child):
            maybe_add(child)

    for source_root in source_roots:
        if not source_root.exists() or not source_root.is_dir():
            continue
        for child in sorted(source_root.iterdir()):
            if child.is_dir() and looks_like_design_source(child):
                maybe_add(child)

    return detected


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


def should_treat_source_root_as_module(root: Path, source_root: Path) -> bool:
    return source_root != root and source_root.parent == root and looks_like_app_root(source_root)


def detect_modules(root: Path, source_roots: Iterable[Path]) -> dict[str, list[str]]:
    modules: dict[str, list[str]] = {}
    for source_root in source_roots:
        if not source_root.exists() or not source_root.is_dir():
            continue
        if should_treat_source_root_as_module(root, source_root):
            module_name = normalize_module_name(source_root.name)
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
            module_name = normalize_module_name(child.name)
            modules.setdefault(module_name, [])
            modules[module_name].append(relative_path(root, child))

    normalized: dict[str, list[str]] = {}
    for name, paths in modules.items():
        normalized[name] = dedupe(paths)
    return normalized


def parse_module_path_specs(root: Path, values: Iterable[str]) -> dict[str, list[str]]:
    parsed: dict[str, list[str]] = {}
    for value in values:
        raw = str(value).strip()
        if "=" not in raw:
            continue
        name, raw_paths = raw.split("=", 1)
        module_name = normalize_module_name(name)
        paths = [to_repo_relative(root, part) for part in expand_cli_values([raw_paths])]
        if not module_name or not paths:
            continue
        parsed.setdefault(module_name, [])
        parsed[module_name].extend(paths)

    normalized: dict[str, list[str]] = {}
    for name, paths in parsed.items():
        normalized[name] = dedupe(paths)
    return normalized


def merge_module_maps(*maps: dict[str, list[str]]) -> dict[str, list[str]]:
    merged: dict[str, list[str]] = {}
    for mapping in maps:
        for name, paths in mapping.items():
            merged.setdefault(name, [])
            merged[name].extend(paths)
    return {name: dedupe(paths) for name, paths in merged.items()}


def read_template(name: str) -> str:
    return (template_dir() / name).read_text(encoding="utf-8")


def ensure_file(path: Path, content: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def normalize_module_name(name: str) -> str:
    return name.strip().replace(" ", "-").replace("_", "-")


def build_sync_status_stub(root: Path, source_roots: list[str], design_sources: list[str]) -> str:
    timestamp = datetime.now(timezone.utc).isoformat()
    template = read_template("sync-status.md")
    body = [
        f"- initialized_at: {timestamp}",
        "- last_sync_at: not yet synced",
        "- last_sync_mode: init-only",
        f"- detected_source_roots: {', '.join(source_roots) if source_roots else 'none detected'}",
        f"- detected_design_sources: {', '.join(design_sources) if design_sources else 'none detected'}",
        "- layout_config: ai-context/repo-layout.json",
        "- notes: run $project-design-sync to populate the generated sections",
    ]
    return template.replace("{{AUTO_SYNC_CONTENT}}", "\n".join(body))


def build_repo_layout(
    source_roots: list[str],
    design_sources: list[str],
    ignore_paths: list[str],
    modules: dict[str, list[str]],
) -> str:
    payload = {
        "version": 1,
        "source_roots": source_roots,
        "design_sources": design_sources,
        "ignore_paths": ignore_paths,
        "modules": {name: {"paths": paths} for name, paths in modules.items()},
    }
    return json.dumps(payload, indent=2, ensure_ascii=True) + "\n"


def create_general_docs(root: Path, force: bool, source_roots: list[str], design_sources: list[str]) -> tuple[list[str], list[str]]:
    created: list[str] = []
    skipped: list[str] = []
    ai_context = root / "ai-context"
    for name in GENERAL_DOCS:
        content = build_sync_status_stub(root, source_roots, design_sources) if name == "sync-status.md" else read_template(name)
        changed = ensure_file(ai_context / name, content, force)
        (created if changed else skipped).append(f"ai-context/{name}")
    return created, skipped


def create_layout_config(root: Path, force: bool, source_roots: list[str], design_sources: list[str], ignore_paths: list[str], modules: dict[str, list[str]]) -> tuple[list[str], list[str]]:
    path = root / "ai-context" / "repo-layout.json"
    changed = ensure_file(path, build_repo_layout(source_roots, design_sources, ignore_paths, modules), force)
    target = "ai-context/repo-layout.json"
    return ([target], []) if changed else ([], [target])


def create_module_docs(root: Path, modules: Iterable[str], force: bool) -> tuple[list[str], list[str]]:
    created: list[str] = []
    skipped: list[str] = []
    template = read_template("module-template.md")
    modules_dir = root / "ai-context" / "modules"
    modules_dir.mkdir(parents=True, exist_ok=True)
    for raw_name in modules:
        module_name = normalize_module_name(raw_name)
        if not module_name:
            continue
        title_name = module_name.replace("-", " ")
        content = template.replace("{{MODULE_NAME}}", title_name.title())
        path = modules_dir / f"{module_name}.md"
        changed = ensure_file(path, content, force)
        rel = f"ai-context/modules/{module_name}.md"
        (created if changed else skipped).append(rel)
    return created, skipped


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    if not root.exists():
        raise SystemExit(f"Root does not exist: {root}")

    explicit_source_roots = [to_repo_relative(root, value) for value in expand_cli_values(args.source_roots)]
    explicit_design_sources = [to_repo_relative(root, value) for value in expand_cli_values(args.design_sources)]
    explicit_ignore_paths = [to_repo_relative(root, value) for value in expand_cli_values(args.ignore_paths)]

    detected_source_roots = [relative_path(root, path) for path in detect_source_roots(root)]
    source_roots = dedupe(explicit_source_roots or detected_source_roots)

    resolved_source_roots = [root if rel == "." else root / rel for rel in source_roots]
    detected_design_sources = detect_design_sources(root, resolved_source_roots)
    design_sources = dedupe(explicit_design_sources or detected_design_sources)
    ignore_paths = dedupe(list(DEFAULT_IGNORE_PATHS) + explicit_ignore_paths)

    detected_modules = detect_modules(root, resolved_source_roots)
    requested_modules = {normalize_module_name(name): [] for name in expand_cli_values(args.modules)}
    explicit_module_paths = parse_module_path_specs(root, args.module_path)
    combined_modules = merge_module_maps(detected_modules, requested_modules, explicit_module_paths)

    created_general, skipped_general = create_general_docs(root, args.force, source_roots, design_sources)
    created_layout, skipped_layout = create_layout_config(root, args.force, source_roots, design_sources, ignore_paths, combined_modules)
    created_modules, skipped_modules = create_module_docs(root, combined_modules.keys(), args.force)

    print(f"Initialized ai-context under: {root}")
    print("Created files:")
    for item in created_general + created_layout + created_modules:
        print(f"  - {item}")
    print("Skipped existing files:")
    for item in skipped_general + skipped_layout + skipped_modules:
        print(f"  - {item}")
    print("Declared source roots:")
    for item in source_roots:
        print(f"  - {item}")
    print("Declared design sources:")
    for item in design_sources:
        print(f"  - {item}")
    print("Seeded modules:")
    for item in combined_modules.keys():
        print(f"  - {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
