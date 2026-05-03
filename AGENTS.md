# IconCraft — AGENTS

## Project overview
AI-powered vector icon generation & optimization platform. Users describe an icon in natural language, select style/size/color, and get a production-ready SVG.

## Stack
- **Frontend:** Vite + React 18 + TypeScript (strict) + Tailwind CSS 3 + shadcn/ui + Lucide icons
- **Backend:** FastAPI (Python 3.12+) + Uvicorn
- **Infra:** Docker Compose (frontend & backend services)
- **Image pipeline:** Pillow → rembg → vtracer → scour
- **Image Providers:** Plugable via `BaseProvider` ABC (env: `IMAGE_PROVIDER`) — flux, openai
- **LLM Providers:** Plugable via `BaseLLMProvider` ABC (env: `LLM_PROVIDER`) — openai, deepseek, anthropic

## Directory structure
```
IconCraft/
├── AGENTS.md
├── docker-compose.yml
├── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.tsx              # Main UI (prompt, canvas, properties panel)
│   │   ├── main.tsx             # Entry point
│   │   ├── index.css            # Tailwind + CSS variables (light/dark)
│   │   ├── hooks/use-theme.ts   # Theme toggle hook
│   │   ├── lib/utils.ts         # cn() utility
│   │   ├── components/          # shadcn/ui components (@/components/ui/*)
│   │   └── ...
│   ├── components.json          # shadcn/ui config
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── vite.config.ts           # @/ alias → ./src
├── backend/
│   ├── main.py                  # FastAPI app, CORS, routers
│   ├── app/
│   │   ├── routers/
│   │   │   ├── generate.py      # POST /api/generate
│   │   │   ├── chat.py          # POST /api/chat
│   │   │   └── mcp.py           # GET /api/mcp
│   │   ├── pipeline/
│   │   │   ├── preprocessor.py  # Pillow image pre-processing
│   │   │   ├── vectorizer.py    # vtracer bitmap→SVG
│   │   │   ├── optimizer.py     # scour SVG optimization
│   │   │   └── prompt_builder.py
│   │   ├── providers/
│   │   │   └── base.py          # BaseProvider ABC (generate → bytes)
│   │   └── mcp/
│   │       ├── tools.py
│   │       └── server.py
│   ├── requirements.txt
│   └── Dockerfile
└── output/                      # Generated SVGs
```

## Commands
```bash
# Frontend
cd frontend && npm run dev      # Dev server :3000
cd frontend && npm run build    # Production build

# Backend
cd backend && uvicorn main:app --reload --port 8000

# Full stack
docker compose up --build
```

## Coding conventions

### General
- No comments unless the intent is non-obvious
- Minimal, clean code — don't add extra abstractions
- Follow existing patterns in neighboring files

### Frontend (React + TypeScript)
- Strict TypeScript — no `any`, no `@ts-ignore`
- Import path alias: `@/` → `./src/`
- CSS: Tailwind utility classes + CSS variables for theming
- Components: shadcn/ui style (`@/components/ui/*`)
- Hooks in `src/hooks/`, utils in `src/lib/`
- Use `cn()` from `@/lib/utils` for className merging
- Lucide icons for all iconography

### Backend (Python)
- FastAPI async endpoints
- Type hints everywhere
- Pipeline stages in `app/pipeline/` (preprocess → vectorize → optimize)
- Providers in `app/providers/` (extend `BaseProvider`)
- Pydantic models for request/response

### Environment variables
Copy `.env.example` → `.env` and fill:
- `LLM_API_KEY` — LLM provider key (OpenAI / DeepSeek / Anthropic)
- `LLM_PROVIDER` — LLM provider name (default: `openai`)
- `IMAGE_API_KEY` — Image generation API key
- `IMAGE_PROVIDER` — Image provider name (default: `flux`)

## Git
- No commits unless explicitly asked
- Never force push to main/master
- Conventional commit style: `type: description`

## Testing
- Backend: `pytest` (if available)
- Frontend: check `package.json` for test scripts
