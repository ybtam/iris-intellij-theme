# Contributing

## Development setup

Install Java 21, clone the repository, and run:

```bash
./gradlew buildPlugin
./gradlew verifyPlugin
./gradlew check
```

If the upstream palette changes, update `source/iris-palette.json` with a pinned commit and regenerate the theme resources:

```bash
python3 tools/import_t3code_palette.py --commit <commit> <themePalettes.ts> source/iris-palette.json
python3 tools/generate_theme.py
```

Keep upstream attribution in `THIRD-PARTY-NOTICES.md` current. Do not commit Marketplace tokens, signing keys, certificates, or passwords.

## Pull requests

- Explain user-visible theme changes.
- Run the Gradle build and plugin verification tasks.
- Keep generated resources synchronized with the source palette.
- Include screenshots for substantial visual changes when practical.
