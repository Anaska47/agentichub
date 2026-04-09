from __future__ import annotations

import json
from string import Template


def render_text_files(concept) -> dict[str, str]:
    return {
        "README.md": render_readme(concept),
        "docs/game-design.md": render_game_design(concept),
        "docs/store-listing.md": render_store_listing(concept),
        "docs/ads-plan.md": render_ads_plan(concept),
        "docs/figma-handoff.md": render_figma_handoff(concept),
        "docs/github-backlog.md": render_github_backlog(concept),
        "docs/code-connect-targets.json": render_code_connect_targets(concept),
        ".github/ISSUE_TEMPLATE/launch-checklist.md": render_issue_template(concept),
        ".github/pull_request_template.md": render_pr_template(concept),
    }


def render_prototype(concept) -> dict[str, str]:
    return {
        "web/index.html": render_index_html(concept),
        "web/styles.css": render_styles(concept),
        "web/game.js": render_game_js(concept),
    }


def render_batch_files(batch) -> dict[str, str]:
    return {
        "portfolio/github-repo-plan.md": render_portfolio_github_plan(batch),
        "portfolio/figma-batch-handoff.md": render_portfolio_figma_handoff(batch),
    }


def render_readme(concept) -> str:
    return f"""# {concept.name}

Prototype casual mobile-first genere par la factory.

## Positionnement

- Mechanic: `{concept.mechanic}`
- Theme: `{concept.theme}`
- Meta loop: `{concept.meta_loop}`
- Art style: `{concept.art_style}`
- Rewarded hook: `{concept.reward_type}`

## Hypothese business

Cette app vise une session courte, une comprehension immediate et une monetisation prudente via rewarded ads en priorite.

## Etat de la generation

- Brief produit: OK
- Prototype web: OK
- Store listing draft: OK
- Ads plan draft: OK

## Suite recommandee

1. Tester le prototype sur mobile.
2. Ajuster la difficulte des 30 premieres secondes.
3. Ajouter analytics, consentement et ads seulement apres validation UX.
"""


def render_game_design(concept) -> str:
    return f"""# Game Design

## Fantasy

{concept.name} transforme le theme `{concept.theme}` en boucle de jeu simple et lisible.

## Core loop

1. Lancer une partie de 30 a 90 secondes.
2. Maitriser la boucle `{concept.mechanic}`.
3. Cumuler score et monnaie soft.
4. Debloquer une couche meta basee sur `{concept.meta_loop}`.
5. Rejouer pour battre son meilleur run.

## Hook

{concept.core_hook}

## Differentiation

{concept.differentiator}

## Session design

- Session cible: 45 secondes
- Courbe de difficulte: douce pendant 10 secondes, puis acceleration
- Defaite: claire et immediate
- Retry: en 1 tap

## Monetisation

- Rewarded ad: proposer `{concept.reward_type}` apres echec ou au retour au hub
- Interstitial: `{concept.interstitial_cadence}`
- Eviter toute pub entre l'action utilisateur et la consequence attendue
"""


def render_store_listing(concept) -> str:
    short_description = f"{concept.core_hook} Releve le defi dans un univers {concept.theme}."
    long_description = (
        f"{concept.name} est un jeu casual mobile centre sur `{concept.mechanic}`. "
        f"Tu enchaines des runs courts, debloques des progres via {concept.meta_loop}, "
        f"et cherches la maitrise parfaite dans une presentation {concept.art_style}."
    )
    payload = {
        "title": concept.name,
        "short_description": short_description,
        "long_description": long_description,
        "keywords": [
            concept.theme,
            concept.mechanic,
            "casual game",
            "mobile arcade",
            "quick sessions",
        ],
    }
    return "# Store Listing Draft\n\n```json\n" + json.dumps(payload, indent=2) + "\n```\n"


def render_ads_plan(concept) -> str:
    bullets = "\n".join(f"- {note}" for note in concept.policy_notes)
    return f"""# Ads Plan

## Format principal

- Rewarded ads d'abord
- Interstitials en support seulement

## Placement recommande

- Ecran de game over
- Ecran de resultat
- Retour au hub meta

## Regles

{bullets}

## Instrumentation a ajouter

- Taux d'acceptation rewarded
- Retention D1 / D7
- Run length mediane
- ARPDAU
"""


def render_figma_handoff(concept) -> str:
    repo_name = f"app-{concept.slug}"
    return f"""# Figma Handoff

## Goal

Construire dans Figma une mini experience mobile-first pour `{concept.name}` en gardant une structure reutilisable pour les autres apps du portefeuille.

## Screens to create

1. `{concept.name} / Menu`
2. `{concept.name} / Run HUD`
3. `{concept.name} / Game Over`
4. `{concept.name} / Rewarded Offer`
5. `{concept.name} / Meta Progression`

## Visual direction

- Theme: `{concept.theme}`
- Art style: `{concept.art_style}`
- Core emotion: rapide, lisible, satisfaisant
- Dominant mechanic: `{concept.mechanic}`

## Components to prepare

- Primary button
- Secondary button
- Stat card
- Reward modal
- Top HUD bar
- Progress card
- Empty state panel

## Token guidance

- 4 color roles minimum: background, surface, accent, danger
- 4 spacing tokens minimum: 8, 12, 16, 24
- Radius family: small, medium, pill
- Typography: display, title, body, caption

## Code connect targets

- Repo target: `{repo_name}`
- `web/index.html`
- `web/styles.css`
- `web/game.js`

## Review checklist

- Aucun placeholder text
- Lisible sur viewport 360x640
- HUD et CTA visibles sans scroll
- Reward modal distinct du game over
- Variantes exportables pour store screenshots
"""


def render_github_backlog(concept) -> str:
    repo_name = f"app-{concept.slug}"
    return f"""# GitHub Backlog

## Suggested repository

- `{repo_name}`

## Milestones

1. Prototype jouable
2. Retention et tuning
3. Monetisation prudente
4. Packaging Android
5. Store readiness

## Issues to open

- Implement analytics events for `{concept.mechanic}`
- Add mobile balancing pass for first 3 sessions
- Integrate consent flow before ads
- Add rewarded flow for `{concept.reward_type}`
- Add Android packaging pipeline
- Prepare Play Store listing assets
- Create closed testing checklist

## Labels

- `prototype`
- `retention`
- `ads`
- `android`
- `store`
- `figma`
"""


def render_code_connect_targets(concept) -> str:
    payload = {
        "screen_set": [
            f"{concept.name} / Menu",
            f"{concept.name} / Run HUD",
            f"{concept.name} / Game Over",
            f"{concept.name} / Rewarded Offer",
            f"{concept.name} / Meta Progression",
        ],
        "targets": [
            {"componentName": "MenuShell", "source": "web/index.html"},
            {"componentName": "ThemeTokens", "source": "web/styles.css"},
            {"componentName": "GameRuntime", "source": "web/game.js"},
        ],
    }
    return json.dumps(payload, indent=2)


def render_issue_template(concept) -> str:
    return f"""---
name: Launch checklist
about: Track production readiness for {concept.name}
title: "[launch] {concept.slug}"
labels: store, android
assignees: ""
---

## Product

- [ ] Core loop is stable
- [ ] Difficulty tuned for first-time users
- [ ] Rewarded prompt adds value

## Monetisation

- [ ] Consent flow implemented
- [ ] Rewarded ads only on clear opt-in
- [ ] Interstitial cadence reviewed

## Release

- [ ] Closed testing completed
- [ ] Store assets prepared
- [ ] Policy review complete
"""


def render_pr_template(concept) -> str:
    return f"""## Summary

- app: `{concept.name}`
- theme: `{concept.theme}`
- mechanic: `{concept.mechanic}`

## Checks

- [ ] Prototype runs locally
- [ ] Mobile viewport checked
- [ ] Ads placement still policy-safe
- [ ] Figma handoff updated if UI changed

## Notes

Explain the retention or monetisation impact of this change.
"""


def render_portfolio_github_plan(batch) -> str:
    lines = ["# Portfolio GitHub Plan", "", "## Suggested repos", ""]
    for concept in batch:
        lines.append(f"- `app-{concept.slug}`: prototype, Android packaging, release tracking")
    lines.extend(
        [
            "",
            "## Shared labels",
            "",
            "- `prototype`",
            "- `retention`",
            "- `ads`",
            "- `android`",
            "- `store`",
            "- `figma`",
            "",
            "## Shared milestones",
            "",
            "1. Prototype",
            "2. Retention",
            "3. Monetisation",
            "4. Android ship",
            "5. Store launch",
        ]
    )
    return "\n".join(lines) + "\n"


def render_portfolio_figma_handoff(batch) -> str:
    lines = [
        "# Portfolio Figma Handoff",
        "",
        "## Batch pages",
        "",
    ]
    for concept in batch:
        lines.append(f"- `{concept.name}`: Menu, Run HUD, Game Over, Rewarded Offer, Meta Progression")
    lines.extend(
        [
            "",
            "## Shared design system needs",
            "",
            "- Button variants",
            "- Stat cards",
            "- Modals",
            "- HUD primitives",
            "- Rewarded ad entry pattern",
            "",
            "## Code connect priorities",
            "",
            "- Map layout shell to `web/index.html`",
            "- Map tokens to `web/styles.css`",
            "- Map gameplay runtime to `web/game.js`",
        ]
    )
    return "\n".join(lines) + "\n"


def render_index_html(concept) -> str:
    return f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{concept.name}</title>
    <link rel="stylesheet" href="./styles.css" />
  </head>
  <body data-mechanic="{concept.mechanic}">
    <main class="shell">
      <section class="hud">
        <p class="eyebrow">{concept.theme}</p>
        <h1>{concept.name}</h1>
        <p class="hook">{concept.core_hook}</p>
        <div class="stats">
          <div><span>Score</span><strong id="score">0</strong></div>
          <div><span>Best</span><strong id="best">0</strong></div>
          <div><span>Status</span><strong id="status">Ready</strong></div>
        </div>
        <button id="actionButton">Start Run</button>
        <p class="hint" id="hint"></p>
      </section>
      <section class="playfield">
        <canvas id="game" width="360" height="640"></canvas>
      </section>
    </main>
    <script src="./game.js"></script>
  </body>
</html>
"""


def render_styles(concept) -> str:
    palettes = {
        "clean flat arcade": ("#f4efe6", "#0f172a", "#ff7b00", "#0284c7"),
        "bold toy-like shapes": ("#fff4d6", "#14213d", "#ef476f", "#06d6a0"),
        "retro neon panels": ("#07111f", "#f8fafc", "#22d3ee", "#f97316"),
        "soft paper-cut layers": ("#f8f7f2", "#263238", "#8bc34a", "#ffb703"),
    }
    bg, text, accent, secondary = palettes.get(
        concept.art_style,
        ("#f4efe6", "#0f172a", "#ff7b00", "#0284c7"),
    )
    return f""":root {{
  --bg: {bg};
  --text: {text};
  --accent: {accent};
  --secondary: {secondary};
  --panel: rgba(255, 255, 255, 0.72);
}}

* {{
  box-sizing: border-box;
}}

body {{
  margin: 0;
  min-height: 100vh;
  background:
    radial-gradient(circle at top, color-mix(in srgb, var(--accent) 22%, transparent), transparent 35%),
    linear-gradient(160deg, var(--bg), color-mix(in srgb, var(--secondary) 16%, white));
  color: var(--text);
  font-family: "Trebuchet MS", "Segoe UI", sans-serif;
}}

.shell {{
  width: min(100%, 1100px);
  margin: 0 auto;
  padding: 24px;
  display: grid;
  gap: 20px;
}}

.hud {{
  padding: 20px;
  border-radius: 24px;
  background: var(--panel);
  backdrop-filter: blur(10px);
  box-shadow: 0 16px 40px rgba(15, 23, 42, 0.12);
}}

.eyebrow {{
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--secondary);
  font-size: 0.75rem;
}}

h1 {{
  margin: 8px 0 12px;
  line-height: 1;
}}

.hook {{
  margin: 0 0 20px;
  max-width: 42ch;
}}

.stats {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}}

.stats div {{
  padding: 12px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.58);
}}

.stats span {{
  display: block;
  font-size: 0.75rem;
  opacity: 0.7;
}}

.stats strong {{
  font-size: 1.25rem;
}}

button {{
  border: none;
  border-radius: 999px;
  background: var(--accent);
  color: white;
  padding: 14px 20px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
}}

.hint {{
  min-height: 1.5rem;
  opacity: 0.8;
}}

.playfield {{
  display: flex;
  justify-content: center;
}}

canvas {{
  width: min(100%, 360px);
  height: auto;
  border-radius: 24px;
  background: rgba(15, 23, 42, 0.92);
  box-shadow: 0 16px 40px rgba(15, 23, 42, 0.25);
}}

@media (min-width: 900px) {{
  .shell {{
    grid-template-columns: 360px 1fr;
    align-items: start;
  }}
}}
"""


def render_game_js(concept) -> str:
    if concept.mechanic == "lane-dodge":
        return lane_dodge_template(concept)
    if concept.mechanic == "survival-harvest":
        return survival_harvest_template(concept)
    return tap_burst_template(concept)


def lane_dodge_template(concept) -> str:
    return Template(
        """const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const scoreNode = document.getElementById("score");
const bestNode = document.getElementById("best");
const statusNode = document.getElementById("status");
const hintNode = document.getElementById("hint");
const button = document.getElementById("actionButton");

const lanes = [80, 180, 280];
const state = {
  running: false,
  score: 0,
  best: Number(localStorage.getItem("${slug}:best") || 0),
  playerLane: 1,
  obstacles: [],
  lastSpawn: 0,
  speed: 3.2,
  raf: 0,
};

bestNode.textContent = state.best;
hintNode.textContent = "Touche l'ecran pour changer de voie. Survis le plus longtemps possible.";

canvas.addEventListener("pointerdown", () => {
  if (!state.running) {
    startRun();
    return;
  }
  state.playerLane = (state.playerLane + 1) % lanes.length;
});

button.addEventListener("click", () => {
  if (state.running) {
    endRun("Run aborted");
    return;
  }
  startRun();
});

function startRun() {
  state.running = true;
  state.score = 0;
  state.playerLane = 1;
  state.obstacles = [];
  state.lastSpawn = 0;
  state.speed = 3.2;
  button.textContent = "Stop Run";
  statusNode.textContent = "Running";
  loop(performance.now());
}

function endRun(reason) {
  state.running = false;
  cancelAnimationFrame(state.raf);
  state.best = Math.max(state.best, state.score);
  localStorage.setItem("${slug}:best", String(state.best));
  scoreNode.textContent = state.score;
  bestNode.textContent = state.best;
  statusNode.textContent = reason;
  button.textContent = "Start Run";
  hintNode.textContent = "Rewarded slot suggere: regarder une pub pour ${reward}.";
  draw();
}

function spawn(now) {
  if (now - state.lastSpawn < 800) {
    return;
  }
  state.lastSpawn = now;
  state.obstacles.push({
    lane: Math.floor(Math.random() * lanes.length),
    y: -30,
    size: 24 + Math.random() * 12,
  });
}

function update() {
  state.speed += 0.002;
  state.score += 1;
  scoreNode.textContent = state.score;
  for (const obstacle of state.obstacles) {
    obstacle.y += state.speed;
    if (obstacle.y > 600 && obstacle.lane === state.playerLane) {
      endRun("Crash");
      return;
    }
  }
  state.obstacles = state.obstacles.filter((obstacle) => obstacle.y < 680);
}

function drawTrack() {
  ctx.fillStyle = "#0b1324";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = "rgba(255,255,255,0.15)";
  ctx.lineWidth = 4;
  for (const x of [130, 230]) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.stroke();
  }
}

function drawPlayer() {
  ctx.fillStyle = "#22d3ee";
  ctx.beginPath();
  ctx.roundRect(lanes[state.playerLane] - 22, 560, 44, 52, 14);
  ctx.fill();
}

function drawObstacles() {
  ctx.fillStyle = "#f97316";
  for (const obstacle of state.obstacles) {
    ctx.beginPath();
    ctx.roundRect(lanes[obstacle.lane] - obstacle.size / 2, obstacle.y, obstacle.size, obstacle.size, 10);
    ctx.fill();
  }
}

function draw() {
  drawTrack();
  drawPlayer();
  drawObstacles();
}

function loop(now) {
  if (!state.running) {
    return;
  }
  spawn(now);
  update();
  draw();
  state.raf = requestAnimationFrame(loop);
}

draw();
"""
    ).substitute(slug=concept.slug, reward=concept.reward_type)


def tap_burst_template(concept) -> str:
    return Template(
        """const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const scoreNode = document.getElementById("score");
const bestNode = document.getElementById("best");
const statusNode = document.getElementById("status");
const hintNode = document.getElementById("hint");
const button = document.getElementById("actionButton");

const state = {
  running: false,
  score: 0,
  best: Number(localStorage.getItem("${slug}:best") || 0),
  timeLeft: 30,
  target: null,
  raf: 0,
  tickTimer: 0,
};

bestNode.textContent = state.best;
hintNode.textContent = "Tape la cible des qu'elle apparait. Enchaine les combos.";

canvas.addEventListener("pointerdown", (event) => {
  if (!state.running) {
    startRun();
    return;
  }
  const rect = canvas.getBoundingClientRect();
  const x = ((event.clientX - rect.left) / rect.width) * canvas.width;
  const y = ((event.clientY - rect.top) / rect.height) * canvas.height;
  if (state.target && Math.hypot(x - state.target.x, y - state.target.y) < state.target.radius) {
    state.score += 10;
    scoreNode.textContent = state.score;
    spawnTarget();
  }
});

button.addEventListener("click", () => {
  if (state.running) {
    endRun("Run aborted");
    return;
  }
  startRun();
});

function startRun() {
  state.running = true;
  state.score = 0;
  state.timeLeft = 30;
  state.tickTimer = performance.now();
  scoreNode.textContent = state.score;
  statusNode.textContent = "Running";
  button.textContent = "Stop Run";
  spawnTarget();
  loop(performance.now());
}

function spawnTarget() {
  state.target = {
    x: 50 + Math.random() * 260,
    y: 90 + Math.random() * 460,
    radius: 26 + Math.random() * 10,
  };
}

function endRun(reason) {
  state.running = false;
  cancelAnimationFrame(state.raf);
  state.best = Math.max(state.best, state.score);
  localStorage.setItem("${slug}:best", String(state.best));
  bestNode.textContent = state.best;
  statusNode.textContent = reason;
  button.textContent = "Start Run";
  hintNode.textContent = "Rewarded slot suggere: regarder une pub pour ${reward}.";
  draw();
}

function update(now) {
  if (now - state.tickTimer >= 1000) {
    state.timeLeft -= 1;
    state.tickTimer = now;
    if (state.timeLeft <= 0) {
      endRun("Time Up");
    }
  }
}

function draw() {
  ctx.fillStyle = "#0b1324";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "#22d3ee";
  ctx.font = "bold 22px Trebuchet MS";
  ctx.fillText("Temps: " + state.timeLeft, 20, 34);

  if (state.target) {
    ctx.beginPath();
    ctx.fillStyle = "#f97316";
    ctx.arc(state.target.x, state.target.y, state.target.radius, 0, Math.PI * 2);
    ctx.fill();
  }
}

function loop(now) {
  if (!state.running) {
    return;
  }
  update(now);
  draw();
  state.raf = requestAnimationFrame(loop);
}

draw();
"""
    ).substitute(slug=concept.slug, reward=concept.reward_type)


def survival_harvest_template(concept) -> str:
    return Template(
        """const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const scoreNode = document.getElementById("score");
const bestNode = document.getElementById("best");
const statusNode = document.getElementById("status");
const hintNode = document.getElementById("hint");
const button = document.getElementById("actionButton");

const state = {
  running: false,
  score: 0,
  best: Number(localStorage.getItem("${slug}:best") || 0),
  player: { x: 180, y: 320, size: 18 },
  pickups: [],
  hazard: { x: 40, y: 40, speed: 0.85 },
  raf: 0,
};

bestNode.textContent = state.best;
hintNode.textContent = "Glisse pour collecter et reste loin du danger.";

canvas.addEventListener("pointermove", (event) => {
  if (!state.running) {
    return;
  }
  const rect = canvas.getBoundingClientRect();
  state.player.x = ((event.clientX - rect.left) / rect.width) * canvas.width;
  state.player.y = ((event.clientY - rect.top) / rect.height) * canvas.height;
});

canvas.addEventListener("pointerdown", () => {
  if (!state.running) {
    startRun();
  }
});

button.addEventListener("click", () => {
  if (state.running) {
    endRun("Run aborted");
    return;
  }
  startRun();
});

function startRun() {
  state.running = true;
  state.score = 0;
  state.player = { x: 180, y: 320, size: 18 };
  state.pickups = [];
  state.hazard = { x: 40, y: 40, speed: 0.85 };
  scoreNode.textContent = state.score;
  statusNode.textContent = "Running";
  button.textContent = "Stop Run";
  for (let index = 0; index < 8; index += 1) spawnPickup();
  loop();
}

function spawnPickup() {
  state.pickups.push({
    x: 30 + Math.random() * 300,
    y: 60 + Math.random() * 520,
    size: 8 + Math.random() * 8,
  });
}

function endRun(reason) {
  state.running = false;
  cancelAnimationFrame(state.raf);
  state.best = Math.max(state.best, state.score);
  localStorage.setItem("${slug}:best", String(state.best));
  bestNode.textContent = state.best;
  statusNode.textContent = reason;
  button.textContent = "Start Run";
  hintNode.textContent = "Rewarded slot suggere: regarder une pub pour ${reward}.";
  draw();
}

function update() {
  const dx = state.player.x - state.hazard.x;
  const dy = state.player.y - state.hazard.y;
  const distance = Math.max(1, Math.hypot(dx, dy));
  state.hazard.x += (dx / distance) * state.hazard.speed;
  state.hazard.y += (dy / distance) * state.hazard.speed;
  state.hazard.speed += 0.0008;

  state.pickups = state.pickups.filter((pickup) => {
    const collected = Math.hypot(state.player.x - pickup.x, state.player.y - pickup.y) < state.player.size + pickup.size;
    if (collected) {
      state.score += 5;
      scoreNode.textContent = state.score;
      spawnPickup();
    }
    return !collected;
  });

  if (Math.hypot(state.player.x - state.hazard.x, state.player.y - state.hazard.y) < state.player.size + 18) {
    endRun("Caught");
  }
}

function draw() {
  ctx.fillStyle = "#0b1324";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  for (const pickup of state.pickups) {
    ctx.fillStyle = "#facc15";
    ctx.beginPath();
    ctx.arc(pickup.x, pickup.y, pickup.size, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.fillStyle = "#22d3ee";
  ctx.beginPath();
  ctx.arc(state.player.x, state.player.y, state.player.size, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#f97316";
  ctx.beginPath();
  ctx.arc(state.hazard.x, state.hazard.y, 18, 0, Math.PI * 2);
  ctx.fill();
}

function loop() {
  if (!state.running) {
    return;
  }
  update();
  draw();
  state.raf = requestAnimationFrame(loop);
}

draw();
"""
    ).substitute(slug=concept.slug, reward=concept.reward_type)
