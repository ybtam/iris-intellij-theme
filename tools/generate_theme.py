#!/usr/bin/env python3
"""Generate IntelliJ theme JSON and editor schemes from the Iris palette."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
PALETTE = ROOT / "source" / "iris-palette.json"
THEMES = ROOT / "src" / "main" / "resources" / "themes"
SCHEMES = ROOT / "src" / "main" / "resources" / "editor-schemes"


def oklch_to_hex(value: str) -> str:
    """Convert a CSS OKLCH color to clamped sRGB hex."""
    parts = value.removeprefix("oklch(").removesuffix(")").split()
    if len(parts) != 3:
        raise ValueError(f"Unsupported OKLCH value: {value}")
    lightness, chroma, hue = map(float, parts)
    hue = math.radians(hue)
    a = chroma * math.cos(hue)
    b = chroma * math.sin(hue)

    l = lightness + 0.3963377774 * a + 0.2158037573 * b
    m = lightness - 0.1055613458 * a - 0.0638541728 * b
    s = lightness - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l**3, m**3, s**3

    red = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    green = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    blue = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s

    def to_srgb(channel: float) -> int:
        channel = max(0.0, min(1.0, channel))
        if channel <= 0.0031308:
            channel = 12.92 * channel
        else:
            channel = 1.055 * channel ** (1 / 2.4) - 0.055
        return round(channel * 255)

    return "#" + "".join(f"{to_srgb(channel):02X}" for channel in (red, green, blue))


def color_name(role: str) -> str:
    return "iris" + role[0].upper() + role[1:]


def palette_for(appearance: str) -> dict[str, str]:
    raw = json.loads(PALETTE.read_text(encoding="utf-8"))[appearance]
    return {role: oklch_to_hex(value) for role, value in raw.items()}


def ui_for(colors: dict[str, str]) -> dict[str, object]:
    def c(role: str) -> str:
        return color_name(role)

    return {
        "*": {
            "background": c("surface"),
            "foreground": c("text"),
        },
        "Panel.background": c("canvas"),
        "EditorPane.background": c("canvas"),
        "EditorTabs": {
            "background": c("chrome"),
            "selectedBackground": c("surfaceRaised"),
            "selectedForeground": c("accent"),
            "inactiveBackground": c("chrome"),
            "inactiveForeground": c("textMuted"),
            "underlineColor": c("accent"),
            "inactiveUnderlineColor": c("border"),
            "underlineHeight": 2,
        },
        "ToolWindow.background": c("surface"),
        "ToolWindow.Header.background": c("toolbar"),
        "ToolWindow.Header.borderColor": c("border"),
        "ToolWindow.HeaderTab.selectedBackground": c("surfaceRaised"),
        "ToolWindow.HeaderTab.selectedForeground": c("accent"),
        "ToolWindow.HeaderTab.inactiveBackground": c("toolbar"),
        "ToolWindow.HeaderTab.inactiveForeground": c("textMuted"),
        "TabbedPane.background": c("surface"),
        "TabbedPane.selectedBackground": c("surfaceRaised"),
        "TabbedPane.selectedForeground": c("accent"),
        "PopupPanel.background": c("surfaceOverlay"),
        "Popup.borderColor": c("border"),
        "Menu.background": c("surfaceOverlay"),
        "Menu.foreground": c("text"),
        "Menu.selectionBackground": c("accentSurface"),
        "Menu.selectionForeground": c("accentSurfaceForeground"),
        "List.background": c("surface"),
        "List.foreground": c("text"),
        "List.selectionBackground": c("accentSurface"),
        "List.selectionForeground": c("accentSurfaceForeground"),
        "Tree.background": c("surface"),
        "Tree.foreground": c("text"),
        "Tree.selectionBackground": c("accentSurface"),
        "Tree.selectionForeground": c("accentSurfaceForeground"),
        "TextField.background": c("input"),
        "TextField.foreground": c("text"),
        "TextField.placeholderForeground": c("placeholder"),
        "TextField.focusedBorderColor": c("focus"),
        "EditorSearchField.borderColor": c("border"),
        "Button.background": c("secondary"),
        "Button.foreground": c("secondaryForeground"),
        "Button.hoverBackground": c("toolbarControlHover"),
        "Button.focusedBorderColor": c("focus"),
        "CheckBox.background": c("surface"),
        "CheckBox.foreground": c("text"),
        "Label.foreground": c("text"),
        "Link.activeForeground": c("accent"),
        "Link.hoverForeground": c("accent"),
        "ProgressBar.background": c("muted"),
        "ProgressBar.foreground": c("accent"),
        "ProgressBar.indeterminateColor": c("accent"),
        "StatusBar.background": c("chrome"),
        "StatusBar.foreground": c("textMuted"),
        "StatusBar.borderColor": c("border"),
        "Notification.background": c("surfaceOverlay"),
        "Notification.borderColor": c("border"),
        "ScrollBar.thumbColor": c("terminalScrollbar"),
        "ScrollBar.thumbColorHover": c("terminalScrollbarHover"),
        "ScrollBar.trackColor": c("surface"),
        "ScrollBar.Mac.Transparent.thumbColor": c("terminalScrollbar"),
        "ScrollBar.Mac.Transparent.thumbColorHover": c("terminalScrollbarHover"),
        "SearchEverywhere.SearchField.background": c("input"),
        "SearchEverywhere.SearchField.borderColor": c("focus"),
        "SearchEverywhere.Header.background": c("toolbar"),
        "VersionControl.FileStatus.modified": c("warning"),
        "VersionControl.FileStatus.added": c("update"),
        "VersionControl.FileStatus.deleted": c("error"),
        "VersionControl.FileStatus.renamed": c("accent"),
        "VersionControl.FileStatus.ignored": c("textMuted"),
        "Debugger.exceptionLabelForeground": c("error"),
        "Debugger.breakpointForeground": c("error"),
        "Debugger.valueForeground": c("accent"),
        "Notification.errorBackground": c("errorSurface"),
        "Notification.warningBackground": c("warningSurface"),
    }


def theme_json(appearance: str, colors: dict[str, str]) -> dict[str, object]:
    prefix = "Iris Light" if appearance == "light" else "Iris Dark"
    return {
        "name": prefix,
        "dark": appearance == "dark",
        "author": "Yi Tam",
        "editorScheme": f"/editor-schemes/iris-{appearance}.icls",
        "colors": {color_name(role): value for role, value in colors.items()},
        "ui": ui_for(colors),
    }


def option(name: str, value: str | int | bool) -> str:
    return f'    <option name="{escape(name)}" value="{escape(str(value).lower() if isinstance(value, bool) else str(value))}" />'


def attribute(name: str, foreground: str, background: str, font_type: int = 0, *, effect: str | None = None) -> str:
    lines = [f'    <option name="{name}">', "      <value>"]
    lines.append(f'        <option name="FOREGROUND" value="{foreground.removeprefix("#")}" />')
    lines.append(f'        <option name="BACKGROUND" value="{background.removeprefix("#")}" />')
    lines.append(f'        <option name="FONT_TYPE" value="{font_type}" />')
    if effect:
        lines.append(f'        <option name="EFFECT_TYPE" value="{effect}" />')
        lines.append(f'        <option name="EFFECT_COLOR" value="{foreground.removeprefix("#")}" />')
    lines += ["      </value>", "    </option>"]
    return "\n".join(lines)


def editor_scheme(appearance: str, colors: dict[str, str]) -> str:
    background = colors["canvas"]
    surface = colors["surface"]
    text = colors["text"]
    muted = colors["textMuted"]
    accent = colors["accent"]
    secondary = colors["secondary"]
    focus = colors["focus"]
    error = colors["error"]
    warning = colors["warning"]
    update = colors["update"]
    message = colors["messageAction"]
    parent = "Default" if appearance == "light" else "Darcula"
    scheme_name = "Iris Light" if appearance == "light" else "Iris Dark"

    lines = [
        f'<scheme name="{scheme_name}" version="142" parent_scheme="{parent}">',
        option("LINE_SPACING", "1.0"),
        option("EDITOR_FONT_SIZE", 13),
        option("EDITOR_FONT_NAME", "JetBrains Mono"),
        option("CONSOLE_FONT_NAME", "JetBrains Mono"),
        option("EDITOR_LIGATURES", True),
        option("CONSOLE_LIGATURES", True),
        option("CONSOLE_LINE_SPACING", "1.0"),
        option("CONSOLE_FONT_SIZE", 13),
        option("CONSOLE_BOLD_FONT_NAME", "JetBrains Mono"),
        option("CONSOLE_ITALIC_FONT_NAME", "JetBrains Mono"),
        option("CONSOLE_BOLD_ITALIC_FONT_NAME", "JetBrains Mono"),
        option("EDITOR_CARET_ROW_COLOR", surface),
        option("CONSOLE_CARET_COLOR", focus),
        option("SELECTION_BACKGROUND", colors["accentSurface"]),
        option("SELECTION_FOREGROUND", colors["accentSurfaceForeground"]),
        option("CARET_COLOR", focus),
        option("RIGHT_MARGIN_COLOR", colors["border"]),
        option("INDENT_GUIDE_COLOR", colors["border"]),
        option("SELECTED_INDENT_GUIDE_COLOR", focus),
        option("WHITESPACES_COLOR", muted),
        option("GUTTER_BACKGROUND", surface),
        option("GUTTER_FOREGROUND", muted),
        option("LINE_NUMBERS_COLOR", muted),
        option("METHOD_SEPARATORS_COLOR", colors["border"]),
        option("TEARLINE_COLOR", colors["border"]),
        option("CONSOLE_BACKGROUND_KEY", colors["terminalBackground"]),
        option("CONSOLE_FOREGROUND_KEY", colors["terminalForeground"]),
        option("CONSOLE_SELECTION_BACKGROUND_KEY", colors["terminalSelection"]),
        option("CONSOLE_CARET_COLOR", colors["terminalCursor"]),
        option("CONSOLE_USER_INPUT_KEY", accent),
        option("CONSOLE_SYSTEM_OUTPUT_KEY", muted),
        option("CONSOLE_NORMAL_OUTPUT_KEY", text),
        option("CONSOLE_ERROR_OUTPUT_KEY", error),
        option("CONSOLE_LOG_WARNING_OUTPUT_KEY", warning),
        option("CONSOLE_LOG_ERROR_OUTPUT_KEY", error),
        option("CONSOLE_LOG_DEBUG_OUTPUT_KEY", message),
        option("CONSOLE_LOG_VERBOSE_OUTPUT_KEY", muted),
        option("BREADCRUMBS_CURRENT", text),
        option("BREADCRUMBS_DEFAULT", muted),
        option("BREADCRUMBS_HOVERED", accent),
        option("BREADCRUMBS_INACTIVE", muted),
        "  <attributes>",
    ]

    attrs = [
        ("TEXT", text, background, 0),
        ("DEFAULT_IDENTIFIER", text, background, 0),
        ("LINE_COMMENT", muted, background, 2),
        ("BLOCK_COMMENT", muted, background, 2),
        ("DOC_COMMENT", muted, background, 2),
        ("STRING", update, background, 0),
        ("VALID_STRING_ESCAPE", accent, background, 1),
        ("INVALID_STRING_ESCAPE", error, background, 1, "1"),
        ("NUMBER", message, background, 0),
        ("KEYWORD", accent, background, 1),
        ("FUNCTION_DECLARATION", accent, background, 1),
        ("FUNCTION_CALL", text, background, 0),
        ("METHOD_CALL", text, background, 0),
        ("PARAMETER", secondary, background, 0),
        ("LOCAL_VARIABLE", text, background, 0),
        ("INSTANCE_FIELD", colors["secondaryLabel"], background, 0),
        ("STATIC_FIELD", message, background, 0),
        ("CLASS_NAME", update, background, 1),
        ("INTERFACE_NAME", update, background, 1),
        ("ENUM_NAME", update, background, 1),
        ("TYPE_PARAMETER", update, background, 0),
        ("CONSTANT", message, background, 1),
        ("PREDEFINED_SYMBOL", accent, background, 0),
        ("METADATA", colors["secondaryForeground"], background, 2),
        ("ANNOTATION", message, background, 0),
        ("REGEXP", message, background, 0),
        ("MARKUP_TAG", accent, background, 1),
        ("MARKUP_ATTRIBUTE", secondary, background, 0),
        ("MARKUP_ENTITY", message, background, 0),
        ("TEMPLATE_LANGUAGE_COLOR", accent, background, 0),
        ("LABEL", accent, background, 0),
        ("OPERATION_SIGN", accent, background, 0),
        ("LOGIC_OPERATION_SIGN", accent, background, 0),
        ("BRACES", text, background, 0),
        ("BRACKETS", text, background, 0),
        ("PARENTHESES", text, background, 0),
        ("COMMA", muted, background, 0),
        ("DOT", muted, background, 0),
        ("SEMICOLON", muted, background, 0),
        ("TODO_DEFAULT", warning, background, 1),
        ("ERRORS_ATTRIBUTES", error, background, 0, "1"),
        ("WARNING_ATTRIBUTES", warning, background, 0, "1"),
        ("DEPRECATED_SYMBOL", muted, background, 0, "4"),
        ("BAD_CHARACTER", error, background, 1, "1"),
        ("SEARCH_RESULT", text, colors["accentSurface"], 0),
        ("TEXT_SEARCH_RESULT", text, colors["accentSurface"], 0),
        ("MATCHED_BRACE", text, colors["accentSurface"], 1),
        ("UNMATCHED_BRACE", error, colors["errorSurface"], 1),
        ("IDENTIFIER_UNDER_CARET", text, colors["accentSurface"], 0),
    ]
    for item in attrs:
        if len(item) == 5:
            lines.append(attribute(*item[:4], effect=item[4]))
        else:
            lines.append(attribute(*item))
    lines += ["  </attributes>", "</scheme>", ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="only validate source palette")
    args = parser.parse_args()
    for appearance in ("light", "dark"):
        colors = palette_for(appearance)
        if len(colors) != 57:
            raise SystemExit(f"{appearance} palette has {len(colors)} roles, expected 57")
        if args.check:
            print(f"{appearance}: {len(colors)} roles; {len(set(colors.values()))} rendered colors")
            continue
        (THEMES / f"iris-{appearance}.theme.json").write_text(
            json.dumps(theme_json(appearance, colors), indent=2) + "\n", encoding="utf-8"
        )
        (SCHEMES / f"iris-{appearance}.icls").write_text(
            editor_scheme(appearance, colors), encoding="utf-8"
        )
        print(f"Generated Iris {appearance} theme and editor scheme")


if __name__ == "__main__":
    main()
