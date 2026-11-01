# Private GitHub repo + free hosting (Cloudflare Pages)

The whole `Birthday` folder is one git repository (branch `main`, about 1.2 GB) and is committed on
your Mac. Only the `Website/` folder gets published as the site; the magazine sources, print PDFs
and original photos stay private in the repo.

Why Cloudflare Pages: GitHub Pages needs a paid plan for private repos, and it can't publish a
sub-folder like `Website/` without extra setup. Cloudflare Pages is free, works with private repos,
redeploys on every push, and can lock the site so only the people you choose can open it.

---

## Part 1 · Create the private repository on GitHub

1. Sign in at https://github.com and open https://github.com/new
2. Repository name: e.g. `athay-20`
3. Choose **Private**
4. Leave "Add a README", ".gitignore" and "license" **unticked** (the folder already has them)
5. Click **Create repository** and keep the page open; it shows your repo URL,
   e.g. `https://github.com/<your-username>/athay-20.git`

## Part 2 · Push the folder (Terminal on your Mac)

Large files need a bigger HTTP buffer, so run these once:

```bash
cd ~/Desktop/Anno/Birthday
git config http.postBuffer 524288000
git remote add origin https://github.com/<your-username>/athay-20.git
git push -u origin main
```

- When asked for a **username**, type your GitHub username.
- When asked for a **password**, paste a **personal access token**, not your GitHub password:
  GitHub → your photo → Settings → Developer settings → Personal access tokens → Tokens (classic)
  → Generate new token → tick **repo** → Generate → copy it.
- The first push uploads about 1.2 GB, so it can take a while on slow Wi-Fi.
  GitHub will print a warning that a few print PDFs are over 50 MB. That's fine; the limit is 100 MB.

(Prefer clicking? Install GitHub Desktop → File → Add Local Repository → choose the `Birthday` folder
→ Publish repository → keep "Keep this code private" ticked.)

## Part 3 · Host it free on Cloudflare Pages

1. Create a free account at https://dash.cloudflare.com/sign-up
2. In the dashboard: **Workers & Pages** → **Create** → **Pages** tab → **Connect to Git**
3. Click **Connect GitHub**, choose **Only select repositories** → `athay-20` → **Install & Authorize**
4. Select `athay-20` → **Begin setup**, then fill in:
   - Project name: `athay-20` (this becomes `athay-20.pages.dev`; pick something sweet, it must be unique)
   - Production branch: `main`
   - Framework preset: **None**
   - Build command: *(leave empty)*
   - Build output directory: `Website`
5. Click **Save and Deploy**. After a minute or two the site is live at
   `https://<project-name>.pages.dev`

Every time you `git push`, Cloudflare redeploys automatically.

## Part 4 · (Recommended) Lock it so only she and you can open it

Without this, anyone who has the link can see the site. It's hidden from search engines, but a link can be forwarded.

1. Cloudflare dashboard → your Pages project → **Settings** → **General** → **Access policy** → **Enable**
   (first time, it asks you to pick a free Zero Trust team name and the **Free** plan; it may ask for a card
   but the Free plan, up to 50 people, costs nothing)
2. Edit the policy: Action **Allow** · Include → **Emails** → her email address and yours
3. Save. Now when she opens the link she enters her email, gets a 6-digit code, and she's in.

Note: by default the Access policy protects preview links. To protect the main `*.pages.dev` address too,
open Zero Trust → Access → Applications → edit the app and add the main domain `<project-name>.pages.dev`.

## Updating the site later

```bash
cd ~/Desktop/Anno/Birthday
git add -A
git commit -m "Update"
git push
```

## Alternative: Netlify (also free)

https://app.netlify.com → Add new site → Import an existing project → GitHub → `athay-20`
→ Base directory: `Website` · Build command: empty · Publish directory: `Website` → Deploy.
Netlify's password protection needs a paid plan, so the link itself is the key.
