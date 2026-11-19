#!/bin/sh
# Run host and desktop tests, or build and check Kindle package candidates.
set -eu
root=$(cd "$(dirname "$0")/.." && pwd)
output=${1:?usage: scripts/simulate.sh OUTPUT_DIR [--packages|--armel-packages]}
mode=${2:-}
case "$mode" in
    ""|--packages|--armel-packages) ;;
    *) echo "Unknown option: $mode" >&2; exit 2 ;;
esac
mkdir -p "$output"
output=$(cd "$output" && pwd)
mkdir -p "$output/logs" "$output/previews" "$output/documents" "$output/packages"
export CARGO_INCREMENTAL=0
export CARGO_PROFILE_DEV_STRIP=none CARGO_PROFILE_TEST_STRIP=none
build=$root/doannt-kindle-build/scripts/package.py

run() {
    name=$1
    shift
    set +e
    (set -e; "$@") >"$output/logs/$name.log" 2>&1
    result=$?
    set -e
    if [ "$result" -ne 0 ]; then
        cat "$output/logs/$name.log" >&2
        return "$result"
    fi
    printf 'Passed %s\n' "$name"
}

native_settings() {
    export CARGO_TARGET_DIR=${CARGO_TARGET_DIR:-"${TMPDIR:-/tmp}/primitive-native-target"}
    export CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0
}

host_tests() (
    case "$1" in tools|launcher|store|terminal|browser) ;; *) native_settings ;; esac
    cd "$root/doannt-kindle-$1"
    cargo test --offline --locked --workspace
)

schema() {
    cd "$root"
    python3 schema/scripts/validate.py schema/examples/*.json
}

catalog() {
    cd "$root/doannt-kindle-catalog"
    sh scripts/test.sh
}

launcher_preview() {
    cd "$root/doannt-kindle-launcher"
    cargo run --offline --locked -q -p kl-desktop -- --documents "$output/documents" --out "$output/previews/launcher"
}

browser_preview() (
    cd "$root/doannt-kindle-browser"
    mkdir -p "$output/previews/browser" "$output/browser-data"
    export KB_DATA="$output/browser-data" KB_SHOTS="$output/previews/browser" KB_OUT="$output/previews/browser/current.png"
    printf 'shot home\nquit\n' | cargo run --offline --locked -q -p kb-desktop -- kbp://home
)

terminal_preview() (
    cd "$root/doannt-kindle-terminal"
    printf 'type echo Primitive Terminal simulation\ngo\nwait 250\nshot terminal\nquit\n' |
        cargo run --offline --locked -q -p kt-desktop -- --out "$output/previews/terminal"
)

launcher_shell() {
    cd "$root/doannt-kindle-launcher"
    for test in tests/*-test.sh; do
        sh "$test"
    done
}

native_preview() (
    native_settings
    cd "$root/doannt-kindle-$1"
    cargo run --offline --locked -q -p "$2-desktop" -- "$output/previews/$2"
)

package() (
    dir=$1
    id=$2
    module=$3
    crate=$4
    install_file=$5
    docs_license=$6
    arch=${7:-armhf}
    case "$arch" in
        armhf) target=armv7-unknown-linux-musleabihf ;;
        armel) target=armv7-unknown-linux-musleabi ;;
        *) echo "Unsupported package architecture: $arch" >&2; exit 1 ;;
    esac
    cd "$root/doannt-kindle-$dir"
    case "$dir" in
        launcher|store|browser|terminal) ;;
        *) native_settings ;;
    esac
    cargo zigbuild --offline --locked --release -p "$crate" --target "$target"
    version=$(cargo metadata --offline --locked --no-deps --format-version 1 |
        python3 -c 'import json, sys; print(next(p["version"] for p in json.load(sys.stdin)["packages"] if p["name"] == sys.argv[1]))' "$crate")
    sh scripts/stage.sh "$arch"
    set --
    if [ -n "$docs_license" ]; then set -- --docs-license "$docs_license"; fi
    python3 "$build" --id "$id" --dir "$module" --version "$version" --arch "$arch" \
        --stage build/stage --license LICENSE "$@" --install "$install_file" --out "$output/packages/$id"
    find "$output/packages/$id" -name "*-$arch.zip" -type f | sort | tail -n 1
)

verify_package_archives() {
    cd "$root"
    python3 scripts/verify-local-packages.py "$output/packages"
    find "$output/packages" -name '*.zip' -type f | while IFS= read -r archive; do
        (cd "$root/doannt-kindle-tools" &&
            KL_TEST_PACKAGE="$archive" cargo test --offline --locked -p kl-store accepts_a_package_from_the_build_packager)
    done
}

verify_packages() {
    verify_package_archives
    store=$(find "$output/packages/primitive-store" -name '*.zip' -type f | sort | tail -n 1)
    (cd "$root/doannt-kindle-launcher" &&
        KL_STORE_BOOTSTRAP_PACKAGE="$store" cargo test --offline --locked -p kl-launcher bootstrap_installs_the_staged_store_archive)
}

if [ "$mode" = --armel-packages ]; then
    run package-launcher-armel package launcher primitive-launcher launcher kl-launcher docs/INSTALL.md LICENSE-DOCS armel
    run package-browser-armel package browser primitive-browser browser kb-kindle docs/INSTALL.md LICENSE-DOCS armel
    run package-terminal-armel package terminal primitive-terminal terminal kt-kindle INSTALL.md "" armel
    run package-verification-armel verify_package_archives
    printf 'Simulation output: %s\n' "$output"
    exit
fi

run schema schema
run catalog catalog
for repo in tools launcher store terminal browser; do
    run "$repo-tests" host_tests "$repo"
done
run launcher-shell launcher_shell
run launcher-preview launcher_preview
run browser-preview browser_preview
run terminal-preview terminal_preview

native_apps="app-template:hello notes:notes words:words focus:focus calculator:calculator sudoku:sudoku minesweeper:minesweeper crossword:crossword blocks:blocks ships:ships cards:cards chess:chess solitaire:solitaire cascade:cascade"
for pair in $native_apps; do
    repo=${pair%:*}
    app=${pair#*:}
    [ -f "$root/doannt-kindle-$repo/Cargo.lock" ] || { echo "Missing app checkout: doannt-kindle-$repo" >&2; exit 1; }
    run "$app-tests" host_tests "$repo"
    run "$app-preview" native_preview "$repo" "$app"
done

if [ "$mode" = --packages ]; then
    run package-launcher package launcher primitive-launcher launcher kl-launcher docs/INSTALL.md LICENSE-DOCS
    run package-store package store primitive-store store store-app INSTALL.md ""
    run package-browser package browser primitive-browser browser kb-kindle docs/INSTALL.md LICENSE-DOCS
    run package-terminal package terminal primitive-terminal terminal kt-kindle INSTALL.md ""
    for pair in $native_apps; do
        repo=${pair%:*}
        app=${pair#*:}
        run "package-$app" package "$repo" "primitive-$app" "$app" "$app-kindle" INSTALL.md LICENSE-DOCS
    done
    run package-verification verify_packages
fi
printf 'Simulation output: %s\n' "$output"
