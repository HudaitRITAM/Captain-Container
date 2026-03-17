# 🐳 Captain Container

> Your personal DevOps assistant — available as both a **desktop app** (drag & drop)
> and a **terminal tool** (command line).
> Drop in your project, get production-ready Docker files in seconds.

---

## 📁 Your Folder Should Look Like This

```
captain-container/
│
├── captain-container-app.html   ← Desktop App  (open in browser, drag & drop)
├── containerize.py              ← Terminal Tool (run in command line)
├── README.md                    ← This file
│
└── sample-output/               ← Example generated files (just for reference)
    ├── Dockerfile
    ├── docker-compose.yml
    ├── .dockerignore
    └── README.docker.md
```

You have **two ways** to use Captain Container — pick whichever feels easier:

| | Desktop App | Terminal Tool |
|--|-------------|---------------|
| **How to open** | Double-click the `.html` file | Run `python3 containerize.py` |
| **How to use** | Drag & drop your project `.zip` | Answer questions in terminal |
| **Best for** | Visual experience, quick scans | Automation, scripts, CI |
| **Needs Python?** | ❌ No | ✅ Yes |
| **AI support?** | ✅ Yes (with API key) | ❌ Not yet |

---

## ✅ Requirements

| Requirement | Needed for | How to check | How to install |
|-------------|-----------|-------------|----------------|
| Any browser (Chrome, Firefox) | Desktop App | — | Already installed |
| Python 3.6+ | Terminal Tool | `python3 --version` | `sudo apt install python3` |
| Docker | Building/running containers | `docker --version` | [docs.docker.com/get-docker](https://docs.docker.com/get-docker/) |

> **Note:** Docker is only needed if you want to actually *build and run* your container.
> Both tools generate the files without Docker installed.

---
---

# 🖥️ PART 1 — Desktop App

## What Is the Desktop App?

The desktop app is a single HTML file you open in your browser — no installation,
no setup, no internet needed (unless you use AI mode). It lives fully on your computer.

You zip your project → drag it into the app window → it scans everything inside
the zip → and generates three ready-to-use Docker files you can download.

---

## How to Open It

```bash
# Option A — Double-click the file in your file manager

# Option B — From terminal:
xdg-open ~/Desktop/captain-container/captain-container-app.html

# Option C — Drag the file into any open browser window
```

---

## How to Use It — Step by Step

### Step 1 — Zip your project

Open a terminal, go into your project folder, and create a zip:

```bash
cd /home/yourname/my-project
zip -r my-project.zip .
```

This creates `my-project.zip` inside your project folder.

### Step 2 — Open the app and drop the zip

Open `captain-container-app.html` in your browser.
Drag `my-project.zip` onto the dashed drop area — or click **Browse Files** to pick it.

### Step 3 — Watch it scan

The app reads every file inside your zip and logs what it finds:

```
→ Reading package.json
→ Reading requirements.txt
✔ Found 47 files
✔ Detected: Node.js · Express.js
→ Port: 3000  |  Start: npm start
✨ Generating Docker files...
```

### Step 4 — Download your files

Three tabs appear at the bottom: **Dockerfile**, **docker-compose.yml**, **.dockerignore**.
Click each tab to see the file. Use the buttons to:
- **Copy** — copies the file content to your clipboard
- **Download** — saves just that one file
- **Download All Files** — saves all three at once

Drop those files into your project folder and you're done.

---

## Every Section of the App Explained

### 🔵 The Drop Zone (top, dashed border)

This is the main area. Drag your `.zip` file here or click **Browse Files**.
The border glows cyan when you drag a file over it — that means it's ready to accept.
Only `.zip` files are accepted. Any size is fine.

---

### 🟣 AI-Powered Mode Banner (purple section at the top)

```
✨ AI-Powered Mode — Add your Anthropic API key for smarter, context-aware generation
```

**What this section is:**
This banner lets you connect the app to Claude AI (made by Anthropic).
When you add your key, instead of using fixed templates, the app sends your
project's file list and key config files to Claude — which reads and understands
your actual code before generating the Docker files.

**Without API key (default):**
The app uses smart built-in templates. It detects your stack, framework, port,
and start command and generates correct, best-practice Docker files.
Works great for 90% of projects. Nothing leaves your computer.

**With API key (AI mode):**
Claude reads your actual `package.json`, `requirements.txt`, `pom.xml` etc.,
understands your specific setup (e.g. "this is a Next.js 14 app with TypeScript,
a custom server.js, running on port 3000") and generates files tailored to
your exact project — not just your stack type.

**How to get an API key:**
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Go to **API Keys** → click **Create Key**
4. Copy the key — it starts with `sk-ant-api03-...`
5. Paste it into the input box in the purple banner
6. Click **Save Key** — it saves in your browser, stays there after you close the app

**When to use AI mode vs local templates:**

| Situation | Recommendation |
|-----------|---------------|
| Standard Node / Python / Java / Go app | Local templates are fine |
| Unusual project structure | AI mode |
| Multiple languages in one project | AI mode |
| Custom build pipeline | AI mode |
| You just want it fast | Local templates |
| You want maximum accuracy | AI mode |

---

### 🟦 Scanning Panel (appears after you drop a zip)

Shows a live log of what the app is doing step by step:
- How many files it found in the zip
- Which key config files it read
- What stack and framework it detected
- Whether it's using AI or local templates to generate

The blue progress bar fills as it works through each step.

---

### 🟩 Detected Stack Card (appears after scan)

Shows what the app figured out about your project:
- **Stack name** — e.g. "Node.js · Express.js"
- **Base image** — the Docker image it chose, e.g. `node:20-alpine`
- **Port** — the port your app runs on inside the container

The coloured feature pills show which best practices are applied:
- `multi-stage build` — uses two Docker stages so the final image is small
- `non-root user` — container runs as a safe user, not as root
- `healthcheck` — Docker automatically checks if your app is still alive
- `layer cache` — dependencies are installed before copying code, so rebuilds are fast

The **⟳ Re-generate** button regenerates all three files fresh without re-scanning.

---

### 🗂️ Output Tabs — The Three Generated Files

**Tab 1: 🐳 Dockerfile**
The main recipe Docker uses to build your app into a container image.
Contains: base image, dependency installation, code copy, port exposure,
non-root user, healthcheck, and the command to start your app.

**Tab 2: ⚙️ docker-compose.yml**
Lets you start your whole stack with one command: `docker compose up -d`.
Includes your app service with port mapping, environment variable file support,
healthcheck, and restart policy. Has commented-out ready-to-use templates for
Nginx (reverse proxy), PostgreSQL (database), and Redis (cache).
Just uncomment whatever you need.

**Tab 3: 🚫 .dockerignore**
Tells Docker which files to skip when building the image.
Automatically customised for your stack — for Node.js it excludes
`node_modules/`, `dist/`, `.next/`, `coverage/` etc.
Keeps your image small and prevents `.env` secrets from ending up inside it.

---

### ⬇ Download All Files

Downloads all three files one after another with a short delay between each
so your browser doesn't block them. Move all three into your project root folder.

### ↺ Scan Another Project

Resets everything back to the drop zone so you can scan a different project.

---

## What the App Auto-Detects

| File found in zip | Detected as | Also reads inside for |
|---|---|---|
| `package.json` | Node.js | Next.js, React, Vue, Express, Fastify, Nuxt, Koa |
| `requirements.txt` | Python | FastAPI, Flask, Django, Gunicorn, Tornado, aiohttp |
| `pom.xml` | Java (Maven) | Spring Boot, Quarkus, Micronaut |
| `build.gradle` | Java (Gradle) | Spring Boot |
| `go.mod` | Go | Gin, Fiber, Echo, Chi |
| `composer.json` | PHP | Laravel, Symfony, Slim |
| `Gemfile` | Ruby | Rails, Sinatra |
| `Cargo.toml` | Rust | Actix-web, Axum, Rocket |
| `*.csproj` / `*.fsproj` | .NET | ASP.NET Core |

---
---

# 💻 PART 2 — Terminal Tool

## What Is the Terminal Tool?

`containerize.py` is a Python script that runs in your terminal.
Instead of drag & drop, it walks you through a short conversation —
asking questions and pre-filling answers it already detected.

Good for: running from scripts, integrating into CI/CD, or if you prefer the terminal.

---

## How to Run It

```bash
# Step 1 — Go into your project folder
cd /home/yourname/my-project

# Step 2 — Run the tool
python3 ~/Desktop/captain-container/containerize.py
```

Press `ENTER` to accept any suggestion shown in `[brackets]`.

---

## Other Useful Ways to Run It

```bash
# Point at a different folder
python3 ~/Desktop/captain-container/containerize.py --dir /path/to/project

# Dry run — shows config without writing any files
python3 ~/Desktop/captain-container/containerize.py --dry-run

# Make it a global shortcut (type 'containerize' from anywhere)
chmod +x ~/Desktop/captain-container/containerize.py
sudo ln -s ~/Desktop/captain-container/containerize.py /usr/local/bin/containerize
containerize
```

---
---

# 🐳 PART 3 — After the Files Are Generated

Drop the three generated files into your project root, then:

```bash
# Easiest way — Docker Compose
docker compose up -d          # build and start
docker compose down           # stop everything
docker compose up -d --build  # rebuild after code changes
docker compose logs -f        # watch logs live

# Or manual Docker commands
docker build -t my-app .
docker run -d -p 3000:3000 --name my-app my-app
docker ps                     # check it's running
docker logs -f my-app         # see logs
docker stop my-app            # stop
docker rm my-app              # remove
```

---
---

# 🚀 PART 4 — How to Upgrade This Product in the Future

This section explains exactly how to add new features or improve the tool.
Everything is plain HTML/JS and Python — no build tools, no npm install, nothing special.

---

## The Two Files and What's Inside Them

### `captain-container-app.html` — Desktop App Structure

```
<style>  ← Visual design (colours, layout, animations) — edit to change appearance
<body>   ← HTML structure (buttons, tabs, panels) — edit to add UI elements
<script> ← All logic — edit to change how detection and generation works
```

**Key functions in `<script>`:**

| Function | What it does | Edit it to... |
|---|---|---|
| `detectStack()` | Reads file list, detects stack & framework | Add a new language |
| `buildDockerfile()` | Generates Dockerfile from template | Improve Dockerfile output |
| `buildCompose()` | Generates docker-compose.yml | Change compose structure |
| `buildIgnore()` | Generates .dockerignore | Add more ignore patterns |
| `generateWithAI()` | Sends data to Claude API | Change the AI prompt |
| `handleZip()` | Main function triggered on file drop | Add new scan steps |
| `downloadAll()` | Downloads all files at once | Add more output files |

### `containerize.py` — Terminal Tool Structure

| Function | What it does |
|---|---|
| `detect_stack()` | Scans files, returns stack info |
| `ask_user_inputs()` | Interactive Q&A in terminal |
| `generate_dockerfile()` | Writes Dockerfile to disk |
| `generate_dockerignore()` | Writes .dockerignore to disk |
| `generate_compose()` | Writes docker-compose.yml to disk |
| `generate_readme()` | Writes README.docker.md to disk |
| `offer_build_run()` | Builds and runs the Docker image |

---

## Common Upgrades — Exactly How to Do Each One

---

### ➕ Add Support for a New Language (e.g. Elixir)

**In `captain-container-app.html`** — find `detectStack()` and add a new block:

```javascript
else if (hasFile('mix.exs')) {
  stack = 'elixir'; display = 'Elixir'; icon = '💜';
  port = '4000'; startCmd = 'mix phx.server';
  buildCmd = 'mix deps.get && mix compile';
  baseImage = 'elixir:1.16-alpine';
  const mix = contents['mix.exs'] || '';
  if (mix.includes('phoenix')) { framework = 'Phoenix'; }
}
```

Then add its ignore patterns in `buildIgnore()`:

```javascript
elixir: ['', '# ── Elixir ──', '_build/', 'deps/', '.elixir_ls/'],
```

**In `containerize.py`** — add to `STACK_RULES`, `BASE_IMAGES`, `DEFAULT_PORTS`,
`DEFAULT_START`, and `DEFAULT_BUILD` dictionaries at the top of the file.

---

### 🎨 Change the Visual Design

Find the `:root { }` block near the top of `<style>` and edit the colour variables:

```css
:root {
  --bg:    #080c10;  /* main background */
  --cyan:  #00e5ff;  /* primary accent colour */
  --green: #3fb950;  /* success colour */
  --text:  #e6edf3;  /* main text colour */
}
```

To switch to a light theme: change `--bg` to `#f5f5f5` and `--text` to `#1a1a1a`.

---

### 📄 Add a Fourth Output File (e.g. `.env.example`)

**Step 1** — Add a generator function in `<script>`:

```javascript
function buildEnvExample(s) {
  return `# .env.example — copy this to .env and fill in real values
NODE_ENV=production
PORT=${s.port}
# DATABASE_URL=postgres://user:pass@db:5432/myapp
`;
}
```

**Step 2** — Call it in `generateLocally()`:

```javascript
generatedFiles.envExample = buildEnvExample(stack);
```

**Step 3** — Add a tab button in the HTML `<div class="tab-bar">`:

```html
<div class="tab" onclick="switchTab('env')">🔑 .env.example</div>
```

**Step 4** — Add the panel content in `<div class="tab-content">`:

```html
<div class="tab-panel" id="tab-env">
  <div class="code-header">
    <div class="code-filename"><span class="dot"></span> .env.example</div>
    <div class="code-actions">
      <button class="btn-copy" onclick="copyCode('envCode', this)">📋 Copy</button>
      <button class="btn-dl" onclick="downloadFile('.env.example', 'envCode')">⬇ Download</button>
    </div>
  </div>
  <div class="code-body"><pre><code id="envCode"></code></pre></div>
</div>
```

**Step 5** — Add it to `downloadAll()`:

```javascript
{ name: '.env.example', id: 'envCode' },
```

---

### 🤖 Improve the AI Prompt

Find the `generateWithAI()` function. The prompt is the long string starting with
`"You are a senior DevOps engineer..."`. Add rules at the bottom of the `Rules:` section:

```
- Always add a comment above every RUN command explaining what it does
- Add LABEL metadata: maintainer, version, description
- Include ARG instructions for any version numbers used
```

---

### 🌐 Add More Framework Detection

Inside `detectStack()`, find the block for your language and add to the framework check.
For Node.js:

```javascript
else if (deps['hono'])    { framework = 'Hono';   port = '3000'; }
else if (deps['nestjs'])  { framework = 'NestJS'; port = '3000'; startCmd = 'npm run start:prod'; }
```

---

### 💾 Download All Files as a Single Zip

Replace the `downloadAll()` function with this (JSZip is already loaded):

```javascript
async function downloadAll() {
  const zip = new JSZip();
  zip.file('Dockerfile',         document.getElementById('dockerfileCode').textContent);
  zip.file('docker-compose.yml', document.getElementById('composeCode').textContent);
  zip.file('.dockerignore',      document.getElementById('ignoreCode').textContent);
  const blob = await zip.generateAsync({ type: 'blob' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'docker-files.zip';
  a.click();
  showToast('✔ docker-files.zip downloaded!', 'success');
}
```

---

### 🔧 Add a Settings Panel (Port Override, App Name, etc.)

Add input fields above the output tabs. Then read the values before generating:

```javascript
// Read overrides before calling buildDockerfile()
const portOverride = document.getElementById('portOverride').value.trim();
if (portOverride) stack.port = portOverride;

const nameOverride = document.getElementById('nameOverride').value.trim();
if (nameOverride) stack.appName = nameOverride;
```

---

## Safe Upgrade Checklist

Before changing anything:

1. **Back up first**: `cp captain-container-app.html captain-container-app.backup.html`
2. **Open DevTools** (`F12` in browser → Console tab) to see errors while testing
3. **One change at a time** — test after each change before making another
4. **Test with a real project zip** after every change

---

## What You Can Safely Ignore (Don't Touch Unless You Need To)

- The CDN `<script>` tags at the top — these load JSZip and Prism from the internet once, then the browser caches them offline
- `Prism.highlightAll()` — this makes the code output colourful, safe to remove if you want plain text
- CSS `@keyframes` blocks (`float`, `spin`, `fadeIn`) — purely visual animations, safe to delete

---
---

# ❓ Troubleshooting

**App won't open / shows blank page**
Open it in Chrome or Firefox. Safari sometimes blocks scripts from local files.

**Dropped the zip but nothing happened**
Make sure it's a `.zip` file. Folders don't work — zip them first.

**AI mode says "HTTP 401"**
Your API key is wrong or expired. Get a new one at [console.anthropic.com](https://console.anthropic.com).

**AI mode says "HTTP 429"**
Rate limit hit. Wait 60 seconds and try again, or use local template mode instead.

**Generated wrong stack**
Click ↺ **Scan Another Project**, re-zip the correct project, and drop it again.

**"python3: command not found"**
```bash
sudo apt update && sudo apt install python3
```

**"docker: command not found"**
Follow: https://docs.docker.com/engine/install/ubuntu/

**Port already in use**
```bash
docker run -p 4000:3000 my-app   # use a different port on the left side
```

---

## 📌 Quick Reference Card

```
# ── Desktop App ──────────────────────────────────
# Open the app
xdg-open ~/Desktop/captain-container/captain-container-app.html

# Zip your project first
cd /path/to/your-project && zip -r project.zip .

# ── Terminal Tool ─────────────────────────────────
python3 ~/Desktop/captain-container/containerize.py
python3 ~/Desktop/captain-container/containerize.py --dir /other/project
python3 ~/Desktop/captain-container/containerize.py --dry-run

# ── After files are generated ─────────────────────
docker compose up -d            # start
docker compose down             # stop
docker compose up -d --build    # rebuild after changes
docker compose logs -f          # watch logs
```

---

## 🗂️ Final Folder Layout

```
captain-container/                ← Keep this safe, don't delete anything here
│
├── captain-container-app.html    ← Desktop App  → open in browser
├── containerize.py               ← Terminal Tool → run with python3
├── README.md                     ← This file
│
└── sample-output/                ← Reference examples only
    ├── Dockerfile
    ├── docker-compose.yml
    ├── .dockerignore
    └── README.docker.md


your-project/                     ← Your actual app's code
│
├── (your source code...)
│
├── Dockerfile                    ← Generated — drop here ✅
├── docker-compose.yml            ← Generated — drop here ✅
└── .dockerignore                 ← Generated — drop here ✅
```

---

*Captain Container · Python 3 + HTML/JS · No installation required · Works on any Linux distro*
