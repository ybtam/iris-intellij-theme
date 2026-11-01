# Contributing

## Development setup

Install Java 21 and Python 3.9 or newer, clone the repository, and install the pre-push hook:

```bash
./tools/install-hooks.sh
```

Run this once per clone; it is safe to repeat. The installer preserves existing hooks and refuses a configured `core.hooksPath`. If you use custom hooks, integrate `tools/pre-push` into your existing pre-push hook manually. If you move the clone, remove its stale project hook symlink yourself before reinstalling.

The hook checks that generated theme resources match the palette and runs `./gradlew buildPlugin`. Both checks must pass for the push to continue. It checks the working tree, so uncommitted changes affect the result. Gradle may download the wrapper and IntelliJ Platform dependencies and writes build outputs and caches. If generated resources are out of date, run `python3 tools/generate_theme.py` and review the resulting changes.

Run the full local checks as well:

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
