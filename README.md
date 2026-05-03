# IconCraft

Plataforma de generación y optimización de iconos vectoriales impulsada por IA.

## Stack

- **Frontend:** Vite + React + TypeScript + Tailwind CSS + shadcn/ui
- **Backend:** FastAPI (Python)
- **Entorno:** Docker Compose

## Instalación y ejecución

1. Clona el repositorio:
   ```bash
   git clone <repo-url>
   cd iconcraft
   ```

2. Copia el archivo de variables de entorno y completa las claves:
   ```bash
   cp .env.example .env
   ```

3. Inicia los servicios:
   ```bash
   docker compose up --build
   ```

4. Accede a:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Documentación API: http://localhost:8000/docs

## Estructura del proyecto

```
iconcraft/
├── docker-compose.yml
├── .env.example
├── README.md
├── frontend/          # Aplicación React
├── backend/           # API FastAPI
└── output/            # Iconos generados
```
