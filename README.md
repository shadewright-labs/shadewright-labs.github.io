# shadewright-labs.github.io

The organisation site of Shadewright Labs: one page about the house, its products (Shadewright, Sablecourt and Nightloom) and the security laws they share. It is plain HTML and CSS with no build step, no JavaScript and no requests to other sites.

The site will be served at https://shadewrightlabs.com once the custom domain is set up. Until then it is at https://shadewright-labs.github.io. All links inside the site are relative or start at the site root, so it works on both hosts.

## Layout

| Path | Contents |
| --- | --- |
| `index.html` | The landing page |
| `404.html` | The page GitHub Pages serves for a missing path. Its links start at `/` because it is served at any depth. |
| `assets/site.css` | The only stylesheet |
| `assets/products-diagram-*.svg` | The diagram of how the products fit together, hand-written SVG: a wide version, and a tall one for narrow screens |
| `assets/<identity>/` | Logo, glyphs, favicons and the social preview image, copied from the Shadewright Labs brand kit |
| `robots.txt`, `.nojekyll` | Crawl rules, and a marker that turns off Jekyll processing on Pages |
| `package.json`, `package-lock.json`, `.htmlvalidate.json` | The pinned HTML validator used by CI. Not published. |

## Paths and repositories

GitHub Pages serves this repository at the root of the domain. Each project repository of the organisation that turns on Pages is served under a path named after the repository, from that repository's own Pages build.

| URL path | Published from |
| --- | --- |
| `/` | This repository |
| `/sablecourt/` | The [Sablecourt repository](https://github.com/shadewright-labs/sablecourt)'s own Pages build (not published yet) |

Do not add a `sablecourt/` directory here: the path belongs to the Sablecourt repository, and a directory of the same name here would conflict with it. Shadewright's documentation has its own domain, https://shadewright.io/, and is not served under this site.

## Preview locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000/. The local server does not serve `404.html` for missing paths the way Pages does; open http://localhost:8000/404.html to see it.

## Checks

Pull requests run `.github/workflows/ci.yml`. The required check is `ci-ok`, which passes when these jobs pass:

- HTML validation with [html-validate](https://html-validate.org/), pinned in `package-lock.json`. Locally: `npm ci --ignore-scripts && npm run validate`.
- Links with [lychee](https://lychee.cli.rs/), downloaded at a pinned version and checked against its SHA-256. Every internal link, asset and anchor must resolve. External links fail the job on an error such as a 404, but not on a timeout or a rate limit.
- [actionlint](https://github.com/rhysd/actionlint) on the workflows, pinned the same way.

## Publishing

`.github/workflows/pages.yml` runs on every push to `main`. It copies the site files (`index.html`, `404.html`, `robots.txt`, `.nojekyll` and `assets/`) into a staging folder and deploys that folder with the official Pages actions, pinned to commit SHAs. Nothing else in the repository is published.

The repository's Pages settings must use "GitHub Actions" as the source. There is no `CNAME` file yet: the custom domain is set in the repository settings when DNS for shadewrightlabs.com points at GitHub Pages.

## Licence

Apache License 2.0, see [LICENSE](LICENSE). The Shadewright Labs, Shadewright, Sablecourt and Nightloom names and artwork identify the projects; the licence does not grant rights to use them as your own marks.
