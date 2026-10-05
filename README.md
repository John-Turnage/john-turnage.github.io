# john-turnage.github.io

Personal academic website, built with Jekyll and served by GitHub Pages.

## Updating content

Most updates are edits to one YAML file in `_data/`:

| To change | Edit |
|---|---|
| Research page: featured and related projects, figures, captions | `_data/projects.yml` |
| Publications | `_data/publications.yml` |
| Talks | `_data/talks.yml` (a talk is marked "Upcoming" until the end of its month) |
| Courses | `_data/teaching.yml` |
| Education (home page) | `_data/background.yml` |
| Name, email, profile links, navigation, footer "Updated" date | `_config.yml` |

Other pieces:

- **Headshot:** `assets/img/headshot.jpg` (720×900, metadata stripped). It also serves as the link-preview image (set under `defaults` in `_config.yml`).
- **CV page:** `cv.html` embeds the full CV in a scrollable PDF viewer (hidden on phones, where embedded PDFs display poorly), with direct open and download links. Education appears at the bottom of the home page.
- **CV PDF:** run `python3 scripts/build_cv.py`. It compiles `External_Files/CV/main.tex` into `files/John_Turnage_CV.pdf` with the tailoring notes off and the lab-only sections removed, without modifying the source.
- **Research figures:** PNGs in `assets/img/research/`, listed per project in `_data/projects.yml`.
- **Colors and type:** tokens at the top of `assets/css/main.css`. The site opens in the light theme; the toggle switches to dark and remembers the choice.

`External_Files/` holds private source material and is git-ignored; copy only finished files into `files/` or `assets/`.

## Previewing locally

```sh
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
bundle install            # first time only
bundle exec jekyll serve --livereload
```

Then open http://127.0.0.1:4000. The `Gemfile` is for local preview only; GitHub Pages builds the site with its own Jekyll 3.10 environment when you push to `main`.
