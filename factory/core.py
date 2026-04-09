from __future__ import annotations

import json
import math
import random
import textwrap
from hashlib import sha256
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from factory.templates import render_batch_files, render_prototype, render_text_files


DEFAULT_STRATEGY = {
    "portfolio_name": "casual-scale",
    "mechanics": ["lane-dodge", "tap-burst", "survival-harvest"],
    "themes": [
        "space salvage",
        "ocean rescue",
        "neon courier",
        "jungle relic",
        "snow sprint",
        "desert convoy",
        "sky garden",
        "factory escape",
    ],
    "meta_loops": [
        "unlockable skins",
        "daily missions",
        "streak rewards",
        "world progression",
    ],
    "art_styles": [
        "clean flat arcade",
        "bold toy-like shapes",
        "retro neon panels",
        "soft paper-cut layers",
    ],
    "reward_types": [
        "extra life",
        "score booster",
        "double coins",
        "shield charge",
    ],
    "interstitial_cadence": "after every 3 runs",
}


MECHANIC_DESCRIPTIONS = {
    "lane-dodge": "Le joueur change de voie pour eviter des obstacles, survivre et faire monter le score.",
    "tap-burst": "Le joueur tape rapidement des cibles ou fenetres de timing pour construire un combo.",
    "survival-harvest": "Le joueur collecte des ressources tout en evitant un danger croissant.",
}


TAGLINES = {
    "lane-dodge": "Un run ultra lisible, une decision par seconde.",
    "tap-burst": "Du rythme, du timing et une boucle de revanche immediate.",
    "survival-harvest": "Une tension douce entre collecte et survie.",
}


@dataclass(frozen=True)
class AppConcept:
    name: str
    slug: str
    mechanic: str
    theme: str
    meta_loop: str
    art_style: str
    reward_type: str
    interstitial_cadence: str
    core_hook: str
    differentiator: str
    policy_notes: list[str]
    score: float

    def to_dict(self) -> dict:
        return asdict(self)


def slugify(value: str) -> str:
    cleaned = "".join(char.lower() if char.isalnum() else "-" for char in value)
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-")


def load_strategy(path: str | None) -> dict:
    if not path:
        return DEFAULT_STRATEGY
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    merged = DEFAULT_STRATEGY | payload
    for key in ("mechanics", "themes", "meta_loops", "art_styles", "reward_types"):
        if key in payload:
            merged[key] = payload[key]
    return merged


def build_candidates(strategy: dict) -> list[AppConcept]:
    candidates: list[AppConcept] = []
    for mechanic in strategy["mechanics"]:
        for theme in strategy["themes"]:
            for meta_loop in strategy["meta_loops"]:
                art_style = pick_deterministic(theme + mechanic, strategy["art_styles"])
                reward_type = pick_deterministic(theme + meta_loop, strategy["reward_types"])
                name = build_name(theme, mechanic)
                slug = slugify(name)
                differentiator = describe_differentiator(mechanic, theme, meta_loop)
                policy_notes = policy_notes_for(
                    reward_type=reward_type,
                    interstitial_cadence=strategy["interstitial_cadence"],
                )
                score = base_score(mechanic, meta_loop, theme)
                candidates.append(
                    AppConcept(
                        name=name,
                        slug=slug,
                        mechanic=mechanic,
                        theme=theme,
                        meta_loop=meta_loop,
                        art_style=art_style,
                        reward_type=reward_type,
                        interstitial_cadence=strategy["interstitial_cadence"],
                        core_hook=TAGLINES[mechanic],
                        differentiator=differentiator,
                        policy_notes=policy_notes,
                        score=score,
                    )
                )
    return dedupe_by_slug(candidates)


def pick_batch(candidates: list[AppConcept], count: int, seed: int = 7) -> list[AppConcept]:
    rng = random.Random(seed)
    pool = candidates[:]
    rng.shuffle(pool)
    selected: list[AppConcept] = []

    mechanics = list({item.mechanic for item in pool})
    mechanic_cap = max(1, math.ceil(count / max(1, len(mechanics))))
    rng.shuffle(mechanics)
    for mechanic in mechanics:
        if len(selected) >= count:
            break
        mechanic_pool = [item for item in pool if item.mechanic == mechanic]
        if not mechanic_pool:
            continue
        best = max(mechanic_pool, key=lambda candidate: candidate.score + diversity_bonus(candidate, selected))
        selected.append(best)
        pool.remove(best)

    while pool and len(selected) < count:
        capped_pool = [
            item
            for item in pool
            if sum(1 for selected_item in selected if selected_item.mechanic == item.mechanic) < mechanic_cap
        ]
        source_pool = capped_pool or pool
        best = max(source_pool, key=lambda candidate: candidate.score + diversity_bonus(candidate, selected))
        selected.append(best)
        pool.remove(best)
    return selected


def diversity_bonus(candidate: AppConcept, selected: list[AppConcept]) -> float:
    if not selected:
        return 5.0
    bonus = 0.0
    if candidate.mechanic not in {item.mechanic for item in selected}:
        bonus += 3.0
    if candidate.theme not in {item.theme for item in selected}:
        bonus += 2.5
    if candidate.meta_loop not in {item.meta_loop for item in selected}:
        bonus += 1.5
    if candidate.art_style not in {item.art_style for item in selected}:
        bonus += 1.0
    return bonus


def build_name(theme: str, mechanic: str) -> str:
    nouns = {
        "lane-dodge": "Dash",
        "tap-burst": "Beat",
        "survival-harvest": "Gather",
    }
    return f"{theme.title()} {nouns[mechanic]}"


def describe_differentiator(mechanic: str, theme: str, meta_loop: str) -> str:
    return (
        f"{MECHANIC_DESCRIPTIONS[mechanic]} "
        f"Le theme '{theme}' pilote la presentation, et la retention repose sur {meta_loop}."
    )


def policy_notes_for(reward_type: str, interstitial_cadence: str) -> list[str]:
    return [
        f"Rewarded ad possible uniquement sur opt-in clair pour offrir '{reward_type}'.",
        f"Interstitial uniquement {interstitial_cadence}, jamais au debut d'une partie ou d'un niveau.",
        "Ne jamais promettre d'argent reel, de crypto, ou de recompense transferable.",
    ]


def base_score(mechanic: str, meta_loop: str, theme: str) -> float:
    score = 50.0
    if mechanic == "lane-dodge":
        score += 5.0
    if meta_loop == "daily missions":
        score += 4.0
    if "space" in theme or "neon" in theme:
        score += 2.0
    return score


def dedupe_by_slug(candidates: Iterable[AppConcept]) -> list[AppConcept]:
    seen: set[str] = set()
    unique: list[AppConcept] = []
    for candidate in candidates:
        if candidate.slug in seen:
            continue
        seen.add(candidate.slug)
        unique.append(candidate)
    return unique


def write_batch(output_dir: str | Path, batch: list[AppConcept]) -> Path:
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)

    manifest = {
        "count": len(batch),
        "mechanic_distribution": Counter(item.mechanic for item in batch),
        "theme_distribution": Counter(item.theme for item in batch),
        "apps": [item.to_dict() for item in batch],
    }
    (root / "batch.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    for relative_path, content in render_batch_files(batch).items():
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    for concept in batch:
        app_root = root / concept.slug
        app_root.mkdir(parents=True, exist_ok=True)
        write_app(app_root, concept)
    return root


def write_app(app_root: Path, concept: AppConcept) -> None:
    (app_root / "brief.json").write_text(
        json.dumps(concept.to_dict(), indent=2),
        encoding="utf-8",
    )

    for relative_path, content in render_text_files(concept).items():
        target = app_root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    for relative_path, content in render_prototype(concept).items():
        target = app_root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def batch_summary(batch: list[AppConcept]) -> str:
    mechanics = Counter(item.mechanic for item in batch)
    themes = ", ".join(item.theme for item in batch[:5])
    return "\n".join(
        [
            f"Apps generees: {len(batch)}",
            f"Mechanics: {dict(mechanics)}",
            f"Themes echantillon: {themes}",
        ]
    )


def portfolio_warning() -> str:
    return textwrap.dedent(
        """
        Attention: cette factory aide a scaler un portefeuille, pas a contourner les policies.
        Avant publication massive, verifie au minimum :
        - unicite reelle de la boucle de jeu et de la presentation
        - qualite et stabilite de l'experience
        - rythme pub non intrusif
        - tests Play Console pour les comptes personnels recents
        """
    ).strip()


def pick_deterministic(seed_text: str, options: list[str]) -> str:
    digest = sha256(seed_text.encode("utf-8")).hexdigest()
    index = int(digest[:8], 16) % len(options)
    return options[index]
