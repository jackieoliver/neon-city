# Neon City

_Built in December 2025 and originally hosted in a private repository; published here as a single snapshot._

40 AI coding agents ran in parallel, and each one built a single interactive cyberpunk visual: boids, fluid, fractals, Game of Life, metaballs, Voronoi and more. `index.html` is the hub that embeds them, four at a time. `gallery.html` shows pixel-art assets generated with Gemini.

![Neon City hub](swarm_hub.png)

## How it works

```mermaid
flowchart LR
    A["serve.py (port 8888)"] --> B[index.html hub]
    A --> G[gallery.html]
    B --> C[40-entry experiences list]
    C -->|4 per page| D["iframe: experiences/*/index.html"]
    D -->|off-screen| E[neon-pause postMessage]
    H[generate_assets.py] --> I{Gemini returned an image?}
    I -->|Yes| J["assets/category/name.png"]
    I -->|No| K[placeholder SVG]
    J --> G
```

The hub only knows each experience's folder name and loads them as iframes, four per page, telling off-screen ones to pause. How the agents were run is not recorded in this repo.

## Run

```sh
python3 serve.py        # opens http://localhost:8888
```

Each experience is one self-contained `experiences/<name>/index.html` with no build step.

## Regenerate assets

```sh
GEMINI_API_KEY=... python3 generate_assets.py
```
