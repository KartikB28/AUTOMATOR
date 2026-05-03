# THE AUTOMATOR — COMPLETE SETUP MANUAL
## How to run this 24/7 on your PC, step-by-step

> Read every line. Don't skip. Don't improvise. If a step fails, scroll to **PART 9: TROUBLESHOOTING** at the end.

---

## WHAT YOU'RE ABOUT TO BUILD

You will install:
1. Node.js (so the desktop window can run)
2. Python (so the bots can run)
3. ffmpeg (so videos can be made)
4. The Automator code (already in this folder)

Then you will:
5. Get an Anthropic API key (the AI brain — REQUIRED)
6. Get keys for at least 1 platform you want to post to
7. Paste those keys into a config file
8. Run one command to start everything
9. Create your first "Niche" inside the app
10. Set it up to run 24/7 even when your PC restarts

**Total time: 30-90 minutes depending on which APIs you set up.**

---

## PART 0: WHICH OPERATING SYSTEM ARE YOU ON?

This guide has 3 versions per step:
- 🟦 **WINDOWS**
- 🟩 **macOS** (Mac)
- 🟧 **LINUX**

Look for the icon that matches your computer. Skip the others.

---

# PART 1: INSTALL THE TOOLS

## STEP 1.1 — Install Node.js

Node.js is what runs the desktop window of the app.

### 🟦 WINDOWS
1. Go to https://nodejs.org
2. Click the big green button that says **"LTS"** (currently version 20)
3. Open the file you just downloaded (`node-v20.x.x.msi`)
4. Click **Next, Next, Next, Install**. Accept all defaults.
5. When it finishes, click **Finish**.

### 🟩 macOS
1. Go to https://nodejs.org
2. Click the big green button that says **"LTS"**
3. Open the file you just downloaded (`node-v20.x.x.pkg`)
4. Click **Continue, Continue, Agree, Install**. Type your Mac password.
5. When it finishes, click **Close**.

### 🟧 LINUX (Ubuntu / Debian)
Open a Terminal (press `Ctrl+Alt+T`) and paste this exactly:
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### CHECK IT WORKED
Open a NEW terminal/command prompt window (closing and reopening matters!) and type:
```
node --version
```
You should see something like `v20.10.0`. If you see `command not found`, restart your computer and try again.

---

## STEP 1.2 — Install Python 3.11 or newer

Python is what runs the 5 bots.

### 🟦 WINDOWS
1. Go to https://www.python.org/downloads/
2. Click the yellow button: **"Download Python 3.12.x"**
3. Open the file (`python-3.12.x-amd64.exe`)
4. **VERY IMPORTANT**: At the bottom of the install window, **CHECK the box** that says **"Add python.exe to PATH"**. If you forget this, nothing will work.
5. Click **"Install Now"**. Wait.
6. Click **Close**.

### 🟩 macOS
Python comes with Mac but the version is usually too old. Install a fresh one:
1. Go to https://www.python.org/downloads/
2. Click the yellow button: **"Download Python 3.12.x"**
3. Open the `.pkg` file
4. Click through the installer with all defaults

### 🟧 LINUX (Ubuntu / Debian)
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv
```

### CHECK IT WORKED
In a NEW terminal/command prompt:
```
python --version
```
(On macOS / Linux, you may need to type `python3 --version` instead)

You should see something like `Python 3.12.1`. Must be **3.11 or higher**.

---

## STEP 1.3 — Install ffmpeg (for making videos)

### 🟦 WINDOWS
1. Go to https://www.gyan.dev/ffmpeg/builds/
2. Scroll down to **"release builds"**
3. Click **`ffmpeg-release-essentials.zip`** to download
4. Right-click the downloaded zip → **Extract All** → save to `C:\ffmpeg`
5. Open Start Menu, type **"environment variables"**, click **"Edit the system environment variables"**
6. Click **"Environment Variables..."** button at the bottom
7. In the bottom box (System variables), find **`Path`**, click it, click **Edit**
8. Click **New**, paste: `C:\ffmpeg\bin` (adjust if you extracted elsewhere — find the `bin` folder inside the extracted folder)
9. Click **OK** on all 3 windows
10. **Close all command prompts and open a fresh one**

### 🟩 macOS
First install Homebrew if you don't have it. Open Terminal and run:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Then:
```bash
brew install ffmpeg
```

### 🟧 LINUX
```bash
sudo apt-get install -y ffmpeg
```

### CHECK IT WORKED
```
ffmpeg -version
```
You should see a wall of text starting with `ffmpeg version ...`.

---

## STEP 1.4 — Install Git (you may already have it)

### 🟦 WINDOWS
Download and install from https://git-scm.com/download/win — accept all defaults.

### 🟩 macOS
Open Terminal and run `git --version`. If it asks to install, click **Install**.

### 🟧 LINUX
```bash
sudo apt-get install -y git
```

---

# PART 2: GET YOUR API KEYS

You need at minimum:
- **1 Anthropic key** (REQUIRED — this is the AI brain)
- **1 platform key** (whichever site you want to post to first)

You can add more later. Start small.

## STEP 2.1 — Get your Anthropic API Key (REQUIRED)

This is the brain. The whole thing dies without it.

1. Go to https://console.anthropic.com/
2. Sign up with your email (or log in if you have an account)
3. **Add billing**: Click **"Plans & Billing"** in the left sidebar → **Add a credit card**. Put $5–10 as your starting credit. (The Builder Bot uses ~$0.01 per piece of content. $10 = ~1,000 posts of content.)
4. Click **"API Keys"** in the left sidebar
5. Click **"Create Key"**
6. Name it `Automator`
7. Click **Create**
8. **COPY THE KEY** that appears. It starts with `sk-ant-...`. **You will never see it again** — if you lose it you have to make a new one.
9. Paste it somewhere safe for now (a sticky note, notepad file, etc.)

You now have the most important key. ✅

## STEP 2.2 — Choose ONE platform to start with

Don't try to set up all 6 at once. Start with the easiest. Here they are ranked from **easiest to hardest**:

| Rank | Platform | Difficulty | Cost | Notes |
|------|----------|-----------|------|-------|
| 🥇 1 | **Facebook Page** | Easy | Free | If you have a Facebook Page, takes ~15 min |
| 🥈 2 | **LinkedIn** | Easy | Free | Posts to your personal LinkedIn |
| 🥉 3 | **Instagram** | Medium | Free | Requires Instagram Business Account + Facebook Page |
| 4 | **YouTube** | Medium | Free | OAuth flow takes some clicking |
| 5 | **TikTok** | Hard | Free | Developer app approval can take 1–7 days |
| 6 | **Twitter/X** | Hard | $100/mo | Posting now requires paid API ($100/month minimum) |

**My recommendation: Start with Facebook Page or LinkedIn.** Get one working end-to-end, then add more.

### Easiest path: FACEBOOK PAGE

1. You need a **Facebook Page** (not just your profile). If you don't have one:
   - Go to https://www.facebook.com/pages/create
   - Pick "Brand or Product" → name it whatever your niche is → Create

2. Get a Page Access Token:
   - Go to https://developers.facebook.com/tools/explorer/
   - Top right: click your profile pic → **"Get Page Access Token"**
   - Click **Continue / Allow** to grant permissions
   - In the **"User or Page"** dropdown, choose your Page name
   - In the **Permissions** field, add: `pages_manage_posts`, `pages_read_engagement`, `pages_show_list`
   - Click **"Generate Access Token"** — copy this token
   - **Save this token** (this is your `FACEBOOK_PAGE_ACCESS_TOKEN`)

3. Get your Page ID:
   - Go to your Facebook Page
   - Click **About** in the left menu
   - Scroll to **"Page transparency"** — your Page ID is shown there
   - **Save this** (this is your `FACEBOOK_PAGE_ID`)

That's it for Facebook.

### Easy path #2: LINKEDIN

1. Go to https://www.linkedin.com/developers/
2. Click **"Create app"**
3. Fill in: App name = `Automator`, LinkedIn Page = your company page (or create one), Logo = anything
4. Check the legal box → **Create app**
5. Click your new app → **Auth** tab
6. Add OAuth 2.0 redirect: `http://localhost:8000/callback`
7. Go to **Products** tab → request access to **"Share on LinkedIn"** and **"Sign In with LinkedIn"**
8. After approval, on the **Auth** tab you'll see your **Client ID** and **Client Secret** — save them
9. To get an access token, you'll need to do the OAuth flow. The simplest way: use https://www.linkedin.com/developers/tools/oauth/token-generator — sign in, pick scopes (`w_member_social`), generate token, **copy it** (this is your `LINKEDIN_ACCESS_TOKEN`)
10. To get your Person ID: while on developers.linkedin.com, hit https://api.linkedin.com/v2/me with your token in the Authorization header, look for `"id":"XXXX"`. Your `LINKEDIN_PERSON_ID` is `urn:li:person:XXXX` (with that prefix).

### For all the other platforms

The setup steps are in the file `config/.env.example`. Each platform's developer portal:
- Instagram → https://developers.facebook.com/apps/ (same as Facebook, then add "Instagram Graph API" product)
- TikTok → https://developers.tiktok.com/
- YouTube → https://console.cloud.google.com/ (create project, enable YouTube Data API v3, create OAuth credentials)
- Twitter/X → https://developer.twitter.com/ (paid)

You can come back and add these after the first one works.

## STEP 2.3 — Optional but recommended free keys

These make your images way better. All free.

### Pexels (free stock photos)
1. Go to https://www.pexels.com/api/
2. Click **"Get Started"** → sign up
3. Copy the API key from your dashboard

### Unsplash (free stock photos)
1. Go to https://unsplash.com/developers
2. Sign up → **"New Application"** → accept terms
3. Name it `Automator` → submit
4. Copy the **Access Key**

### OpenAI (DALL-E 3 image generation, ~$0.04/image)
1. Go to https://platform.openai.com/api-keys
2. Sign in → click **"Create new secret key"**
3. Add billing ($5–10 credit)
4. Copy the key (starts with `sk-...`)

---

# PART 3: SET UP THE AUTOMATOR

## STEP 3.1 — Open a terminal in the project folder

The code is at `/home/user/AUTOMATOR` (this folder). Whenever this manual says "in your terminal", it means a terminal opened **inside that folder**.

### 🟦 WINDOWS
1. Open File Explorer
2. Navigate to where you cloned/copied the project
3. Click in the address bar at the top, type `cmd` and press Enter
4. A black window opens. You're now "in" the folder.

### 🟩 macOS / 🟧 LINUX
1. Open Terminal
2. Type `cd ` (with a space) but don't press Enter yet
3. Drag the project folder from Finder/Files into the terminal — its path appears
4. Press Enter

You should now see the prompt has the project path. Type `ls` (or `dir` on Windows) and press Enter — you should see `package.json`, `electron`, `frontend`, `backend`, etc.

## STEP 3.2 — Run the setup script

This installs everything the app needs. It will take 5–15 minutes — go get a coffee.

### 🟦 WINDOWS
```
setup.bat
```

### 🟩 macOS / 🟧 LINUX
```bash
./setup.sh
```

You'll see lots of text scrolling by — that's normal. It's downloading thousands of files. **Wait until you see `Setup complete!`** at the end. If it errors out, see PART 9.

## STEP 3.3 — Create the .env config file

The `.env` file holds all your API keys.

### 🟦 WINDOWS
```
copy config\.env.example config\.env
notepad config\.env
```

### 🟩 macOS / 🟧 LINUX
```bash
cp config/.env.example config/.env
nano config/.env
```
(or open the file in any text editor — VS Code, TextEdit, anything)

You will see lines like:
```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
FACEBOOK_PAGE_ACCESS_TOKEN=your_facebook_page_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id
```

**Replace the right side of each line with the keys you saved earlier.** Example:
```
ANTHROPIC_API_KEY=sk-ant-api03-aBcD1234...
FACEBOOK_PAGE_ACCESS_TOKEN=EAABwz...
FACEBOOK_PAGE_ID=123456789012345
```

Leave the keys you don't have alone (the bot just skips them).

**Save the file:**
- Notepad: Ctrl+S → Close
- Nano: Ctrl+O → Enter → Ctrl+X
- VS Code / TextEdit: Cmd+S or Ctrl+S → close

---

# PART 4: FIRST RUN

## STEP 4.1 — Start the app

In your terminal (still in the project folder):

```
npm start
```

What happens:
1. Two terminal panels appear (or text from two processes mixed together)
2. After ~10–30 seconds, **a window opens** showing the Automator dashboard
3. The window is dark with a sidebar on the left

If a window doesn't appear after 60 seconds, see PART 9.

## STEP 4.2 — Verify everything is healthy

In the app window:
1. Click **"Settings"** in the left sidebar
2. You should see a list of services with green checkmarks (✅) for the ones you set up keys for
3. **Anthropic must be green.** If it's red, your `ANTHROPIC_API_KEY` is wrong — go fix `config/.env`, save, then close the app and `npm start` again.

## STEP 4.3 — Create your first Niche

A "Niche" is a content topic — like "Fitness" or "Tech News".

1. Click **"Niches"** in the sidebar
2. Click **"Create Niche"** (top right)
3. Fill in the form:
   - **Name**: `Fitness Tips` (or whatever you want)
   - **Description**: `Daily fitness tips for busy adults`
   - **Keywords**: Type each one and press Enter — `fitness`, `workout`, `home gym`, `exercise`, `weight loss`
   - **Hashtags**: Type each — `#fitness`, `#workout`, `#fitlife`
   - **Target Platforms**: Check ONLY the platform(s) you have keys for. (Don't check Instagram if you didn't set up Instagram!)
   - **Posts per day**: `2` (start small)
   - **Content Tone**: `engaging`
   - **Target Audience**: `Adults 25-45 who want to get in shape`
   - **Brand Voice**: `Practical, no-BS, motivating but realistic`
4. Click **Create Niche**

## STEP 4.4 — Watch the bots work

1. Click **"Dashboard"** in the sidebar
2. You'll see 5 bots listed with status circles
3. Click the **▶ play button** next to **"Scout Bot"** to run it now (don't wait for the schedule)
4. Status changes to "RUNNING" with a spinner. Wait 1–3 minutes.
5. When it finishes, click **▶** next to **"Builder Bot"**. Wait 1–3 minutes.
6. Click **▶** next to **"Creator Bot"**. Wait 2–5 minutes (it's downloading/generating images).
7. Click **"Content"** in the sidebar — you should see a grid of generated posts with thumbnails!
8. Click any post to see the full caption, hook, hashtags.

🎉 If you see content appearing in the Content tab, **the system is working**.

## STEP 4.5 — Make your first real post (optional, do this when ready)

Until you're confident it looks good, **don't auto-publish**. To delete a post: click it → Delete. To force-publish a single post manually: click it → "Post Now".

Once you're ready to let it post automatically:
1. Go to **Schedule**
2. Pick your niche
3. Click **"Add Time Slot"** — pick a platform, day = "Every day", hour = `9`, minute = `0`
4. Save. Now Publisher Bot will post that niche at 9am UTC daily.
5. Add more slots as desired.

If no schedule is set, Publisher Bot will post any time it has ready content (up to the daily limit).

---

# PART 5: HOW THE 5 BOTS WORK (the manual part you asked for)

This is the brain map. Memorize this.

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE AUTOMATOR PIPELINE                       │
└─────────────────────────────────────────────────────────────────┘

    ⏰ Every 2 hours          ⏰ Every 1 hour       ⏰ Every 1 hour
    ┌──────────────┐         ┌──────────────┐    ┌──────────────┐
    │  SCOUT BOT   │ ──────> │  BUILDER BOT │ ─> │ CREATOR BOT  │
    │              │         │              │    │              │
    │  Scrapes:    │         │  Calls       │    │  Tries:      │
    │  • Google    │         │  Claude AI   │    │  1. DALL-E 3 │
    │  • Reddit    │         │  to write:   │    │  2. Stability│
    │  • Twitter   │         │  • Hooks     │    │  3. Pexels   │
    │  • TikTok    │         │  • Captions  │    │  4. Unsplash │
    │  • YouTube   │         │  • Scripts   │    │  5. Generate │
    │  • RSS       │         │  • Hashtags  │    │     fallback │
    │              │         │  • CTAs      │    │  Then makes  │
    │  Scores      │         │              │    │  thumbnail.  │
    │  trends.     │         │  One per     │    │              │
    │  Saves top   │         │  platform    │    │              │
    │  20 to DB.   │         │  per trend.  │    │              │
    └──────────────┘         └──────────────┘    └──────────────┘
                                                          │
                                                          ▼
    ⏰ Every 6 hours                                ⏰ Every 15 min
    ┌──────────────┐                              ┌──────────────┐
    │  ANALYST BOT │ <──── posted content ────── │ PUBLISHER BOT│
    │              │                              │              │
    │  Pulls       │                              │  Checks the  │
    │  metrics.    │                              │  schedule.   │
    │  Calculates  │                              │  Posts to:   │
    │  engagement. │                              │  • Instagram │
    │  Mondays:    │                              │  • TikTok    │
    │  generates   │                              │  • YouTube   │
    │  weekly AI   │                              │  • Twitter   │
    │  digest.     │                              │  • LinkedIn  │
    │              │                              │  • Facebook  │
    └──────────────┘                              └──────────────┘
```

**Status flow of one piece of content:**
```
pending (Scout/Builder created it)
   ↓
media_pending (Creator picked it up)
   ↓
media_ready (Creator finished media)
   ↓
posting (Publisher is sending it)
   ↓
posted ✅ (live on the platform)
```

If anything fails, status becomes `failed` with an error message you can see by clicking the post.

**The bots run on their own.** As long as the app is running, they fire on schedule. You don't need to touch anything.

---

# PART 6: KEEP IT RUNNING 24/7

The whole point — automation that doesn't stop. There are 3 things to fix:
1. PC stays on (no sleeping)
2. App auto-starts when PC reboots
3. App auto-restarts if it crashes

## STEP 6.1 — Stop your PC from going to sleep

### 🟦 WINDOWS
1. Open **Settings** → **System** → **Power & battery** (or "Power & sleep")
2. Set **Screen** = `Never`
3. Set **Sleep** = `Never`
4. (Laptop) Plug in the charger — the bots eat CPU/network 24/7.

### 🟩 macOS
1. **System Settings** → **Displays** → **Advanced** → set **"Prevent automatic sleeping..."** to ON
2. **System Settings** → **Battery** (or **Energy Saver**) → set **"Prevent computer from sleeping when display is off"** ON
3. Or just run this in Terminal to keep it awake forever:
   ```bash
   caffeinate -d &
   ```

### 🟧 LINUX
```bash
# GNOME
gsettings set org.gnome.desktop.session idle-delay 0
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing'
```
Or open **Settings → Power → Screen Blank: Never; Automatic Suspend: Off**.

## STEP 6.2 — Auto-start the app on boot

### 🟦 WINDOWS
1. Press **Win+R**, type `shell:startup`, press Enter — Startup folder opens
2. Right-click in this folder → **New** → **Shortcut**
3. For the location, paste:
   ```
   cmd /k "cd /d C:\path\to\AUTOMATOR && npm start"
   ```
   Replace `C:\path\to\AUTOMATOR` with the actual path on your PC
4. Click **Next** → name it `Automator` → **Finish**
5. Restart your PC. The app should open automatically.

### 🟩 macOS
1. Create a launch script at `~/automator-start.command`:
   ```bash
   echo '#!/bin/bash
   cd /path/to/AUTOMATOR
   npm start' > ~/automator-start.command
   chmod +x ~/automator-start.command
   ```
2. **System Settings** → **General** → **Login Items** → click **+** → choose `automator-start.command`
3. Restart Mac to test.

### 🟧 LINUX (systemd — most robust, auto-restarts on crash)
1. Create a service file:
   ```bash
   sudo nano /etc/systemd/system/automator.service
   ```
2. Paste this (replace `YOURUSER` and the path):
   ```ini
   [Unit]
   Description=The Automator
   After=network.target

   [Service]
   Type=simple
   User=YOURUSER
   WorkingDirectory=/home/YOURUSER/AUTOMATOR
   ExecStart=/usr/bin/npm start
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```
3. Save (Ctrl+O, Enter, Ctrl+X)
4. Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable automator
   sudo systemctl start automator
   ```
5. Check status: `sudo systemctl status automator`
6. View logs: `journalctl -u automator -f`

## STEP 6.3 — Auto-restart if it crashes (Windows/macOS)

The Linux systemd setup above already does this. For Windows/macOS, install **PM2** (a Node.js process manager that auto-restarts):

```bash
npm install -g pm2
```

Then in the project folder:
```bash
pm2 start npm --name automator -- start
pm2 save
pm2 startup
```
Run the command pm2 prints back at you (it sets up auto-start).

To check: `pm2 status`. To see logs: `pm2 logs automator`. To restart: `pm2 restart automator`.

---

# PART 7: USING THE APP DAY-TO-DAY

## What you should do daily (5 minutes)
1. Open the app
2. Go to **Dashboard** — verify all 5 bots show recent runs (last few hours)
3. Go to **Content** — scan recent posts, delete any that look bad
4. Go to **Analytics** — see what's getting engagement

## What you should do weekly
1. Read the **Weekly AI Digest** at the bottom of Analytics — it tells you what's working
2. Tweak your niche's brand voice / keywords based on what performs
3. Add new platforms once you've validated the first one works

## What runs without you
- Scout Bot every 2 hours: finds new trending topics
- Builder Bot every 1 hour: writes content for those trends
- Creator Bot every 1 hour 15 min: makes images
- Publisher Bot every 15 min: posts to platforms (respects schedule + daily limits)
- Analyst Bot every 6 hours: pulls metrics; generates weekly report on Mondays

## Adjusting how often it posts
**Niche → Edit → Posts per day**: this controls how many times Publisher Bot will post per niche **across all platforms** per day. So `posts_per_day=6` with 3 platforms = 2 posts per platform per day.

## Pausing everything (e.g., going on vacation)
Click **Bots** in sidebar → **Pause All** at the top right. Everything halts. Click **Resume All** to wake it up.

You can also right-click the system tray icon (bottom right of screen) and pick **"Pause All Bots"**.

---

# PART 8: COSTS

Rough monthly costs at moderate use (3 niches × 3 posts/day × 6 platforms = ~50 posts/day):

| Service | Cost/month | Required? |
|---------|------------|-----------|
| Anthropic API | $5–25 | YES |
| OpenAI (DALL-E 3) | $30–60 | No (falls back to Pexels) |
| Stability AI | $10 | No |
| Pexels / Unsplash | Free | No |
| Twitter/X API | $100 | No (skip Twitter) |
| All other platforms | Free | No |
| Electricity | $5–15 | Yes (PC on 24/7) |

**Cheapest viable setup**: $10/mo (Anthropic + free stock photos + no Twitter).

---

# PART 9: TROUBLESHOOTING

## The window doesn't open when I run `npm start`
- Wait a full 60 seconds first
- Check the terminal output for red error messages
- Most common: Python isn't on your PATH → reinstall Python and check the "Add to PATH" box

## "Command not found: npm" / "node"
Restart your computer after installing Node.js. Open a fresh terminal.

## Setup script fails with "ERROR: Could not install packages..."
Your Python is probably too old. Run `python --version` (or `python3 --version`). Must be 3.11+.

## All bots show "error" status
Open Settings → check that **Anthropic** has a green checkmark. If red, your API key is wrong.

## Posts say "failed" with "Instagram credentials not configured"
You haven't filled in `INSTAGRAM_ACCESS_TOKEN` and `INSTAGRAM_BUSINESS_ACCOUNT_ID` in `config/.env`. **Or** you have the niche set to post to Instagram but didn't set up that platform — uncheck Instagram on the niche.

## Builder Bot fails with "model claude-sonnet-4-6 not found"
Your Anthropic key works but doesn't have access to that model yet. Check https://docs.anthropic.com/en/docs/about-claude/models for the latest model name and update `backend/bots/builder_bot.py` line ~149 (`model="claude-sonnet-4-6"`).

## Instagram post fails with "image_url is not accessible"
Instagram needs your image to be hosted on a public URL. Local file URLs don't work for them in production. The dev setup uses `http://localhost:PORT/media/...` which only works if Instagram's servers can reach your machine. Solutions:
1. Use **ngrok** to expose your local server: `ngrok http 8765`, then edit `backend/platforms/instagram.py` line ~106 to use the ngrok URL
2. Or upload images to S3/Cloudinary first (more advanced, not built-in)

## Reddit/Twitter scraping returns nothing
Both platforms aggressively block scrapers. Scout Bot will still get plenty of trends from Google Trends, RSS, and YouTube. Don't worry about it.

## Disk filling up with images
Old media files pile up in the `media/` folder. Once a month, delete folders inside `media/` for dates older than 30 days. (Future: auto-cleanup will be added.)

## How do I see the logs?
- **Live in terminal**: just look at the `npm start` window
- **Saved logs**: `~/.automator/logs/automator.log` (Mac/Linux) or `%USERPROFILE%\.automator\logs\automator.log` (Windows)
- **Systemd**: `journalctl -u automator -f`
- **PM2**: `pm2 logs automator`

## I want to stop everything completely
- Close the app window (X)
- If using PM2: `pm2 stop automator && pm2 delete automator`
- If using systemd: `sudo systemctl stop automator && sudo systemctl disable automator`

---

# QUICK REFERENCE — ALL COMMANDS

```bash
# Install everything (one-time)
./setup.sh                # Mac/Linux
setup.bat                 # Windows

# Start the app
npm start

# Run with PM2 (auto-restart on crash)
pm2 start npm --name automator -- start
pm2 logs automator        # see what's happening
pm2 restart automator     # restart
pm2 stop automator        # stop

# Linux systemd
sudo systemctl start automator
sudo systemctl stop automator
sudo systemctl status automator
journalctl -u automator -f
```

---

**That's it. Follow this manual top to bottom. If you get stuck on any step, the answer is in PART 9.**
