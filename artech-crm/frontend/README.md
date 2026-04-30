# Artech CRM Frontend

![Vue.js](https://img.shields.io/badge/Vue.js-3-4FC08D?style=flat&logo=vuedotjs&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-4+-646CFF?style=flat&logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3-06B6D4?style=flat&logo=tailwindcss&logoColor=white)
![Yarn](https://img.shields.io/badge/Yarn-1.22+-2C8EBB?style=flat&logo=yarn&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat&logo=nodedotjs&logoColor=white)

Vue.js 3 SPA frontend for Artech CRM. Communicates with the Artech backend via REST API.

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| ![Vue.js](https://img.shields.io/badge/-Vue.js_3-4FC08D?style=flat&logo=vuedotjs&logoColor=white) | Reactive component framework (Composition API) |
| ![Vite](https://img.shields.io/badge/-Vite-646CFF?style=flat&logo=vite&logoColor=white) | Dev server & production bundler |
| ![TailwindCSS](https://img.shields.io/badge/-Tailwind_CSS-06B6D4?style=flat&logo=tailwindcss&logoColor=white) | Utility-first CSS styling |
| ![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) | App logic |
| ![Yarn](https://img.shields.io/badge/-Yarn-2C8EBB?style=flat&logo=yarn&logoColor=white) | Package manager |

## Setup

```bash
yarn install
yarn dev
```

Requires the Artech bench running at `http://localhost:8000`. See [parent README](../README.md) for full setup.

## Build

```bash
yarn build
```

Built assets are output to `../artech_crm/public/frontend/`.
