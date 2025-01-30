default:
  @just --list


# init local dev environment
[group('dev')]
sync:
    uv sync


# add news item of type
[group('dev')]
news type id *msg:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ "{{id}}" = "-" ]; then
      id=`git rev-parse --abbrev-ref HEAD | cut -d- -f1`
    else
      id="{{id}}"
    fi
    if [ "{{msg}}" = "" ]; then
      msg=`git rev-parse --abbrev-ref HEAD | sed 's/^[0-9][0-9]*-//' | uv run caseutil -csentence`
    fi
    uv run towncrier create -c "{{msg}}" "$id.{{type}}.md"


# run linters
[group('dev')]
lint:
    uv run mypy .
    uv run ruff check
    uv run ruff format --check


# build python package
[group('dev')]
build:
    @just sync
    make build


# run tests
[group('dev')]
test *label: ( build )
    #!/usr/bin/env bash
    set -euo pipefail
    PKG="$(find dist -name '*.whl')"
    TOX="time docker compose run --rm -it tox"
    if [ -n "{{label}}" ]; then
      $TOX run --installpkg="$PKG" -m "{{label}}"
    else
      $TOX run-parallel --installpkg="$PKG"
    fi


# compile docs
[group('dev')]
docs:
    make docs
    uv run docsub apply -i README.md


#
#  Release
# ---------
#
# just lint
# just test
# just docs
#
# just version [patch|minor|major]
# just changelog
# (proofread changelog)
#
# just docs
# just build
# just push-pypi
# (create github release)
#


# bump project version (major|minor|patch)
[group('release')]
version:
    #!/usr/bin/env bash
    set -euo pipefail
    uv run bump-my-version show-bump
    printf 'Choose bump path: '
    read BUMP
    uv run bump-my-version bump -- "$BUMP"
    uv lock


# collect changelog entries
[group('release')]
changelog:
    uv run towncrier build --yes --version "$(uv run bump-my-version show current_version 2>/dev/null)"
    sed -e's/^### \(.*\)$/***\1***/; s/\([a-z]\)\*\*\*$/\1***/' -i '' CHANGELOG.md


# publish package on PyPI
[group('release')]
push-pypi:
    @just build
    uv publish
