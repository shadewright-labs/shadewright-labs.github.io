#!/usr/bin/env bash
# Copies the published site into a staging folder (default: _site) from an explicit allow-list, then checks that
# nothing else came along: no dotfiles other than .nojekyll and .well-known, and no file outside the list.
# Used by the Pages and CI workflows, so what CI checks is what Pages publishes.
set -euo pipefail

out="${1:-_site}"
files=(index.html 404.html robots.txt .nojekyll)
dirs=(assets .well-known)

if [[ -e "${out}" ]]; then
  echo "stage-site: ${out} already exists" >&2
  exit 1
fi
mkdir "${out}"
cp "${files[@]}" "${out}/"
cp -R "${dirs[@]}" "${out}/"

# Dotfiles: only the two the site needs.
unexpected=$(cd "${out}" && find . -name '.*' ! -name '.' ! -path './.nojekyll' ! -path './.well-known' ! -path './.well-known/*' -print)
if [[ -n "${unexpected}" ]]; then
  echo "stage-site: unexpected dotfiles in ${out}:" >&2
  echo "${unexpected}" >&2
  exit 1
fi
# Top level: only the allow-list.
while IFS= read -r entry; do
  case "${entry}" in
    index.html | 404.html | robots.txt | .nojekyll | assets | .well-known) ;;
    *)
      echo "stage-site: unexpected top-level entry: ${entry}" >&2
      exit 1
      ;;
  esac
done < <(ls -A "${out}")
echo "stage-site: staged $(find "${out}" -type f | wc -l | tr -d ' ') files, $(du -sk "${out}" | cut -f1) KiB, in ${out}"
