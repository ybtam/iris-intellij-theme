#!/bin/sh
set -eu

root=$(git rev-parse --show-toplevel)
cd "$root"
if git config --get core.hooksPath >/dev/null 2>&1; then
    echo 'Hook installation stopped: core.hooksPath is configured. Integrate tools/pre-push into your existing hooks manually.' >&2
    exit 1
fi

hooks_dir=$(git rev-parse --git-path hooks)
mkdir -p "$hooks_dir"
hook="$hooks_dir/pre-push"
target="$root/tools/pre-push"
if [ -L "$hook" ] && [ "$(readlink "$hook")" = "$target" ]; then
    echo 'Pre-push hook is already installed.'
elif [ -e "$hook" ] || [ -L "$hook" ]; then
    echo "Hook installation stopped: $hook already exists. Integrate tools/pre-push manually." >&2
    exit 1
else
    ln -s "$target" "$hook"
    echo "Installed pre-push hook at $hook"
fi
