# App Factory

Cette base pose une V1 d'agent local pour industrialiser la creation d'apps casual mobiles sans tomber dans une simple usine a clones.

Le systeme fait trois choses :

- genere des concepts d'apps avec des variations substantielles
- applique des garde-fous de risque avant generation
- scaffold des dossiers d'apps avec prototype web, docs store et plan de monetisation
- prepare aussi un handoff Figma et une structure GitHub par app
- peut convertir un batch genere en scaffold Android-ready via Capacitor

## Pourquoi cette approche

Scaler vers 100 apps peut marcher uniquement si on scale :

- un moteur commun
- des boucles de jeu distinctes
- des themes et economies differencies
- une verification produit/policy stricte

Google Play sanctionne le contenu repetitif ou de faible valeur. Cette factory vise donc un portefeuille de variantes significatives, pas des copies recolorees.

## Ce que la V1 genere

Pour chaque app :

- `brief.json` : fiche machine-readable de l'app
- `README.md` : resume produit et etat de la generation
- `docs/game-design.md` : boucle de jeu et retention
- `docs/store-listing.md` : base de fiche Play Store
- `docs/ads-plan.md` : plan rewarded/interstitial prudent
- `docs/figma-handoff.md` : ecrans, composants et tokens a produire
- `docs/github-backlog.md` : milestones, labels et issues a ouvrir
- `docs/code-connect-targets.json` : cibles de mapping code/design
- `.github/` : templates minimaux pour lancer un repo par app
- `web/` : prototype HTML/CSS/JS mobile-first

Apres export Android :

- `package.json`
- `capacitor.config.json`
- `mobile/android-config.json`
- `docs/android-release.md`
- `docs/admob-integration.md`
- `docs/play-store-checklist.md`
- `fastlane/metadata/android/en-US/*`

Au niveau du batch :

- `portfolio/github-repo-plan.md`
- `portfolio/figma-batch-handoff.md`
- `android-batch.json`

## Quick start

```bash
python -m factory.cli batch --count 5
```

Le batch sera ecrit dans `generated/`.

Pour choisir un autre dossier :

```bash
python -m factory.cli batch --count 10 --output output
```

Pour changer la strategie :

```bash
python -m factory.cli batch --count 8 --strategy strategies/casual_scale.json
```

Verification locale simple :

```bash
python -m unittest discover -s tests
```

Export Android d'un batch deja genere :

```bash
python -m factory.cli androidize --source generated_v4 --output android_exports
```

Puis, dans une app exportee :

```bash
npm install
npm run cap:add:android
npm run cap:sync
npm run cap:open:android
```

## Philosophie de scaling

Ne pas essayer de publier 100 apps d'un coup. Le bon rythme est :

1. Generer 20 concepts.
2. En retenir 3 a 5 avec une bonne diversite.
3. Prototype rapide.
4. Test de retention.
5. Ajouter la monetisation seulement apres verification UX.
6. Industrialiser le pipeline gagnant.

## Brancher d'autres outils ensuite

Les plugins les plus utiles ensuite seront :

- `GitHub` pour piloter plusieurs repos et PRs
- `Figma` ou `Canva` pour produire des themes/assets plus distinctifs
- `Google Drive` pour centraliser briefs, assets et matrices de test

## Etat des integrations

- `GitHub` : exploitable pour brancher des repos reels quand tu me donnes un owner/repo
- `Figma` : le programme sort deja les handoffs et cibles Code Connect; si tu me donnes un file key ou une URL Figma, je pourrai travailler dans le fichier

## Capacitor et release

Le scaffold Android utilise Capacitor pour emballer directement le prototype web existant. L'inference ici est volontaire : pour scaler vite sur Android avec des jeux casual simples, cette voie est nettement plus rapide qu'une pile mobile native separee par app.

## Sources officielles a garder en tete

- Google Play interdit le contenu repetitif ou de faible valeur : https://support.google.com/googleplay/android-developer/answer/16070163
- Les nouveaux comptes personnels ont des exigences de test avant production : https://support.google.com/googleplay/android-developer/answer/6112435?hl=en
- AdMob rewarded ads Android : https://developers.google.com/admob/android/next-gen/rewarded
- Les ads ne doivent pas interrompre l'action de facon inattendue : https://support.google.com/googleplay/android-developer/answer/16810878
