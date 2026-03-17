#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════╗
║   🐳 DevOps Containerization Agent v1.0     ║
║   Simple. Smart. No frameworks needed.      ║
╚══════════════════════════════════════════════╝

A practical CLI assistant that detects your tech stack,
asks only the questions it needs to, and generates
production-ready Docker files for your project.

Usage:
    python3 containerize.py [--dir /path/to/project]

Author : DevOps Assistant
Requires: Python 3.6+  (zero extra dependencies)
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path


# ─────────────────────────────────────────────
#  TERMINAL COLOURS  (no external libraries)
# ─────────────────────────────────────────────
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    CYAN   = "\033[96m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    BLUE   = "\033[94m"
    DIM    = "\033[2m"


def banner():
    print(f"""
{C.CYAN}{C.BOLD}
╔══════════════════════════════════════════════════╗
║   🐳  DevOps Containerization Agent  v1.0       ║
║   Detects · Asks · Generates · Done             ║
╚══════════════════════════════════════════════════╝
{C.RESET}""")


def info(msg):    print(f"  {C.CYAN}ℹ{C.RESET}  {msg}")
def success(msg): print(f"  {C.GREEN}✔{C.RESET}  {msg}")
def warn(msg):    print(f"  {C.YELLOW}⚠{C.RESET}  {msg}")
def error(msg):   print(f"  {C.RED}✖{C.RESET}  {msg}")
def section(msg): print(f"\n{C.BOLD}{C.BLUE}── {msg} {'─' * (45 - len(msg))}{C.RESET}")
def ask(prompt, default=""):
    """Prompt with an optional default shown in brackets."""
    d = f" [{C.DIM}{default}{C.RESET}]" if default else ""
    return input(f"  {C.BOLD}?{C.RESET}  {prompt}{d}: ").strip()


# ─────────────────────────────────────────────
#  STACK DETECTION
# ─────────────────────────────────────────────
STACK_RULES = [
    # (marker file/dir,  stack-key,  display name)
    ("package.json",    "node",     "Node.js"),
    ("requirements.txt","python",   "Python"),
    ("Pipfile",         "python",   "Python"),
    ("pyproject.toml",  "python",   "Python"),
    ("pom.xml",         "java",     "Java (Maven)"),
    ("build.gradle",    "java",     "Java (Gradle)"),
    ("go.mod",          "go",       "Go"),
    ("composer.json",   "php",      "PHP"),
    ("Gemfile",         "ruby",     "Ruby"),
    ("Cargo.toml",      "rust",     "Rust"),
    ("*.csproj",        "dotnet",   ".NET"),
    ("*.fsproj",        "dotnet",   ".NET"),
]

# Best-practice base images per stack
BASE_IMAGES = {
    "node":   {"build": "node:20-alpine",   "run": "node:20-alpine"},
    "python": {"build": "python:3.12-slim", "run": "python:3.12-slim"},
    "java":   {"build": "eclipse-temurin:21-jdk-alpine", "run": "eclipse-temurin:21-jre-alpine"},
    "go":     {"build": "golang:1.22-alpine", "run": "gcr.io/distroless/static-debian12"},
    "php":    {"build": "php:8.3-fpm-alpine","run": "php:8.3-fpm-alpine"},
    "ruby":   {"build": "ruby:3.3-alpine",   "run": "ruby:3.3-alpine"},
    "rust":   {"build": "rust:1.77-alpine",  "run": "debian:12-slim"},
    "dotnet": {"build": "mcr.microsoft.com/dotnet/sdk:8.0", "run": "mcr.microsoft.com/dotnet/aspnet:8.0"},
    "generic":{"build": "debian:12-slim",    "run": "debian:12-slim"},
}

DEFAULT_PORTS = {
    "node": "3000", "python": "5000", "java": "8080",
    "go": "8080", "php": "80", "ruby": "3000",
    "rust": "8080", "dotnet": "8080", "generic": "8080",
}

DEFAULT_START = {
    "node":    "node server.js",
    "python":  "python app.py",
    "java":    "java -jar app.jar",
    "go":      "./app",
    "php":     "php-fpm",
    "ruby":    "ruby app.rb",
    "rust":    "./app",
    "dotnet":  "dotnet app.dll",
    "generic": "./start.sh",
}

DEFAULT_BUILD = {
    "node":   "npm install && npm run build",
    "python": "pip install -r requirements.txt",
    "java":   "mvn clean package -DskipTests",
    "go":     "go build -o app .",
    "php":    "composer install --no-dev",
    "ruby":   "bundle install",
    "rust":   "cargo build --release",
    "dotnet": "dotnet publish -c Release -o /app/publish",
}


def detect_stack(project_dir: Path) -> dict:
    """
    Scan the project directory and return a dict with:
      stack, display_name, version_hint, build_cmd, start_cmd, port
    """
    detected = {"stack": "generic", "display": "Unknown", "version": None,
                 "build_cmd": "", "start_cmd": "", "port": ""}

    for marker, stack, display in STACK_RULES:
        if "*" in marker:
            # glob match (e.g. *.csproj)
            ext = marker.replace("*", "")
            matches = list(project_dir.glob(f"*{ext}"))
            found = bool(matches)
        else:
            found = (project_dir / marker).exists()

        if found:
            detected["stack"] = stack
            detected["display"] = display
            break

    s = detected["stack"]
    detected["port"]      = DEFAULT_PORTS.get(s, "8080")
    detected["start_cmd"] = DEFAULT_START.get(s, "")
    detected["build_cmd"] = DEFAULT_BUILD.get(s, "")

    # ── Extra hints from files ──────────────────────────
    pkg = project_dir / "package.json"
    if s == "node" and pkg.exists():
        try:
            data = json.loads(pkg.read_text())
            scripts = data.get("scripts", {})
            if "start" in scripts:
                detected["start_cmd"] = "npm start"
            elif "serve" in scripts:
                detected["start_cmd"] = "npm run serve"
            engines = data.get("engines", {})
            if "node" in engines:
                ver = engines["node"].strip("^~>=< ")
                major = ver.split(".")[0]
                detected["version"] = major
        except Exception:
            pass

    req = project_dir / "requirements.txt"
    if s == "python" and req.exists():
        text = req.read_text().lower()
        if "flask" in text:
            detected["start_cmd"] = "flask run --host=0.0.0.0"
        elif "fastapi" in text or "uvicorn" in text:
            detected["start_cmd"] = "uvicorn main:app --host 0.0.0.0 --port 8000"
            detected["port"] = "8000"
        elif "django" in text:
            detected["start_cmd"] = "python manage.py runserver 0.0.0.0:8000"
            detected["port"] = "8000"
        elif "gunicorn" in text:
            detected["start_cmd"] = "gunicorn -b 0.0.0.0:5000 app:app"

    return detected


# ─────────────────────────────────────────────
#  USER INPUT COLLECTION
# ─────────────────────────────────────────────
def ask_user_inputs(detected: dict, project_dir: Path) -> dict:
    """
    Walk the user through config questions.
    Skip or pre-fill anything already detected.
    Returns a final config dict.
    """
    section("Project Configuration")

    cfg = {}

    # ── App name ──────────────────────────────
    default_name = project_dir.name.lower().replace(" ", "-")
    raw = ask("App name", default_name)
    cfg["app_name"] = raw or default_name

    # ── Stack override ────────────────────────
    info(f"Detected stack: {C.GREEN}{detected['display']}{C.RESET}")
    override = ask("Override stack? (node/python/java/go/php/ruby/rust/dotnet) or ENTER to keep", "")
    if override and override in BASE_IMAGES:
        detected["stack"]   = override
        detected["display"] = override.capitalize()
        detected["port"]      = DEFAULT_PORTS.get(override, "8080")
        detected["start_cmd"] = DEFAULT_START.get(override, "")
        detected["build_cmd"] = DEFAULT_BUILD.get(override, "")
    cfg["stack"]   = detected["stack"]
    cfg["display"] = detected["display"]

    # ── Port ─────────────────────────────────
    raw = ask(f"Container port", detected["port"])
    cfg["port"] = raw or detected["port"]

    # ── Start command ─────────────────────────
    raw = ask("Start command", detected["start_cmd"])
    cfg["start_cmd"] = raw or detected["start_cmd"]

    # ── Build command ─────────────────────────
    default_build = detected["build_cmd"]
    raw = ask("Build command (ENTER to skip)", default_build)
    cfg["build_cmd"] = raw  # could be empty – that's fine

    # ── Environment variables ──────────────────
    section("Environment Variables")
    info("Enter KEY=VALUE pairs one per line. Empty line to finish.")
    env_vars = {}
    while True:
        line = input("  >  ").strip()
        if not line:
            break
        if "=" in line:
            k, _, v = line.partition("=")
            env_vars[k.strip()] = v.strip()
        else:
            warn(f"Skipping '{line}' — must be KEY=VALUE format")
    cfg["env_vars"] = env_vars

    # ── docker-compose? ───────────────────────
    section("Optional Files")
    raw = ask("Generate docker-compose.yml? (Y/n)", "Y")
    cfg["gen_compose"] = raw.upper() != "N"

    raw = ask("Generate README.md? (Y/n)", "Y")
    cfg["gen_readme"] = raw.upper() != "N"

    # ── Non-root user ─────────────────────────
    raw = ask("Run as non-root user inside container? (Y/n)", "Y")
    cfg["non_root"] = raw.upper() != "N"

    return cfg


# ─────────────────────────────────────────────
#  FILE GENERATORS
# ─────────────────────────────────────────────
def generate_dockerfile(cfg: dict, project_dir: Path) -> str:
    """
    Generate a Dockerfile.
    Uses multi-stage build when a build command is provided.
    """
    s      = cfg["stack"]
    imgs   = BASE_IMAGES.get(s, BASE_IMAGES["generic"])
    build  = cfg["build_cmd"]
    start  = cfg["start_cmd"]
    port   = cfg["port"]
    multi  = bool(build) and s not in ("python", "php")  # multi-stage for compiled stacks

    lines = [
        "# ─────────────────────────────────────────────",
        f"#  Dockerfile – {cfg['app_name']}",
        f"#  Stack : {cfg['display']}",
        "# ─────────────────────────────────────────────",
        "",
    ]

    # ── Multi-stage (compiled stacks) ────────────────
    if multi:
        lines += [
            f"FROM {imgs['build']} AS builder",
            "WORKDIR /build",
            "",
        ]

        if s == "node":
            lines += [
                "# Install dependencies first (layer caching)",
                "COPY package*.json ./",
                f"RUN {build}",
                "COPY . .",
                "",
            ]
        elif s == "go":
            lines += [
                "COPY go.mod go.sum ./",
                "RUN go mod download",
                "COPY . .",
                f"RUN {build}",
                "",
            ]
        elif s == "java":
            lines += [
                "COPY pom.xml ./",
                "COPY src ./src",
                f"RUN {build}",
                "",
            ]
        elif s == "rust":
            lines += [
                "COPY Cargo.toml Cargo.lock ./",
                "COPY src ./src",
                f"RUN {build}",
                "",
            ]
        elif s == "dotnet":
            lines += [
                "COPY *.csproj ./",
                "RUN dotnet restore",
                "COPY . .",
                f"RUN {build}",
                "",
            ]
        else:
            lines += [
                "COPY . .",
                f"RUN {build}",
                "",
            ]

        lines += [
            f"# ── Runtime image (smaller) ─────────────",
            f"FROM {imgs['run']}",
            "WORKDIR /app",
            "",
        ]

        # Copy built artefacts
        if s == "node":
            lines += [
                "COPY --from=builder /build/node_modules ./node_modules",
                "COPY --from=builder /build/dist ./dist",
                "COPY --from=builder /build/package.json ./",
                "",
            ]
        elif s == "go":
            lines += ["COPY --from=builder /build/app ./app", ""]
        elif s == "java":
            lines += ["COPY --from=builder /build/target/*.jar app.jar", ""]
        elif s == "rust":
            lines += ["COPY --from=builder /build/target/release/app ./app", ""]
        elif s == "dotnet":
            lines += ["COPY --from=builder /app/publish .", ""]
        else:
            lines += ["COPY --from=builder /build /app", ""]

    # ── Single-stage (interpreted stacks) ────────────
    else:
        lines += [
            f"FROM {imgs['build']}",
            "WORKDIR /app",
            "",
        ]

        if s == "python":
            lines += [
                "# Install dependencies first (layer caching)",
                "COPY requirements*.txt ./",
                "RUN pip install --no-cache-dir -r requirements.txt",
                "",
                "COPY . .",
                "",
            ]
        elif s == "php":
            lines += [
                "COPY composer*.json ./",
                "RUN composer install --no-dev --optimize-autoloader",
                "",
                "COPY . .",
                "",
            ]
        elif s == "ruby":
            lines += [
                "COPY Gemfile* ./",
                "RUN bundle install --without development test",
                "",
                "COPY . .",
                "",
            ]
        else:
            if build:
                lines += [
                    "COPY . .",
                    f"RUN {build}",
                    "",
                ]
            else:
                lines += ["COPY . .", ""]

    # ── Non-root user ────────────────────────────────
    if cfg.get("non_root") and s not in ("dotnet",):
        lines += [
            "# Run as non-root for security",
            "RUN addgroup -S appgroup && adduser -S appuser -G appgroup",
            "USER appuser",
            "",
        ]

    # ── Environment variables ────────────────────────
    if cfg["env_vars"]:
        lines.append("# Environment variables")
        for k, v in cfg["env_vars"].items():
            lines.append(f"ENV {k}={v}")
        lines.append("")

    # ── Expose & CMD ─────────────────────────────────
    lines += [
        f"EXPOSE {port}",
        "",
        f'CMD {json.dumps(start.split())}',
    ]

    content = "\n".join(lines) + "\n"
    out = project_dir / "Dockerfile"
    out.write_text(content)
    return str(out)


def generate_dockerignore(cfg: dict, project_dir: Path) -> str:
    """Create a sensible .dockerignore for the detected stack."""
    s = cfg["stack"]

    common = [
        "# ── Common ──────────────────────────",
        ".git",
        ".gitignore",
        ".env",
        ".env.*",
        "*.md",
        "Dockerfile*",
        "docker-compose*.yml",
        ".dockerignore",
        ".DS_Store",
        "*.log",
        "logs/",
        "tmp/",
        "",
    ]

    extras = {
        "node":   ["node_modules/", "dist/", "build/", ".npm", "coverage/", "*.test.js"],
        "python": ["__pycache__/", "*.pyc", "*.pyo", ".venv/", "venv/", ".pytest_cache/", "*.egg-info/", "dist/", "build/"],
        "java":   ["target/", "*.class", "*.jar", ".mvn/", ".gradle/"],
        "go":     ["vendor/", "*.exe", "*.test"],
        "php":    ["vendor/", "*.cache", "storage/logs/"],
        "ruby":   [".bundle/", "vendor/bundle/", "coverage/"],
        "rust":   ["target/"],
        "dotnet": ["bin/", "obj/", "*.user"],
    }

    specific = extras.get(s, [])
    if specific:
        common += [f"# ── {cfg['display']} ──────────────────────────"] + specific

    out = project_dir / ".dockerignore"
    out.write_text("\n".join(common) + "\n")
    return str(out)


def generate_compose(cfg: dict, project_dir: Path) -> str:
    """Generate a docker-compose.yml."""
    app  = cfg["app_name"]
    port = cfg["port"]

    env_block = ""
    if cfg["env_vars"]:
        env_block = "    environment:\n"
        for k, v in cfg["env_vars"].items():
            env_block += f"      {k}: \"{v}\"\n"

    content = f"""\
# docker-compose.yml – {app}
# Generated by DevOps Containerization Agent

version: "3.9"

services:
  {app}:
    build:
      context: .
      dockerfile: Dockerfile
    image: {app}:latest
    container_name: {app}
    restart: unless-stopped
    ports:
      - "{port}:{port}"
{env_block}\
    # Uncomment to add a database service:
    # depends_on:
    #   - db

  # ── Example database (uncomment if needed) ──────────
  # db:
  #   image: postgres:16-alpine
  #   environment:
  #     POSTGRES_USER: user
  #     POSTGRES_PASSWORD: password
  #     POSTGRES_DB: {app}_db
  #   volumes:
  #     - db_data:/var/lib/postgresql/data

# volumes:
#   db_data:
"""
    out = project_dir / "docker-compose.yml"
    out.write_text(content)
    return str(out)


def generate_readme(cfg: dict, project_dir: Path) -> str:
    """Generate a Docker-focused README section."""
    app  = cfg["app_name"]
    port = cfg["port"]

    content = f"""\
# {app}

## 🐳 Docker Quick Start

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) ≥ 24
- [Docker Compose](https://docs.docker.com/compose/install/) ≥ 2 (optional)

### Build & Run

```bash
# Build the image
docker build -t {app} .

# Run the container
docker run -d --name {app} -p {port}:{port} {app}

# Check logs
docker logs -f {app}
```

### Using Docker Compose

```bash
# Start
docker compose up -d

# Stop
docker compose down

# Rebuild after code changes
docker compose up -d --build
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
{chr(10).join(f"| `{k}` | | `{v}` |" for k, v in cfg["env_vars"].items()) if cfg["env_vars"] else "| _(none configured)_ | | |"}

### Ports

| Container | Host |
|-----------|------|
| {port} | {port} |

---
_Generated by [DevOps Containerization Agent](https://github.com/your-repo)_
"""
    out = project_dir / "README.docker.md"
    out.write_text(content)
    return str(out)


# ─────────────────────────────────────────────
#  SUMMARY
# ─────────────────────────────────────────────
def print_summary(cfg: dict, files: list):
    section("Summary")
    print(f"""
  {C.BOLD}App name  :{C.RESET} {cfg['app_name']}
  {C.BOLD}Stack     :{C.RESET} {cfg['display']}
  {C.BOLD}Port      :{C.RESET} {cfg['port']}
  {C.BOLD}Start     :{C.RESET} {cfg['start_cmd']}
  {C.BOLD}Build     :{C.RESET} {cfg['build_cmd'] or '(none)'}
  {C.BOLD}Env vars  :{C.RESET} {len(cfg['env_vars'])} defined
""")
    section("Files Generated")
    for f in files:
        success(f)


# ─────────────────────────────────────────────
#  BONUS: BUILD & RUN
# ─────────────────────────────────────────────
def offer_build_run(cfg: dict, project_dir: Path):
    section("Build & Run (Bonus)")
    raw = ask("Build Docker image now? (y/N)", "N")
    if raw.upper() != "Y":
        return

    app  = cfg["app_name"]
    port = cfg["port"]

    info(f"Building image '{app}:latest' …")
    result = subprocess.run(
        ["docker", "build", "-t", f"{app}:latest", "."],
        cwd=project_dir
    )
    if result.returncode != 0:
        error("Docker build failed. Check the output above.")
        return
    success(f"Image '{app}:latest' built successfully!")

    raw = ask("Run the container now? (y/N)", "N")
    if raw.upper() != "Y":
        return

    # Stop any existing container with same name
    subprocess.run(["docker", "rm", "-f", app],
                   capture_output=True, cwd=project_dir)

    env_flags = []
    for k, v in cfg["env_vars"].items():
        env_flags += ["-e", f"{k}={v}"]

    cmd = ["docker", "run", "-d",
           "--name", app,
           "-p", f"{port}:{port}"] + env_flags + [f"{app}:latest"]

    info(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=project_dir)
    if result.returncode == 0:
        success(f"Container running → http://localhost:{port}")
        info(f"Logs: docker logs -f {app}")
    else:
        error("Container failed to start.")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="🐳 DevOps Containerization Agent — auto-detect & generate Docker files"
    )
    parser.add_argument(
        "--dir", "-d",
        default=".",
        help="Path to your project directory (default: current directory)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be generated without writing files"
    )
    args = parser.parse_args()

    banner()

    project_dir = Path(args.dir).resolve()
    if not project_dir.is_dir():
        error(f"Directory not found: {project_dir}")
        sys.exit(1)

    info(f"Scanning project: {C.BOLD}{project_dir}{C.RESET}")

    # 1. Detect stack
    detected = detect_stack(project_dir)
    success(f"Detected → {C.GREEN}{detected['display']}{C.RESET}")

    # 2. Collect user inputs
    cfg = ask_user_inputs(detected, project_dir)

    if args.dry_run:
        section("Dry Run — No files written")
        print(json.dumps(cfg, indent=2))
        return

    # 3. Generate files
    section("Generating Files")
    files = []

    info("Writing Dockerfile …")
    files.append(generate_dockerfile(cfg, project_dir))
    success("Dockerfile created")

    info("Writing .dockerignore …")
    files.append(generate_dockerignore(cfg, project_dir))
    success(".dockerignore created")

    if cfg["gen_compose"]:
        info("Writing docker-compose.yml …")
        files.append(generate_compose(cfg, project_dir))
        success("docker-compose.yml created")

    if cfg["gen_readme"]:
        info("Writing README.docker.md …")
        files.append(generate_readme(cfg, project_dir))
        success("README.docker.md created")

    # 4. Summary
    print_summary(cfg, files)

    # 5. Bonus: build & run
    offer_build_run(cfg, project_dir)

    section("All Done")
    print(f"""
  {C.GREEN}{C.BOLD}Your project is container-ready! 🎉{C.RESET}

  Next steps:
    {C.DIM}docker build -t {cfg['app_name']} .{C.RESET}
    {C.DIM}docker run -p {cfg['port']}:{cfg['port']} {cfg['app_name']}{C.RESET}

    — or —

    {C.DIM}docker compose up -d{C.RESET}
""")


if __name__ == "__main__":
    main()
