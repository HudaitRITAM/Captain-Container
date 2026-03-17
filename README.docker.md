# 🐳 Captain Container

> A smart, simple DevOps assistant that runs in your terminal.
> It looks at your project, figures out what kind of app it is,
> asks you a few questions, and generates everything you need
> to containerize it with Docker — in under 2 minutes.

---

## 📁 What's Inside Your Folder

After you create the `captain-container` folder and copy the files in,
it should look like this:

```
captain-container/
│
├── containerize.py          ← The main tool (this is what you run)
│
└── sample-output/           ← Example files it generated (for reference)
    ├── Dockerfile
    ├── docker-compose.yml
    ├── .dockerignore
    └── README.docker.md
```

You only ever need to run **one file**: `containerize.py`

---

## ✅ Requirements

Before running the tool, make sure you have these installed on your Linux machine:

| Requirement | How to check | How to install |
|-------------|-------------|----------------|
| Python 3.6+ | `python3 --version` | `sudo apt install python3` |
| Docker | `docker --version` | [docs.docker.com/get-docker](https://docs.docker.com/get-docker/) |

> **Note:** Docker is only needed if you want the tool to also
> *build and run* your container. The file generation works without it.

---

## 🚀 How to Run It — Step by Step

### Step 1 — Open your terminal

Press `Ctrl + Alt + T` on Ubuntu/Debian, or open any terminal you use.

---

### Step 2 — Go into your project folder

This is the folder that has your app's code in it.
For example, if your app is in `/home/yourname/my-website`:

```bash
cd /home/yourname/my-website
```

---

### Step 3 — Run the tool

```bash
python3 /path/to/captain-container/containerize.py
```

**Real example** — if you put `captain-container` on your Desktop:

```bash
python3 ~/Desktop/captain-container/containerize.py
```

That's it. The tool will start asking you questions.

---

## 💬 What Happens When You Run It

The tool walks you through a short conversation. Here's exactly what you'll see:

```
🐳  DevOps Containerization Agent  v1.0

  ℹ  Scanning project: /home/yourname/my-website
  ✔  Detected → Node.js          ← It figured out your stack automatically

── Project Configuration ──────────────────────────────
  ?  App name [my-website]:        ← Press ENTER to accept, or type a new name
  ?  Container port [3000]:        ← Press ENTER if 3000 is fine
  ?  Start command [npm start]:    ← Press ENTER to accept
  ?  Build command: npm ci         ← Type your build command, or ENTER to skip

── Environment Variables ──────────────────────────────
  ℹ  Enter KEY=VALUE pairs. Empty line to finish.
  >  NODE_ENV=production           ← Type env vars like this
  >  PORT=3000
  >                                ← Press ENTER on empty line to stop

── Optional Files ─────────────────────────────────────
  ?  Generate docker-compose.yml? (Y/n):    ← Press ENTER for Yes
  ?  Generate README.md? (Y/n):             ← Press ENTER for Yes
  ?  Run as non-root user? (Y/n):           ← Press ENTER for Yes (safer)

── Generating Files ───────────────────────────────────
  ✔  Dockerfile created
  ✔  .dockerignore created
  ✔  docker-compose.yml created
  ✔  README.docker.md created

── Build & Run (Bonus) ────────────────────────────────
  ?  Build Docker image now? (y/N):   ← Type y to build right now, or N to skip
  ?  Run the container now? (y/N):    ← Type y to run it, or N to skip

  ✔  Container running → http://localhost:3000  🎉
```

---

## 📄 Files It Creates (In Your Project Folder)

After running, these files appear **inside your project folder**:

### `Dockerfile`
The recipe Docker uses to build your app into a container image.
It automatically uses the right base image for your stack and follows best practices.

### `.dockerignore`
Tells Docker which files to skip (like `node_modules/`, `.env`, `.git`).
Makes your image smaller and faster to build.

### `docker-compose.yml`
Lets you start your app with one command: `docker compose up -d`.
Also has a commented-out database template you can uncomment if needed.

### `README.docker.md`
A quick-start guide for anyone who wants to run your app with Docker.
Auto-filled with your app name, port, and environment variables.

---

## 🧠 What It Auto-Detects (You Don't Have to Tell It)

The tool scans your project folder and figures out your stack automatically:

| If it finds this file... | It knows you're using... | Default port |
|--------------------------|--------------------------|-------------|
| `package.json` | Node.js | 3000 |
| `requirements.txt` | Python | 5000 |
| `pom.xml` | Java (Maven) | 8080 |
| `build.gradle` | Java (Gradle) | 8080 |
| `go.mod` | Go | 8080 |
| `composer.json` | PHP | 80 |
| `Gemfile` | Ruby | 3000 |
| `Cargo.toml` | Rust | 8080 |
| `*.csproj` | .NET | 8080 |

It also reads *inside* files for smarter defaults:
- Finds Flask/FastAPI/Django in `requirements.txt` → sets the right start command
- Reads `scripts.start` from `package.json` → uses `npm start` automatically
- Reads `engines.node` version → picks the matching Docker image

---

## ⚙️ Other Ways to Run It

### Point it at a different folder (without cd-ing into it)

```bash
python3 ~/Desktop/captain-container/containerize.py --dir /path/to/your/project
```

### Dry run — see what it *would* do, without writing any files

```bash
python3 ~/Desktop/captain-container/containerize.py --dry-run
```

### Make it a global command (optional, run from anywhere)

```bash
# Make it executable
chmod +x ~/Desktop/captain-container/containerize.py

# Create a shortcut so you can just type: containerize
sudo ln -s ~/Desktop/captain-container/containerize.py /usr/local/bin/containerize

# Now from any project folder just run:
containerize
```

---

## 🐳 After the Files Are Generated

Once `Dockerfile` is in your project, here are the Docker commands you'll use:

```bash
# Build your Docker image
docker build -t my-app-name .

# Run your container
docker run -d -p 3000:3000 --name my-app-name my-app-name

# Check if it's running
docker ps

# See logs
docker logs -f my-app-name

# Stop it
docker stop my-app-name

# Remove the container
docker rm my-app-name
```

### Or use Docker Compose (easier):

```bash
# Start (builds automatically too)
docker compose up -d

# Stop
docker compose down

# Rebuild after code changes
docker compose up -d --build

# See logs
docker compose logs -f
```

---

## ❓ Troubleshooting

**"python3: command not found"**
```bash
sudo apt update && sudo apt install python3
```

**"docker: command not found"**
Follow the official guide: https://docs.docker.com/engine/install/ubuntu/

**"Permission denied" when running the script**
```bash
chmod +x /path/to/captain-container/containerize.py
```

**Tool generated wrong stack**
When it asks `Override stack?` — just type the correct one
(e.g. `python`, `node`, `java`, `go`, `php`, `ruby`, `rust`, `dotnet`)

**Port is already in use when running container**
Change the host port (left side of the colon):
```bash
docker run -p 4000:3000 my-app   # your machine's port 4000 → container's 3000
```

---

## 📌 Quick Reference Card

```
# Run the tool on your current project
python3 ~/Desktop/captain-container/containerize.py

# Run on a specific project
python3 ~/Desktop/captain-container/containerize.py --dir /path/to/project

# Dry run (no files written)
python3 ~/Desktop/captain-container/containerize.py --dry-run

# After generating files — build & run manually
docker build -t myapp .
docker run -d -p 3000:3000 myapp

# Or with Compose
docker compose up -d
```

---

## 🗂️ Folder Layout Summary

```
captain-container/            ← Keep this folder somewhere safe
│
└── containerize.py           ← Run this from inside any project

your-project/                 ← Your actual app code
│
├── (your code files...)
│
├── Dockerfile                ← Generated by the tool ✅
├── .dockerignore             ← Generated by the tool ✅
├── docker-compose.yml        ← Generated by the tool ✅
└── README.docker.md          ← Generated by the tool ✅
```

---

*Built with Python 3 · Zero external dependencies · Works on any Linux distro*