# Iris Theme for JetBrains IDEs

A complete light and dark IntelliJ Platform theme based on the [Iris palette from T3 Code](https://github.com/pingdotgg/t3code/blob/d07ffbe351a10e1001f6d8eafa5b7533b8bd7e23/packages/shared/src/themePalettes.ts).

Iris includes matching UI themes and editor schemes for WebStorm and other JetBrains IDEs:

- Iris Light and Iris Dark
- Editor, console, terminal, gutter, caret, selection, and indentation colors
- Syntax highlighting for common language constructs
- Tabs, tool windows, popups, menus, lists, trees, inputs, buttons, notifications, and status bars
- Version-control, debugger, warning, error, and update colors
- Custom Iris plugin icon
- Reproducible palette import and theme generation scripts

This plugin is independent and is not affiliated with T3 Tools or JetBrains.

## Install

### JetBrains Marketplace

The Marketplace listing will be linked here after the first public release is approved.

### Install from disk

1. Download the ZIP from [GitHub Releases](https://github.com/ybtam/iris-intellij-theme/releases).
2. In WebStorm, open **Settings/Preferences → Plugins**.
3. Select the gear icon → **Install Plugin from Disk…**.
4. Choose the downloaded ZIP and restart WebStorm if prompted.
5. Select **Settings/Preferences → Appearance & Behavior → Appearance → Theme** and choose **Iris Light** or **Iris Dark**.

## Build locally

Requirements: Java 21 and a network connection for the IntelliJ Platform dependency.

```bash
./gradlew buildPlugin
./gradlew verifyPlugin
./gradlew check
```

The installable ZIP is written to `build/distributions/`.

The generated theme files are derived from the checked-in palette snapshot:

```bash
python3 tools/generate_theme.py --check
python3 -m json.tool source/iris-palette.json >/dev/null
```

To refresh the snapshot from an upstream checkout, pin the exact commit:

```bash
python3 tools/import_t3code_palette.py \
  --commit d07ffbe351a10e1001f6d8eafa5b7533b8bd7e23 \
  /path/to/themePalettes.ts \
  source/iris-palette.json
python3 tools/generate_theme.py
```

The source palette uses CSS OKLCH. The generator converts it to clamped sRGB hex values because IntelliJ theme resources use RGB color values.

## Publish to JetBrains Marketplace

Publishing requires a JetBrains Marketplace account, a Marketplace publishing token, and a signing certificate. The repository never stores these values.

Create the following environment variables in the local shell or CI secret store:

- `PUBLISH_TOKEN`
- `CERTIFICATE_CHAIN` — base64-encoded certificate chain
- `PRIVATE_KEY` — base64-encoded private key
- `PRIVATE_KEY_PASSWORD`

Then run:

```bash
./gradlew signPlugin
./gradlew publishPlugin
```

The official instructions are in the [JetBrains plugin publishing documentation](https://plugins.jetbrains.com/docs/intellij/publishing-plugin.html) and [plugin signing documentation](https://plugins.jetbrains.com/docs/intellij/plugin-signing.html).

The included GitHub Actions release workflow publishes only when a GitHub release is created and the four secrets above have been configured. It does not expose or commit credentials.

## Attribution and license

The Iris palette is derived from `themePalettes.ts` in [pingdotgg/t3code](https://github.com/pingdotgg/t3code), pinned to commit `d07ffbe351a10e1001f6d8eafa5b7533b8bd7e23`, and used under its MIT License. See [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

The plugin source and original assets are available under the MIT License; see [LICENSE](LICENSE).
