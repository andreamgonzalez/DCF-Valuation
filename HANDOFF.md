# Handoff: redesign with Tailwind CSS

Written 2026-10-09 for the next working session. Delete this file once the redesign is merged.

## The task

Redesign the app's front end so it looks professional, using **Tailwind CSS**, with **a light and a dark theme**. Nothing of the redesign has been started. All work so far was on the back end.

The owner chose Tailwind from a four-way comparison page (Bootstrap, Tabler, Tailwind with daisyUI, Bulma): https://claude.ai/artifact/EdoQNa5TvCeaNkR4Ko1vHq

The option shown there was Tailwind **with daisyUI** (light preview used the `corporate` theme, dark used `business`). The owner's reply was "Go with tailwind with light and dark theme". Treat daisyUI as the intended component layer, and confirm that in one line before building.

## Where things stand

- Repo: `~/projects/DCF-Valuation`, GitHub `andreamgonzalez/DCF-Valuation`.
- Current branch: `upgrade-python-and-libraries`, pushed. It contains three commits on top of `master`:
  1. `90835e5` Fix the DCF valuation math
  2. `b8764f3` Update yfinance to 1.2.0 and fix the financials lookup
  3. `0b2c8a4` Upgrade to Python 3.14 and the latest libraries
- `master` is untouched and no pull request has been opened. Start the redesign on a new branch off `upgrade-python-and-libraries`.
- Commit, push and pull requests only when the owner asks. Commit author for this repo is set locally to `andreagon <andreagon6135@gmail.com>`.

## Running it

```bash
cd ~/projects/DCF-Valuation
source venv/bin/activate          # Python 3.14.8, everything in requirements.txt installed
flask run                         # http://127.0.0.1:5000
python -m unittest test_dcf test_routes
```

- `venv/` is git-ignored. Python 3.14.8 was installed through pyenv; the pyenv global is still 3.8.10.
- Postgres runs locally. `valuation` is the dev database (tables created, no accounts yet). `valuation_test` is used by `test_routes.py`, which drops and recreates its tables.
- Live stock data comes from Yahoo through `yfinance`, so pages under `/stock/<ticker>` and `/valuation/<ticker>` need network access and take a few seconds.
- There is no browser on this machine for screenshots. The owner views the app in their Windows browser, so ask them to look after each visible change.

## What the front end is today

Server-rendered Jinja templates, Bootstrap loaded unversioned from unpkg, plus jQuery and Font Awesome 5.3.1. No build step, and `static/app.js` is empty.

| Template | Lines | Notes |
|---|---|---|
| `templates/base.html` | 72 | Navbar ("The Analyst"), loads all CSS and JS. The flash-message block is inside an HTML comment, so messages are invisible site-wide. |
| `templates/public.html` | 87 | Landing page, own `<style>` block |
| `templates/login.html`, `signup.html` | 26, 25 | WTForms loops |
| `templates/valuations/stocksSearch.html` | 46 | Ticker search |
| `templates/valuations/stockDetail.html` | 342 | Historical financials tables |
| `templates/valuations/valuationForm.html` | 358 | Logged-in assumptions form plus history tables |
| `templates/valuations/publicValuationForm.html` | 353 | Near-duplicate of the above for logged-out users |
| `templates/valuations/valuationDetail.html` | 214 | Results table |
| `templates/users/dashboard.html` | 142 | Hardcoded placeholder cards (AMZN, "Some quick example text"); it does not show the user's saved valuations |

Things that will bite:

- **Line endings are CRLF** in every `.py`, `.html` and `.css` file. Preserve them, or diffs show every line as changed.
- **Each page carries its own `<style>` block** forcing a dark background (`#212529`) and white headings. These have to go for theming to work.
- **The two valuation form templates are nearly identical** (their diff is about ten lines of styling). Merging them into one template, or a shared partial, before restyling halves the work.
- **The valuation forms render flashed messages themselves** (added for the "WACC must be greater than the terminal growth rate" error). If the flash block in `base.html` is re-enabled, remove those two copies so messages do not show twice.
- **The results template indexes rows oddly**: per-year rows loop over `valuation`, totals (terminal value, enterprise value, equity value, share price) read `valuation[:1]`. A valuation is five rows, periods 1 to 5, with the totals repeated on each row.
- **Figures arrive pre-formatted**. Logged-out results are strings in millions with thousands separators; saved results come back from the database as floats in millions (for example `1100.0`). Nothing on the page says "$ in millions".
- **The form hints are misleading.** The "change %" rows show year-over-year growth, but the EBIT, tax, D&A and capex inputs now mean a share of revenue (tax is a share of EBIT).

## Suggested approach

1. **Tooling.** Tailwind needs a build step. The deployment is Python-only (`Procfile` runs gunicorn, `runtime.txt` pins Python), so avoid making Node a deploy requirement: build the CSS locally and commit the output under `static/`. Node is installed on this machine; Tailwind's standalone CLI is the alternative. Check the current Tailwind and daisyUI install docs first, since both changed their setup in their latest major versions.
2. **Theme.** Two themes with a toggle in the navbar, defaulting to the visitor's system setting and remembering their choice. Set the theme before first paint to avoid a flash.
3. **Base layout first.** Rebuild `base.html` (navbar, container, visible flash messages, theme toggle), drop Bootstrap, jQuery and the unversioned CDN links, then confirm with the owner before converting the rest.
4. **Convert pages in order of use**: results, valuation form, stock detail, search, landing, login and signup, dashboard.
5. **Tables are the core of the app.** Right-align numbers, use tabular figures, keep the first column readable, let wide tables scroll inside their own container, and label the units.

Agree the scope of step 4 with the owner: a restyle of what exists, or also fixing the dashboard so it lists real saved valuations.

## Open items outside the redesign

Raised with the owner, not yet acted on:

- Three security items are listed in `HANDOFF.private.md`, a local file that is deliberately not committed because this repo is public.
- The forms use `DataRequired`, which rejects `0`, so a 0% assumption cannot be entered.
- A company whose latest year has no reported cash or long-term debt gets an error instead of a valuation.
- Saved valuations are stored as five rows sharing a random ID between 0 and 4000, which can collide. The `Valuation` model declares several columns twice.
- `Stock`, `Financial` and `Favorites` tables and the favorite and delete routes are unused or commented out.
- `runtime.txt` asks for Python 3.14.8; nothing has been deployed since the upgrade.
