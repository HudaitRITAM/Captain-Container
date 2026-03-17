# 🐳 Captain Container

> Your personal DevOps assistant — drag and drop your project ZIP,
> get five production-ready Docker files in seconds.
> Runs 100% locally. No internet. No API key. No cloud.

---

## 📁 Your Folder

```
captain-container/
│
├── captain-container-app.html   ← The app (open in browser)
├── containerize.py              ← Terminal tool (optional, run with python3)
├── README.md                    ← This file
│
└── sample-output/               ← Reference examples only
    ├── Dockerfile
    ├── docker-compose.yml
    ├── .dockerignore
    └── README.docker.md
```

---

## ✅ Requirements

| What | Needed for | Check |
|------|-----------|-------|
| Chrome or Firefox | Desktop app | Already installed |
| Python 3.6+ | Terminal tool only | `python3 --version` |
| Docker | Building/running containers | `docker --version` |

---
---

# 🖥️ PART 1 — Desktop App (Drag & Drop)

## How to Open It

```bash
# Double-click in your file manager, OR:
xdg-open ~/Desktop/captain-container/captain-container-app.html
```

## How to Use It

### Step 1 — Zip your project
```bash
cd /path/to/your-project
zip -r my-project.zip .
```

### Step 2 — Drop the zip into the app
Open the HTML file in your browser and drag `my-project.zip` onto the drop area.

### Step 3 — Download your files
Five tabs appear. Download each file or click **Download All 5 Files as ZIP**.
Put all files into your project's root folder.

---

## Every Section of the App Explained

### 🔵 The Drop Zone
Drag your `.zip` here or click **Browse Files**. The border glows when a file is dragged over it.
Only `.zip` files are accepted.

### 🟦 Scanning Panel
A live log of exactly what the engine is doing — how many files it found,
which config files it read, whether it scanned your source code for port numbers,
and what it detected at each step.

### 🟩 Detected Stack Card
Shows everything the engine figured out:

| Field | What it shows |
|-------|--------------|
| Stack name | e.g. "Python · FastAPI" |
| Build image | The Docker image used during build stage |
| Runtime image | The lean final image your container actually runs |
| Port | The port your app listens on |
| Port Source | **Where the port came from** — `source code`, `Procfile`, `.env file`, or `default` |
| Pkg Manager | npm / yarn / pnpm / bun / pip / poetry / pipenv / uv / cargo / etc |
| Databases | Detected from your dependency files |
| Native Deps | System packages your code needs (libvips, imagemagick, etc) |
| Workers | Background job workers detected |
| Volumes | Writable paths detected (uploads/, storage/, etc) |

**Feature pills** on the card show best practices applied:
- `multi-stage` — two Docker stages so the final image is lean
- `non-root` — container doesn't run as root
- `healthcheck` — Docker polls your app every 30s
- `OCI labels` — standard image metadata
- `distroless` — no shell at all (Go and Rust only) — maximum security
- `port from src` — port was read from your actual code, not guessed
- `TypeScript` — compile step added
- `worker` — separate worker service in compose

### 🔶 Insights Panel (appears when there's something important)
Smart warnings and confirmations specific to your project:

| Color | Meaning |
|-------|---------|
| 🟢 Green (good) | Something was detected and handled correctly |
| 🔵 Blue (info) | A note about something to be aware of |
| 🟡 Yellow (warn) | Something needs your attention before deploying |
| 🔴 Red (crit) | Security issue — action required |

Examples of what it tells you:
- `✔ Port 8000 confirmed by reading your source code — not just a default guess`
- `✔ Start command taken from your Procfile`
- `⚠ Database detected but no DATABASE_URL found in .env.example`
- `⚠ Native module requires non-Alpine image — switched to bullseye-slim`
- `🚨 .env is NOT in .gitignore — your secrets may be committed to git!`
- `ℹ WebSockets detected — make sure your load balancer has upgrade headers`
- `ℹ Background worker detected — compose includes a separate worker service`

### 🗂️ The Five Output Tabs

**Tab 1: 🐳 Dockerfile**
The recipe for building your container. Includes:
multi-stage build, dependency layer caching, non-root user, OCI labels,
`STOPSIGNAL`, healthcheck, and smart start command.

**Tab 2: ⚙️ docker-compose.yml**
Start everything with `docker compose up -d`. Includes:
your app service, auto-wired database (PostgreSQL/MySQL/MongoDB),
Redis if detected, background worker service if detected,
healthchecks on all services, memory/CPU limits, restart policy,
volume mounts for persistent storage, and commented Nginx reverse proxy.

**Tab 3: 🚫 .dockerignore**
Keeps your image small and prevents secrets from leaking into it.
Customised per stack — excludes `node_modules/`, `__pycache__/`, `target/`, `.venv/`,
test files, CI configs, logs, OS files, and dev tool artifacts.

**Tab 4: 🔑 .env.example**
Pre-filled with every environment variable the engine detected from your project —
including database URLs (with the right format for your database), Redis URL,
JWT fields, app name/version, and any vars found in your existing `.env.example`.
Secret values are masked as `CHANGE_ME`.

**Tab 5: ⚡ Makefile**
Run common Docker operations with short commands:
`make build`, `make up`, `make down`, `make rebuild`, `make logs`, `make shell`, `make clean`.

---

## What the Intelligence Engine Does (v3)

This is completely local. It reads your files and makes smart decisions.

### It reads 40+ config files
`.nvmrc`, `.node-version`, `.tool-versions`, `.python-version`, `runtime.txt`,
`pyproject.toml`, `Pipfile`, `poetry.lock`, `go.sum`, `Cargo.lock`, `Gemfile.lock`,
`application.properties`, `deno.json`, `.env.example`, `Procfile`, `nginx.conf`,
`supervisord.conf`, `tsconfig.json`, `next.config.js`, `angular.json`, and more.

### It reads your actual source code
For these files it scans the content to find real port numbers:
`app.py`, `main.py`, `index.js`, `server.js`, `main.go`, `main.rs`, `app.rb`, `server.ts`, etc.

It looks for patterns like:
- `app.listen(3000)` — Node.js
- `uvicorn.run(app, port=8000)` — Python
- `http.ListenAndServe(":8080", ...)` — Go
- `.bind("0.0.0.0:3000")` — Rust/Actix

If it finds a port in your code, the card shows `port from src` and the insights panel confirms it.

### It detects native system dependencies
Some npm/pip packages need OS-level libraries to compile.
The engine knows about this and adds the right `apk add` or `apt-get install` lines:

| Package | System dep added |
|---------|-----------------|
| `sharp` (Node) | `vips-dev` |
| `canvas` (Node) | `cairo-dev`, `pango-dev` |
| `bcrypt` / `argon2` | `python3`, `make`, `g++` |
| `Pillow` / `PIL` (Python) | `libjpeg-dev`, `libpng-dev` |
| `lxml` (Python) | `libxml2-dev`, `libxslt-dev` |
| `psycopg2` (Python, non-binary) | `libpq-dev` |
| `puppeteer` | `chromium` + 6 deps |
| `nokogiri` (Ruby) | `libxml2-dev`, `libxslt-dev` |
| `ffmpeg` | `ffmpeg` |
| `imagemagick` | `imagemagick` |

### It switches base image when Alpine won't work
Some packages (`sharp`, `canvas`, `puppeteer`) don't compile on Alpine Linux.
The engine detects this and automatically switches from `node:20-alpine`
to `node:20-bullseye-slim`, then shows a warning in the insights panel.

### It parses your Procfile
If you have a `Procfile` (Heroku-style), it reads the `web:` line and uses
that as your start command. It reads the `worker:` line and adds a separate
worker service to `docker-compose.yml`. No guessing.

### It detects background workers
If it finds Celery (Python), Sidekiq (Ruby), Bull/BullMQ (Node), or
similar in your dependencies, it adds a separate worker service to
`docker-compose.yml` with the right command.

### It generates JVM flags for Java
Instead of generic `java -jar app.jar`, it generates:
```
java -Xms256m -Xmx512m -XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -jar app.jar
```
Container-aware memory settings that respect the memory limit you set.

### It generates `NODE_OPTIONS` for large Node apps
For frameworks like Next.js or Strapi that need more memory:
```
ENV NODE_OPTIONS="--max-old-space-size=768"
```
Set to 75% of the memory limit so Node doesn't OOM-kill itself.

### It uses distroless runtime images for Go and Rust
Go and Rust produce static binaries. The engine uses
`gcr.io/distroless/static-debian12` (Go) and `gcr.io/distroless/cc-debian12` (Rust)
as the runtime image. These have **no shell, no package manager, no OS tools** —
just your binary. Smallest possible attack surface.

### It detects volumes
If your project has `uploads/`, `storage/`, `logs/` directories, it adds
Docker named volumes in `docker-compose.yml` so those paths persist when the container restarts.

### It checks your `.gitignore` for secrets
If `.env` is not in your `.gitignore`, the insights panel shows a red critical warning.

### Frameworks detected per stack (50+)

| Stack | Frameworks |
|-------|-----------|
| Node.js | Next.js, Nuxt, Angular, React+Vite, Vue+Vite, SvelteKit, Astro, Remix, NestJS, Strapi, PayloadCMS, Express, Fastify, Koa, Hono, Hapi, Sails, Socket.IO |
| Python | FastAPI, Litestar, Sanic, aiohttp, Tornado, Django, Flask, Starlette, Pyramid, Bottle, Falcon |
| Java | Spring Boot, Quarkus, Micronaut, Helidon, Vert.x, Jakarta EE |
| Go | Gin, Fiber, Echo, Chi, Gorilla Mux, Beego, Buffalo, go-kit |
| PHP | Laravel, Symfony, Slim, CakePHP, Yii2, CodeIgniter, WordPress |
| Ruby | Rails, Sinatra, Hanami, Padrino, Roda, Grape |
| Rust | Actix-web, Axum, Rocket, Warp, Poem, Tide, ntex |

### Package managers detected

| Stack | Detected |
|-------|---------|
| Node.js | npm, yarn, pnpm, bun (from lockfiles) |
| Python | pip, poetry, pipenv, pdm, uv, hatch |
| Ruby | bundler |
| Rust | cargo |
| Java | maven, gradle |
| PHP | composer |

### Language version sources

| Stack | Where version is read from |
|-------|--------------------------|
| Node.js | `.nvmrc`, `.node-version`, `.tool-versions`, `package.json engines.node` |
| Python | `.python-version`, `runtime.txt`, `.tool-versions`, `pyproject.toml` |
| Ruby | `Gemfile` (`ruby "3.3"`), `.ruby-version` |
| Java | `pom.xml` (`<java.version>`), `build.gradle` (`sourceCompatibility`) |
| Go | `go.mod` (`go 1.22`) |
| .NET | `*.csproj` (`<TargetFramework>net8`) |

---

## Detected Stack → Generated Files

| Your project has... | Dockerfile type | Runtime image | Compose includes |
|--------------------|----------------|--------------|-----------------|
| `package.json` + Next.js | Multi-stage + build | `node:20-alpine` | app |
| `package.json` + React+Vite | Multi-stage + nginx | `nginx:1.27-alpine` | app |
| `requirements.txt` + FastAPI | Single-stage | `python:3.12-slim` | app + optional db |
| `pom.xml` + Spring Boot | Multi-stage | `eclipse-temurin:21-jre-alpine` | app + optional db |
| `go.mod` + Gin | Multi-stage | `gcr.io/distroless/static-debian12` | app |
| `Cargo.toml` + Axum | Multi-stage | `gcr.io/distroless/cc-debian12` | app |
| `Gemfile` + Rails + Sidekiq | Multi-stage | `ruby:3.3-alpine` | app + sidekiq + redis |
| Any + PostgreSQL dependency | Any | Any | app + postgres + volumes |
| Any + Redis dependency | Any | Any | app + redis |
| Any + Celery/Sidekiq/Bull | Any | Any | app + worker service |

---
---

# 💻 PART 2 — Terminal Tool

```bash
# Go into your project
cd /path/to/your-project

# Run
python3 ~/Desktop/captain-container/containerize.py

# Options
python3 ~/Desktop/captain-container/containerize.py --dir /other/project
python3 ~/Desktop/captain-container/containerize.py --dry-run

# Global shortcut
chmod +x ~/Desktop/captain-container/containerize.py
sudo ln -s ~/Desktop/captain-container/containerize.py /usr/local/bin/containerize
```

---
---

# 🐳 PART 3 — After the Files Are Generated

Put all 5 files into your project root, then:

```bash
# Copy .env.example to .env and fill in real values
cp .env.example .env
nano .env

# Start everything (builds automatically)
docker compose up -d

# Or use the generated Makefile
make up
make logs
make shell
make down
make rebuild
make clean
```

---
---

# 🚀 PART 4 — How to Upgrade in the Future

## File structure

```
captain-container-app.html
│
├── <style>     ← All visual design — colours, layout, animations
├── <body>      ← HTML structure — buttons, tabs, panels
└── <script>
    │
    ├── analyse()              ← Master intelligence function
    │   ├── Node.js block      ← All Node/framework/pkg detection
    │   ├── Python block       ← All Python/framework/pkg detection
    │   ├── Java block         ← Maven/Gradle/Spring/version detection
    │   ├── Go block           ← go.mod parsing, framework, distroless
    │   ├── ... (all stacks)
    │   ├── ENV VAR section    ← Reads .env files across all stacks
    │   ├── VOLUME section     ← Detects persistent paths
    │   └── INSIGHTS section   ← Smart warnings and tips
    │
    ├── scanPortFromSource()   ← Reads source code for port numbers
    ├── detectNodeNativeDeps() ← Maps npm packages to OS packages
    ├── mkDockerfile()         ← Generates Dockerfile
    ├── mkCompose()            ← Generates docker-compose.yml
    ├── mkIgnore()             ← Generates .dockerignore
    ├── mkEnvExample()         ← Generates .env.example
    └── mkMakefile()           ← Generates Makefile
```

## Common upgrades

### Add a new language
Find the large `if/else if` chain in `analyse()` and add a new block:
```javascript
else if (hf('mix.exs')) {
  R.stack='elixir'; R.display='Elixir'; R.icon='💜';
  R.port='4000'; R.pkgMgr='mix';
  R.buildImg='elixir:1.17-alpine'; R.baseImg='elixir:1.17-alpine';
  R.startCmd='mix phx.server'; R.buildCmd='mix do deps.get, compile';
  const mix=(C['mix.exs']||'').toLowerCase();
  if(has(mix,'phoenix')) R.framework='Phoenix';
}
```
Then add to `mkIgnore()` stacks object: `elixir: ['_build/','deps/','*.beam']`

### Add a new Node.js framework
Inside the Node.js block in `analyse()`, add to the framework chain:
```javascript
else if (deps['hono']) { R.framework='Hono'; R.port='3000'; R.startCmd=sc[R.pkgMgr]; }
```

### Add a native dep mapping
In `detectNodeNativeDeps()`:
```javascript
if (has(dStr,'wkhtmltopdf')) R.sysDeps.push('wkhtmltopdf','xvfb');
```

### Change port scanning patterns
In `scanPortFromSource()`, add a pattern to the right language's array:
```javascript
node: [
  ...existing patterns...
  /createApp\(\)\s*\.listen\(\s*(\d{3,5})/,  // custom pattern
],
```

### Add a new insight
At the bottom of `analyse()`, add to `R.insights`:
```javascript
if (R.framework === 'Django' && !has(allPy,'whitenoise'))
  R.insights.push({type:'warn', text:'Django detected without whitenoise — static files may not serve in production'});
```
Types: `good` (green ✔), `info` (blue ℹ), `warn` (yellow ⚠), `crit` (red 🚨)

### Change visual colours
Edit the `:root {}` block at the top of `<style>`:
```css
:root {
  --bg:     #05070a;   /* main background */
  --accent: #00d4aa;   /* primary teal accent */
  --accent2:#00a8ff;   /* blue accent */
  --green:  #44e580;   /* success green */
  --warm:   #ff9f43;   /* warning orange */
}
```

### Safe upgrade checklist
1. `cp captain-container-app.html captain-container-app.backup.html`
2. Make one change
3. Open in browser, press F12 → Console to check for errors
4. Test with a real zip
5. Repeat

---
---

# ❓ Troubleshooting

**Blank page / nothing loads**
Use Chrome or Firefox. Safari sometimes blocks local JS files.

**Dropped zip but nothing happened**
File must end in `.zip`. Zip it first: `zip -r project.zip .`

**Wrong stack detected**
The engine missed a marker file. Check your zip contains `package.json` / `requirements.txt` / `go.mod` etc. in the root level.

**Port is wrong**
The engine scans source files but may miss custom setups.
After downloading, manually edit `EXPOSE` and the port in `CMD` in the Dockerfile.

**Docker build fails with "file not found"**
Your project structure puts source in a subfolder. Edit the `COPY` lines in the Dockerfile to match.

**"docker: command not found"**
Install Docker: https://docs.docker.com/engine/install/ubuntu/

**Port already in use**
```bash
docker run -p 4001:3000 my-app   # use a different host port on the left
```

---

## 📌 Quick Reference

```bash
# ── Open the app ──────────────────────────────────
xdg-open ~/Desktop/captain-container/captain-container-app.html

# ── Zip your project ──────────────────────────────
cd /path/to/project && zip -r project.zip .

# ── After generating files ────────────────────────
cp .env.example .env && nano .env
make up              # or: docker compose up -d
make logs            # or: docker compose logs -f
make rebuild         # or: docker compose up -d --build
make shell           # or: docker compose exec app sh
make down            # or: docker compose down
make clean           # remove containers + images
```

---

## 🗂️ Folder Layout

```
captain-container/                ← Keep this safe
├── captain-container-app.html   ← Open in browser
├── containerize.py              ← Terminal tool
└── README.md

your-project/                    ← Your app code
├── Dockerfile                   ← Generated ✅
├── docker-compose.yml           ← Generated ✅
├── .dockerignore                ← Generated ✅
├── .env.example                 ← Generated ✅
├── Makefile                     ← Generated ✅
└── .env                         ← You create from .env.example
```

---

*Captain Container v3 · 100% local · Python 3 + HTML/JS · Zero installation*

---
---

# 🔬 PART 5 — Real-World Test & What Was Fixed (v4)

## The Test Project

A real CRA (Create React App) + Node.js server project was run through the agent.
The project had:
- `package.json` with `react-scripts`
- A custom `nest_portal_server/server.js` serving the built React app on port **5000**
- `REACT_APP_*` environment variables baked into the JS bundle at build time
- A Kubernetes deployment already in production
- Redis connected via k8s ConfigMap env var (`REDIS_URL`) — **not** as an npm package

## What v3 Generated (Wrong)

| Output | What it said | Why it was wrong |
|--------|-------------|-----------------|
| Dockerfile | nginx on port 80 | Saw `react-scripts` → assumed pure static site. Never found `server.js` |
| docker-compose.yml | Added Redis as a local service | Matched the string `"redis"` inside the k8s ConfigMap value — not an actual dep |
| Node version | `node:20-alpine` | No `.nvmrc` — should have read `FROM node:22.2` from the existing Dockerfile |
| ENV vars | All as runtime `ENV` | `REACT_APP_*` vars need Docker `ARG` — they're baked at `npm run build`, not runtime |
| k8s | Nothing | No Kubernetes detection existed |

## What v4 Fixed

### Fix 1 — Custom server detection
The agent now scans **all** `.js` files in all subdirectories (not just root).
If a `server.js` exists anywhere, it overrides the static-site assumption.
Your project becomes `CRA + Node Server` with the correct port and `node server.js` start command.

### Fix 2 — `REACT_APP_*` become Docker `ARG`, not `ENV`
The agent now knows that these prefixes are **baked into the JS bundle at build time**:
`REACT_APP_*`, `NEXT_PUBLIC_*`, `VITE_*`, `GATSBY_*`, `NUXT_PUBLIC_*`, `PUBLIC_*`

It generates them as `ARG` + `ENV` in the **build stage**, not the runtime stage:
```dockerfile
# Build-time variables — baked into JS bundle at build time
ARG REACT_APP_KEYCLOAK_ACCESS
ARG REACT_APP_KEYCLOAK_REALM
ENV REACT_APP_KEYCLOAK_ACCESS=${REACT_APP_KEYCLOAK_ACCESS}
ENV REACT_APP_KEYCLOAK_REALM=${REACT_APP_KEYCLOAK_REALM}
```
And in `docker-compose.yml` under `build.args`:
```yaml
build:
  args:
    - REACT_APP_KEYCLOAK_ACCESS=${REACT_APP_KEYCLOAK_ACCESS}
```

### Fix 3 — Port from subdirectory server files
Previously only scanned `server.js` at the root.
Now scans **every** `server.js` / `server.ts` / `app.js` in the entire project tree,
so `nest_portal_server/server.js` listening on port 5000 is found.

### Fix 4 — Redis false positive
Previously: any string containing `"redis"` (including env var values like `REDIS_URL=redis://...`)
would add Redis as a local docker-compose service.

Now: Redis only added if `"redis"` or `"ioredis"` is an actual **npm dependency** in `package.json`.
If you connect to an external Redis via env var, no local service is added.

### Fix 5 — Kubernetes detection (new ☸️ k8s.yml tab)
The agent now reads **every `.yml`/`.yaml`** file in the project.
If it finds `apiVersion:` + `kind:` → it's a Kubernetes project.

It extracts:
- Namespace from `metadata.namespace`
- Replica count from `spec.replicas`
- Resource limits/requests from `resources.limits`

And generates a complete `k8s.yml` with:
- `Namespace`
- `ConfigMap` (non-secret vars)
- `Secret` (detected secret vars)
- `Deployment` with liveness + readiness probes
- `Service` (ClusterIP)
- `HorizontalPodAutoscaler` (min → max replicas, CPU+memory targets)

### Fix 6 — Node version from existing Dockerfile
Previously: no `.nvmrc` + no `engines` field → defaulted to Node 20.

Now: also reads `FROM node:22.2` from the existing `Dockerfile` as a version source.
Priority order: `.nvmrc` → `engines.node` → **existing Dockerfile FROM** → default 20.

### Fix 7 — Build-time meta vars as `ARG`
`APP_VERSION`, `BUILD_DATE`, `BUILD_TIME`, `VERSION`, `GIT_SHA`, `GIT_COMMIT`
are now detected as build-time ARGs (not runtime ENV) because they're typically
injected by CI/CD pipelines at build time.

---

## The Correct Output for That Project

**Dockerfile (what it should have generated):**
```dockerfile
# Build stage
FROM node:22-alpine AS builder
WORKDIR /build

# Layer cache
COPY package*.json ./
RUN npm ci

# Build-time variables — baked into JS bundle at build time
ARG REACT_APP_KEYCLOAK_ACCESS
ARG REACT_APP_KEYCLOAK_REALM
ARG REACT_APP_KEYCLOAK_CLIENT
ARG REACT_APP_VERSION
ARG REACT_APP_BUILD_DATE
ARG REACT_APP_BUILD_TIME
ARG REACT_APP_ROLE_BASED_USER
ARG REACT_APP_SECRET_KEY
ARG REACT_APP_ENCRYPT_KEY
ENV REACT_APP_KEYCLOAK_ACCESS=${REACT_APP_KEYCLOAK_ACCESS}
# ... (all the above)

COPY . .
RUN npm run build

# Runtime stage
FROM node:22-alpine AS runtime
WORKDIR /app
COPY --from=builder /build/node_modules ./node_modules
COPY --from=builder /build/ ./

EXPOSE 5000
CMD ["node", "nest_portal_server/server.js"]
```

**k8s.yml tab (new):** Full Deployment + Service + HPA + ConfigMap + Secret,
with namespace `web`, replicas from your existing manifest, resource limits preserved.

---

## How to Use Build-Time Args When Running Docker

```bash
# Build with build-args
docker build \
  --build-arg REACT_APP_KEYCLOAK_ACCESS=https://... \
  --build-arg REACT_APP_KEYCLOAK_REALM=nest \
  --build-arg REACT_APP_VERSION=1.2.3 \
  -t myapp .

# Or with docker compose (set in .env file, compose passes them through)
docker compose up -d --build
```

In CI/CD (GitHub Actions):
```yaml
- name: Build Docker image
  run: |
    docker build \
      --build-arg REACT_APP_KEYCLOAK_ACCESS=${{ secrets.KC_ACCESS }} \
      --build-arg REACT_APP_VERSION=${{ github.ref_name }} \
      -t myapp .
```
