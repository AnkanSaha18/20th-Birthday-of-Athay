# Hosting the website for free with GitHub Pages

Repo: https://github.com/AnkanSaha18/20th-Birthday-of-Athay
Live site (after setup): **https://ankansaha18.github.io/20th-Birthday-of-Athay/**
Magazine reader: https://ankansaha18.github.io/20th-Birthday-of-Athay/magazine.html

GitHub Pages is free on **public** repos (private repos need GitHub Pro). A workflow in
`.github/workflows/pages.yml` publishes only the `Website/` folder every time you push to `main`.

> Before you go public: anyone on the internet can then browse the whole repo, including the
> original photos in `Images/`, the family photos, the love letter and the print PDFs, and download them.
> If that's not OK, keep the repo private and use the Cloudflare Pages option at the bottom instead (also free).

---

## Step 1 · Push the latest changes (GitHub Desktop)

1. Open **GitHub Desktop**; the repo `20th-Birthday-of-Athay` is selected.
2. Under **History** you'll see the commit "Deploy website with GitHub Pages…" already made.
3. Click **Push origin** (top bar).

## Step 2 · Make the repository public

1. Open https://github.com/AnkanSaha18/20th-Birthday-of-Athay
2. Click **Settings** (top tab, gear icon).
3. Scroll to the very bottom: **Danger Zone** → **Change repository visibility** → **Change visibility**.
4. Choose **Make public**, confirm the warnings and type the repo name when asked.

## Step 3 · Turn on GitHub Pages

1. Still in **Settings**, click **Pages** in the left sidebar.
2. Under **Build and deployment** → **Source**, choose **GitHub Actions** (not "Deploy from a branch").
   Nothing else to fill in.

## Step 4 · Run the deploy

1. Click the **Actions** tab of the repo.
2. Click **Deploy website to GitHub Pages** on the left → **Run workflow** → **Run workflow**.
   (From now on, every push to `main` deploys automatically.)
3. Wait for the green tick (about a minute); the run page shows the site link.
4. Open **https://ankansaha18.github.io/20th-Birthday-of-Athay/**, tap the seal, sound on.

If you get a 404 right after the first deploy, wait a minute and refresh.

## Updating later

Edit the files → GitHub Desktop → write a summary → **Commit to main** → **Push origin**.
The site updates within a minute or two.

---

## Going private and back to public (re-deploying)

**What happens:** on a free GitHub account, Pages only works for public repos. The moment you switch the
repo to **private**, GitHub unpublishes the site and the link shows a 404. Nothing is deleted: the files,
the workflow and the history all stay in the repo.

**Turning it back on:** making the repo public again does *not* always bring the site back by itself,
so do this every time:

1. Repo → **Settings** → bottom **Danger Zone** → **Change visibility** → **Make public**.
2. **Settings** → **Pages** → under **Build and deployment** → **Source**: make sure it says
   **GitHub Actions** (choose it again if it's blank or says "Deploy from a branch").
3. **Actions** tab → **Deploy website to GitHub Pages** (left side) → **Run workflow** → **Run workflow**.
4. Wait for the green tick, then open https://ankansaha18.github.io/20th-Birthday-of-Athay/
   (same address as before). If it still shows 404, wait a couple of minutes and refresh.

**Notes**
- Every push to `main` also re-deploys automatically, so pushing any small change does the same as step 3.
- If you see "Deploy website to GitHub Pages" failing with a Pages/permissions error, step 2 was skipped.
- Google: while the site is down, Google may drop it from search results. After it's back, open
  Search Console → **URL inspection** → paste the URL → **Request indexing**. The Google verification
  file stays in the `Website` folder, so you don't need to verify again.
- Want the files private *and* the site online? Use the Cloudflare Pages option below instead.

---

## If you'd rather keep everything private (also free): Cloudflare Pages

1. Keep the repo **private**.
2. https://dash.cloudflare.com → **Workers & Pages** → **Create** → **Pages** → **Connect to Git** → choose this repo.
3. Framework preset **None**, build command empty, **Build output directory: `Website`** → **Save and Deploy**.
4. Live at `https://<project-name>.pages.dev`. Optional: project **Settings → Access policy** to allow only her email and yours.

---

## Getting it on Google Search

The pages now carry a search title and description built around "20th Birthday of Athay", a share preview
image (`Website/assets/og-image.jpg`), a canonical URL, structured data, icons and `Website/sitemap.xml`.

1. Push the latest commit in GitHub Desktop and wait for the green tick in **Actions**.
2. Open https://search.google.com/search-console and sign in with your Google account.
3. **Add property** → choose **URL prefix** (right side) → paste
   `https://ankansaha18.github.io/20th-Birthday-of-Athay/` → **Continue**.
4. Verify ownership with **HTML file**:
   - Download the file it offers (named like `google1a2b3c4d5e.html`).
   - Put it inside the `Website` folder (next to `index.html`), then commit and push in GitHub Desktop.
   - Wait for the deploy to finish, check that
     `https://ankansaha18.github.io/20th-Birthday-of-Athay/google1a2b3c4d5e.html` opens, then click **Verify**.
5. Left menu → **Sitemaps** → enter `sitemap.xml` → **Submit**.
6. Top search bar (**URL inspection**) → paste the site URL → **Request indexing**.
   Do the same for `https://ankansaha18.github.io/20th-Birthday-of-Athay/magazine.html`.

Google usually lists a new page within a few days, sometimes a week or two; nobody can force the exact
day. Then searching **20th Birthday of Athay** should bring it up. Sharing the link anywhere public
(e.g. an Instagram bio or a post) helps Google find it faster.

To check the link-preview card (WhatsApp / Messenger / Facebook), paste the URL into
https://developers.facebook.com/tools/debug/ → **Scrape Again**.
