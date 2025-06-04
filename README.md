# openai-blog-ssg-next

> **A next-generation static site generator and publishing platform, powered by Next.js and enhanced with AI.**

---

## Overview

This project is a modern static site generator, built on [Next.js](https://nextjs.org/) for ultra-fast, SEO-optimized static blogs, and extended with an AI backend for automatic content generation, smart suggestions, and streamlined publishing workflows.

* **Static blog SSG (Next.js)**: Generate static, portable, lightning-fast blog sites from Markdown content.
* **AI backend (FastAPI / Ursus)**: Advanced features for content creation, tagging, metadata, and automated publishing using OpenAI-powered suggestions.
* **Zero-downtime atomic deployment:** Production deploy strategy with directory & permissions swap, perfect for Docker/Nginx.
* **Markdown-first workflow:** Write content in Markdown, easily versioned and edited.
* **Fully Dockerized:** Separate, composable containers for frontend and backend. Clean CI/CD pipeline.

---

## Repository Structure

```
openai-blog-ssg-next/
├── frontend/       # Next.js static site generator
│   ├── ...         # Pages, components, config, etc.
│   └── out/        # Build output (static export)
├── ai/             # FastAPI (Ursus) AI backend
│   ├── ...         # Content helpers, API endpoints
│   └── ...
├── docker-compose.yml
├── Dockerfile.frontend
├── Dockerfile.ai
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/emirbaycan/openai-blog-ssg-next.git
cd openai-blog-ssg-next
```

### 2. Install dependencies

> Requires Node.js 18+ and Yarn 3.x (Berry)

```bash
cd frontend
yarn install
cd ..
cd ai
pip install -r requirements.txt
```

### 3. Development

#### Run Next.js Frontend (SSG)

```bash
cd frontend
yarn dev
```

#### Run AI Backend (FastAPI)

```bash
cd ai
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

### 4. Docker Usage (Production)

You can build and run both services using Docker Compose:

```bash
docker-compose up --build
```

* Frontend will be available on `localhost:3000` (or as configured).
* AI backend will be on `localhost:5000` (or as configured).

---

## Deployment & Zero Downtime Strategy

Production deploy is designed for **zero downtime** using directory and permission swapping for atomic releases, as described in the `/ai/scripts/deploy.py` (or your deploy script).

* Only one of the `active` or `backup` folders is ever readable at a time; the other is write-only and inaccessible.
* This enables safe, robust failover for static content in Nginx.

See detailed deployment strategies in the documentation or comments in the deploy script.

---

## Contributing

Pull requests and issues are welcome! Please see [openai-blog-ssg-ursus](https://github.com/emirbaycan/openai-blog-ssg-ursus) for the original AI engine, or open a discussion for larger ideas.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Credits

* Built and maintained by [@emirbaycan](https://github.com/emirbaycan)
* Inspired by modern SSG and MLOps workflows
* Powered by OpenAI, Next.js, FastAPI
