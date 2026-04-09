from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from factory.core import AppConcept


CAPACITOR_VERSION = "^8.0.0"


def discover_app_dirs(source: str | Path) -> list[Path]:
    root = Path(source)
    if (root / "brief.json").exists():
        return [root]
    if (root / "batch.json").exists():
        return sorted(path for path in root.iterdir() if path.is_dir() and (path / "brief.json").exists())
    raise FileNotFoundError(f"Could not find app source or batch manifest in {root}")


def load_concept(app_dir: str | Path) -> AppConcept:
    payload = json.loads((Path(app_dir) / "brief.json").read_text(encoding="utf-8"))
    return AppConcept(**payload)


def androidize_source(
    source: str | Path,
    output_dir: str | Path,
    package_prefix: str = "com.agentichub",
    capacitor_version: str = CAPACITOR_VERSION,
) -> Path:
    source_root = Path(source)
    app_dirs = discover_app_dirs(source_root)
    export_root = Path(output_dir)
    export_root.mkdir(parents=True, exist_ok=True)

    manifest_apps = []
    for app_dir in app_dirs:
        concept = load_concept(app_dir)
        package_id = build_package_id(package_prefix, concept.slug)
        target_dir = export_root / concept.slug
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(app_dir, target_dir)
        write_android_files(target_dir, concept, package_id, capacitor_version)
        manifest_apps.append(
            {
                "name": concept.name,
                "slug": concept.slug,
                "packageId": package_id,
                "path": str(target_dir),
            }
        )

    (export_root / "android-batch.json").write_text(
        json.dumps(
            {
                "source": str(source_root),
                "count": len(manifest_apps),
                "packagePrefix": package_prefix,
                "apps": manifest_apps,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return export_root


def write_android_files(app_root: Path, concept: AppConcept, package_id: str, capacitor_version: str) -> None:
    files = render_android_files(concept, package_id, capacitor_version)
    for relative_path, content in files.items():
        target = app_root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def build_package_id(package_prefix: str, slug: str) -> str:
    sanitized_prefix = ".".join(_sanitize_package_segment(segment) for segment in package_prefix.split(".") if segment)
    leaf = _sanitize_package_segment(slug.replace("-", ""))
    return f"{sanitized_prefix}.{leaf}"


def _sanitize_package_segment(value: str) -> str:
    lowered = re.sub(r"[^a-zA-Z0-9_]", "", value.lower())
    if not lowered:
        lowered = "app"
    if lowered[0].isdigit():
        lowered = f"app{lowered}"
    return lowered


def render_android_files(concept: AppConcept, package_id: str, capacitor_version: str) -> dict[str, str]:
    short_description = f"{concept.core_hook} Releve le defi dans un univers {concept.theme}."
    long_description = (
        f"{concept.name} est un jeu casual mobile base sur {concept.mechanic}. "
        f"Chaque run est court, lisible et pousse a rejouer via {concept.meta_loop}. "
        f"La monétisation cible d'abord les rewarded ads, avec un rythme interstitial prudent."
    )

    package_json = {
        "name": f"mobile-{concept.slug}",
        "private": True,
        "version": "0.1.0",
        "description": f"Android wrapper for {concept.name}",
        "scripts": {
            "cap:add:android": "npx cap add android",
            "cap:sync": "npx cap sync android",
            "cap:open:android": "npx cap open android",
            "doctor": "npx cap doctor",
        },
        "dependencies": {
            "@capacitor/core": capacitor_version,
        },
        "devDependencies": {
            "@capacitor/android": capacitor_version,
            "@capacitor/cli": capacitor_version,
        },
    }

    capacitor_config = {
        "appId": package_id,
        "appName": concept.name,
        "webDir": "web",
        "bundledWebRuntime": False,
    }

    metadata = {
        "applicationId": package_id,
        "versionCode": 1,
        "versionName": "0.1.0",
        "playStoreCategory": "GAME_CASUAL",
        "adsPrimaryFormat": "rewarded",
        "adsSecondaryFormat": "interstitial",
    }

    return {
        "package.json": json.dumps(package_json, indent=2) + "\n",
        "capacitor.config.json": json.dumps(capacitor_config, indent=2) + "\n",
        ".gitignore": "node_modules/\nandroid/\n",
        "mobile/android-config.json": json.dumps(metadata, indent=2) + "\n",
        "docs/android-release.md": render_android_release_doc(concept, package_id),
        "docs/admob-integration.md": render_admob_doc(concept),
        "docs/play-store-checklist.md": render_play_store_doc(concept, package_id),
        "fastlane/metadata/android/en-US/title.txt": concept.name + "\n",
        "fastlane/metadata/android/en-US/short_description.txt": short_description + "\n",
        "fastlane/metadata/android/en-US/full_description.txt": long_description + "\n",
        "fastlane/metadata/android/en-US/changelogs/default.txt": "Initial Android packaging scaffold.\n",
    }


def render_android_release_doc(concept: AppConcept, package_id: str) -> str:
    return f"""# Android Release

## Package identity

- App name: `{concept.name}`
- Package id: `{package_id}`
- Web assets directory: `web/`

## Capacitor bootstrap

1. `npm install`
2. `npm run cap:add:android`
3. `npm run cap:sync`
4. `npm run cap:open:android`

## Android Studio release path

1. Open the generated Android project in Android Studio.
2. Configure signing for release.
3. Build a signed Android App Bundle (`.aab`).
4. Upload the bundle to Google Play Console.

## Notes

- This wrapper assumes the generated web prototype stays in `web/`.
- Add native plugins only after the loop and UI are validated.
- Keep the first release minimal and policy-safe.
"""


def render_admob_doc(concept: AppConcept) -> str:
    return f"""# AdMob Integration

## Recommended order

1. Validate retention before monetisation.
2. Add consent flow for ads.
3. Integrate rewarded ads first.
4. Add interstitials only after UX review.

## Placements for this app

- Rewarded offer for `{concept.reward_type}`
- Interstitial cadence: `{concept.interstitial_cadence}`

## Implementation checklist

- Add AdMob app and ad unit ids
- Integrate consent update on launch
- Use test ads during development
- Track rewarded opt-in rate
- Track retention impact after ads rollout

## Policy reminders

- No surprise ads at the start of a run
- No fake close buttons
- No rewards convertible to real-world money
"""


def render_play_store_doc(concept: AppConcept, package_id: str) -> str:
    return f"""# Play Store Checklist

## Identity

- Title: `{concept.name}`
- Package id: `{package_id}`
- Category: Casual game

## Store assets

- Icon
- Feature graphic
- Minimum 4 screenshots
- Short description
- Full description

## Pre-launch

- Closed testing configured
- App content questionnaire completed
- Ads disclosure reviewed
- Privacy policy URL ready
- Play App Signing enabled

## Release flow

1. Build signed `.aab`
2. Upload to internal or closed testing
3. Resolve crashes and policy issues
4. Promote to production when metrics are acceptable
"""
