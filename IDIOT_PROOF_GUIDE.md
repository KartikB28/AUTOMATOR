# THE AUTOMATOR — IDIOT-PROOF GUIDE
## For Windows + Instagram. Follow every step. Do not skip.

> If a step doesn't work, STOP. Re-read it. Try again. Don't move on.
> If you're confused about what to click, look at the words in **bold** — those are the buttons.

---

# PHASE A: INSTALL THE 4 TOOLS YOUR PC NEEDS

This phase has zero brain work. Just click "Next" a lot.

## STEP 1 — Install Node.js

1. Open your web browser (Chrome, Edge, Firefox — any of them).
2. In the address bar at the top, type: **`nodejs.org`** and press Enter.
3. You'll see a green webpage. Look for the BIG green button on the LEFT that says **"LTS"** (it will say something like "20.x.x LTS - Recommended For Most Users"). Click it.
4. A file starts downloading at the bottom of your browser. Wait for it. The file is named like `node-v20.10.0-x64.msi`.
5. When the download finishes, click on it (or open your Downloads folder and double-click it).
6. A blue "Welcome to the Node.js Setup Wizard" window opens. Click **"Next"**.
7. Check the box **"I accept the terms in the License Agreement"** → click **"Next"**.
8. Just click **"Next"** on the next screen (don't change the folder).
9. Just click **"Next"** again (don't change the features).
10. **IMPORTANT**: On the screen that says "Tools for Native Modules", **leave the checkbox UNCHECKED**. Click **"Next"**.
11. Click **"Install"**. Windows may pop up asking "Do you want to allow this app to make changes?" — click **"Yes"**.
12. Wait. A green progress bar fills up.
13. When done, click **"Finish"**.

✅ Node.js is installed.

## STEP 2 — Install Python (THE MOST IMPORTANT STEP — DON'T MESS THIS UP)

1. Go to **`python.org`** in your browser.
2. Hover over **"Downloads"** in the top menu → click **"Windows"**.
3. You'll see "Stable Releases" on the left. Find the most recent version (something like Python 3.12.x). Click **"Windows installer (64-bit)"** below it.
4. Wait for the download. The file is named like `python-3.12.1-amd64.exe`.
5. Open the file you just downloaded.
6. A black window with "Install Python 3.12.x" opens.
7. **🚨 STOP. READ THIS. 🚨**
   At the BOTTOM of that window, there are TWO checkboxes. The bottom one says **"Add python.exe to PATH"**.
   **CHECK THAT BOX. ✅ CHECK IT. CHECK IT. CHECK IT.**
   If you forget this, the entire app will not work and you'll have to uninstall and start over.
8. Now click **"Install Now"** (the top blue option).
9. Windows may ask "Do you want to allow this app to make changes?" — click **"Yes"**.
10. Wait for the install. Green progress bar.
11. When you see "Setup was successful", click **"Disable path length limit"** if it's offered (it's a button at the bottom). Click **"Yes"** if Windows asks again.
12. Click **"Close"**.

✅ Python is installed.

### Verify Python is correct
1. Press the **Windows key** on your keyboard.
2. Type **`cmd`** and press Enter. A black window opens.
3. In the black window, type exactly this and press Enter:
   ```
   python --version
   ```
4. You should see `Python 3.12.x` (or higher).
5. If you see `'python' is not recognized as an internal or external command...` — you forgot to check the PATH box in step 7. Uninstall Python (Settings → Apps → Python → Uninstall) and redo Step 2 from the beginning. Don't skip this.

## STEP 3 — Install ffmpeg (for making videos)

1. In your browser, go to: **`https://www.gyan.dev/ffmpeg/builds/`**
2. Scroll down. Find the section called **"release builds"**.
3. Click **`ffmpeg-release-essentials.zip`** to download it.
4. Wait for download. File is like `ffmpeg-6.x-essentials_build.zip`.
5. Open File Explorer (the folder icon at the bottom). Go to your **Downloads** folder.
6. Right-click the zip file you downloaded → click **"Extract All..."**.
7. In the box that pops up, change the path to exactly: **`C:\ffmpeg`**. Click **"Extract"**.
8. Open File Explorer to **`C:\ffmpeg`**. You'll see ONE folder inside (named something like `ffmpeg-6.x-essentials_build`). Open it. You'll see a `bin` folder. **Remember this path** — it will be `C:\ffmpeg\ffmpeg-6.x-essentials_build\bin` (yours will have a slightly different number).
9. Now we add it to PATH so the app can find it:
   - Press **Windows key**, type **`environment variables`**, click **"Edit the system environment variables"**.
   - A System Properties window opens. Click the **"Environment Variables..."** button at the bottom.
   - In the BOTTOM box (System variables), scroll until you see **`Path`**. Click on it once to highlight it. Click **"Edit..."**.
   - A new window opens with a list. Click **"New"** on the right.
   - Paste your ffmpeg bin path from step 8 (the full path ending in `\bin`).
   - Click **"OK"**. Click **"OK"** again. Click **"OK"** one more time.
10. **Close any open Command Prompts (cmd windows). Open a fresh one.**

### Verify ffmpeg
1. Press **Windows key** → type **`cmd`** → Enter.
2. Type:
   ```
   ffmpeg -version
   ```
3. You should see lots of text starting with `ffmpeg version 6.x...`. If yes ✅. If `'ffmpeg' is not recognized` — go back to step 9 and check the path is correct.

## STEP 4 — Install Git

1. Go to **`git-scm.com/download/win`** in your browser.
2. The download starts automatically. File is named like `Git-2.43.0-64-bit.exe`.
3. Open it.
4. Click **"Yes"** if Windows asks permission.
5. Click **"Next"** through ALL the screens. Don't change ANY settings. Just keep clicking **"Next"** until you see **"Install"**.
6. Click **"Install"**. Wait.
7. **UNCHECK** "Launch Git Bash" and "View Release Notes". Click **"Finish"**.

✅ All 4 tools installed. Phase A complete.

---

# PHASE B: GET THE CODE ONTO YOUR COMPUTER

## STEP 5 — Download the Automator code

You already have the code (the GitHub repo). If it's NOT on your computer yet:

1. Go to the GitHub repo URL in your browser.
2. Click the green **"Code"** button → click **"Download ZIP"**.
3. The zip downloads. Extract it to **`C:\AUTOMATOR`** (right-click → Extract All → change path to `C:\AUTOMATOR`).
4. Open File Explorer and go to `C:\AUTOMATOR`. You should see folders named `backend`, `frontend`, `electron`, `config`, etc.

If the code IS already on your computer, just remember the folder location.

---

# PHASE C: GET YOUR API KEYS (THE HARDEST PHASE — TAKE YOUR TIME)

## STEP 6 — Get your Anthropic API key (THE BRAIN)

This costs money but is required. Budget $10/month minimum.

1. Go to **`console.anthropic.com`** in your browser.
2. Click **"Sign Up"**. Use your email or sign in with Google.
3. Verify your email if asked (check your inbox).
4. You'll land on the dashboard.
5. **Add billing first**:
   - Click your profile icon (top right) → **"Plans & Billing"** OR look in the LEFT sidebar for **"Settings" → "Billing"**.
   - Click **"Add Payment Method"**. Enter your credit card.
   - **Add prepaid credit**: usually a button "Add Credits" — add $10 to start.
6. Now create the key:
   - In the left sidebar, click **"API Keys"**.
   - Click **"Create Key"**.
   - In the name field, type: **`Automator`**
   - Click **"Add"** or **"Create Key"**.
7. **🚨 STOP. READ THIS. 🚨**
   A key appears that starts with **`sk-ant-api03-...`**. **Click "Copy"**. Then immediately:
   - Open Notepad (Windows key → type `notepad` → Enter).
   - Paste the key (Ctrl+V).
   - Save this file as `mykeys.txt` on your Desktop.
   - **You cannot see this key again.** If you lose it, you have to make a new one.
8. Label the key in your notepad like:
   ```
   ANTHROPIC_API_KEY = sk-ant-api03-xxxxxxxxxx
   ```

## STEP 7 — Set up Instagram (this takes 30-60 minutes — be patient)

Instagram is the hardest one. Here's the path:

### 7.1 — Make sure you have a Facebook account
Go to `facebook.com`. Log in. If you don't have an account, sign up.

### 7.2 — Make sure you have a Facebook Page
A "Page" is different from your personal profile. It's like a business page.
1. Go to **`facebook.com/pages/create`**
2. Pick **"Brand"** or **"Business or brand"**.
3. Type a name (whatever fits your niche, e.g., "Daily Fitness Tips").
4. Pick a category (e.g., "Health & Wellness").
5. Click **"Create Page"**.
6. Skip adding photos for now — click skip / not now.
7. **Save the Page name** in your notepad. You'll need it.

### 7.3 — Convert your Instagram to a Business Account
1. Open Instagram on your phone (you need the phone app for this).
2. Go to your profile → tap the menu (≡ icon, top right) → **"Settings and privacy"**.
3. Tap **"For professionals"** → **"Account type and tools"** → **"Switch to professional account"**.
4. Pick a category → tap **"Business"** (not Creator) → fill in contact info → **"Connect to Facebook"** and pick the Page you created in 7.2.
5. Done. Your Instagram is now a Business Account linked to your Facebook Page.

### 7.4 — Sign up as a Meta Developer
1. Go to **`developers.facebook.com`** in your browser.
2. Click **"Get Started"** at the top right.
3. Click through the prompts. You may be asked to verify your phone number — do it.
4. When done, you're a developer. ✅

### 7.5 — Create an app
1. Go to **`developers.facebook.com/apps`**.
2. Click **"Create App"** (green button, top right).
3. Choose use case: pick **"Other"** → click **"Next"**.
4. Choose app type: pick **"Business"** → click **"Next"**.
5. Fill in:
   - App name: **`Automator`**
   - Contact email: your email
   - Business portfolio: pick yours (or leave blank)
6. Click **"Create App"**. Enter your password if asked.

### 7.6 — Add Instagram product to your app
1. You're now on the app dashboard. Scroll down to **"Add products to your app"**.
2. Find **"Instagram Graph API"** → click **"Set up"**.
3. Now find **"Facebook Login for Business"** → click **"Set up"** too.

### 7.7 — Get your Instagram Business Account ID
1. In your app dashboard, top menu, click **"Tools"** → **"Graph API Explorer"**.
2. On the right side, you'll see **"Meta App"** dropdown — choose your `Automator` app.
3. Click **"Generate Access Token"** → log in with Facebook → grant permissions.
4. Now in the URL bar at the top of the Graph API Explorer, you'll see something like `me?fields=id,name`. Change it to:
   ```
   me/accounts
   ```
5. Click the blue **"Submit"** button.
6. You'll see JSON output. Find your Page in the list. Copy its `"id"` value (a long number). **Save it as PAGE_ID in your notepad.**
7. Now change the URL bar to:
   ```
   PAGE_ID?fields=instagram_business_account
   ```
   Replace `PAGE_ID` with the actual number you just copied.
8. Click **"Submit"**.
9. The output shows `"instagram_business_account": { "id": "1784..." }`. **Copy that id**. **Save it in your notepad as `INSTAGRAM_BUSINESS_ACCOUNT_ID`.**

### 7.8 — Get a long-lived access token (this is the key the app uses)
1. Still in Graph API Explorer, top right area, click **"Generate Access Token"** again.
2. **IMPORTANT**: Below the token area, click **"Add a Permission"** and add ALL of these:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_show_list`
   - `pages_read_engagement`
   - `business_management`
3. Click **"Generate Access Token"** again — re-confirm permissions in the popup.
4. A new token appears in the **"Access Token"** field at the top. Copy it.
5. **This is a SHORT-LIVED token (only lasts 1 hour). Convert it to long-lived:**
   - Open a new browser tab.
   - Paste this URL (replace 3 things — see below):
     ```
     https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=SHORT_LIVED_TOKEN
     ```
   - Get **APP_ID** from your app dashboard → top left, "App ID: 12345..."
   - Get **APP_SECRET**: in the app dashboard left sidebar → **"App Settings" → "Basic"** → click **"Show"** next to **App Secret** → enter your password → copy it.
   - Replace **SHORT_LIVED_TOKEN** with the token from step 4.
6. Press Enter on the URL. You'll see JSON like:
   ```
   {"access_token":"EAABwz...","token_type":"bearer","expires_in":5183944}
   ```
7. **Copy that long `access_token` value. Save it in your notepad as `INSTAGRAM_ACCESS_TOKEN`.** This one lasts ~60 days.

### Your notepad should now have:
```
ANTHROPIC_API_KEY = sk-ant-api03-xxxxx
INSTAGRAM_ACCESS_TOKEN = EAABwz...
INSTAGRAM_BUSINESS_ACCOUNT_ID = 17841234567890
```

---

# PHASE D: SET UP THE APP

## STEP 8 — Open a Command Prompt in the project folder

1. Open File Explorer (folder icon in taskbar).
2. Navigate to **`C:\AUTOMATOR`** (or wherever you put the code).
3. Click in the address bar at the very top of File Explorer (the bar that shows the path).
4. The path becomes editable. Delete it. Type **`cmd`** and press Enter.
5. A black command prompt window opens, already inside the project folder. ✅

## STEP 9 — Run the setup script

In that black window, type:
```
setup.bat
```
Press Enter.

A wall of text starts scrolling. THIS WILL TAKE 10–20 MINUTES. Don't close the window. Don't click anything. Just wait.

You're done when you see the green text **"Setup complete!"** at the bottom.

If it fails with red errors, scroll up to find the FIRST red error. Most likely:
- "ERROR: Could not find a version that satisfies the requirement" → Python version is too old. Reinstall Python (Step 2) with the newest version.
- "Permission denied" → close the cmd window, right-click `setup.bat` in File Explorer → **"Run as administrator"**.

## STEP 10 — Add your keys to the .env file

1. In the same black command prompt window, type:
   ```
   copy config\.env.example config\.env
   ```
   Press Enter. You'll see "1 file(s) copied."

2. Now open the file:
   ```
   notepad config\.env
   ```
   Press Enter. Notepad opens with the file.

3. You'll see lines like:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   INSTAGRAM_ACCESS_TOKEN=your_instagram_long_lived_access_token
   INSTAGRAM_BUSINESS_ACCOUNT_ID=your_instagram_business_account_id
   ```

4. Replace the right side of each line with YOUR keys from your notepad. Example:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-aBcDeF1234567...
   INSTAGRAM_ACCESS_TOKEN=EAABwzLixnjY...
   INSTAGRAM_BUSINESS_ACCOUNT_ID=17841234567890
   ```
   **Important rules:**
   - NO spaces around the `=` sign
   - NO quotes around the value
   - NO spaces at the end of the line

5. Leave all other lines alone (the bot just skips keys you don't have).

6. Save the file: **Ctrl+S**, then close Notepad (X).

---

# PHASE E: RUN THE APP FOR THE FIRST TIME

## STEP 11 — Start it

In your command prompt window (still in `C:\AUTOMATOR`), type:
```
npm start
```
Press Enter.

Wait. You'll see lots of text scrolling. After 20–60 seconds, **a dark window opens** showing the Automator app.

## STEP 12 — Verify it's working

1. In the app window, click **"Settings"** in the LEFT sidebar.
2. You should see a list of services. Look for **"Anthropic (Claude)"** — there should be a ✅ green checkmark next to it.
3. **"Instagram"** should also have a ✅ green checkmark.
4. Other services without keys will show ❌ — that's fine for now.

If Anthropic shows ❌ red:
- Close the app (X).
- In the cmd window, press **Ctrl+C** then **Y** to kill it.
- Re-open `config\.env` (`notepad config\.env`).
- Check your `ANTHROPIC_API_KEY` line — no quotes, no spaces.
- Save, then `npm start` again.

## STEP 13 — Create your first Niche

1. Click **"Niches"** in the left sidebar.
2. Click the green **"Create Niche"** button (top right).
3. Fill it out (example for fitness):
   - **Name**: `Fitness Tips`
   - **Description**: `Daily fitness tips for busy adults who want to stay in shape`
   - **Keywords**: Click in the keyword box. Type `fitness` and press Enter. Type `workout` and press Enter. Repeat for `home gym`, `weight loss`, `exercise`, `health`. (Press Enter after each one!)
   - **Hashtags**: Type `fitness` and press Enter. Repeat for `workout`, `fitlife`, `fitnessmotivation`, `gymlife`. (The # is added automatically.)
   - **Target Platforms**: ⚠️ Check ONLY **Instagram**. Uncheck everything else (since you only set up Instagram).
   - **Posts per day**: `2` (start small)
   - **Content Tone**: `engaging`
   - **Target Audience**: `Adults 25-45 who want to get fit at home`
   - **Brand Voice**: `Practical, encouraging, no-nonsense`
4. Click **"Create Niche"** at the bottom.

✅ Your first niche exists.

## STEP 14 — Watch the bots work

1. Click **"Dashboard"** in the left sidebar.
2. You'll see 5 bots listed: Scout, Builder, Creator, Publisher, Analyst.
3. **Click the ▶ (play) button** next to **"Scout Bot"**.
4. The status changes to "RUNNING" with a spinning circle. Wait 1-3 minutes.
5. When it's done (status = "idle"), click ▶ next to **"Builder Bot"**. Wait 1-3 minutes.
6. When done, click ▶ next to **"Creator Bot"**. Wait 2-5 minutes (it's making images).
7. Now click **"Content"** in the left sidebar.

🎉 **You should see a grid of posts with images, captions, and hashtags!** Click any one to see the full details.

## STEP 15 — Decide if you're ready to actually publish

Until you trust the AI's content, **don't auto-publish yet**.

To publish a single post manually as a test:
1. Click any post you like in the Content tab.
2. A popup opens with the full caption, image, etc.
3. Scroll down. Click **"Post Now"**.
4. Wait. Status changes to "POSTING" then "POSTED".
5. Open Instagram on your phone — your post should be there!

If you DON'T want it to ever post automatically, leave the schedule empty. The Publisher Bot only fires when it's a scheduled time.

To enable automatic posting:
1. Click **"Schedule"** in the sidebar.
2. Pick your niche from the dropdown.
3. Click **"Add Time Slot"**:
   - Platform: **Instagram**
   - Day: **Every day**
   - Hour: **9** (UTC time — that's 9am UK, 4am New York, 5pm Singapore. Adjust!)
   - Minute: **0**
4. Click **"Add Slot"**.

Now the app will post 1 piece of Instagram content per day at 9am UTC, automatically, forever.

---

# PHASE F: KEEP IT RUNNING 24/7

The whole point — runs while you sleep.

## STEP 16 — Stop your PC from going to sleep

1. Press **Windows key** → type **`power`** → click **"Power & sleep settings"**.
2. Under "Screen", set both dropdowns to **"Never"**.
3. Under "Sleep", set both dropdowns to **"Never"**.
4. Close the window.

If you have a laptop, **plug in the charger and leave it plugged in 24/7**.

## STEP 17 — Make the app start automatically when your PC turns on

We'll use **PM2** — a tool that keeps the app alive forever.

1. Open a NEW command prompt as Administrator:
   - Press **Windows key** → type **`cmd`**.
   - **Right-click** "Command Prompt" → **"Run as administrator"**.
   - Click **"Yes"** to the permission prompt.

2. Install PM2 globally. In the admin cmd, type:
   ```
   npm install -g pm2 pm2-windows-startup
   ```
   Press Enter. Wait 1-2 minutes.

3. Set up PM2 to start with Windows:
   ```
   pm2-startup install
   ```
   Press Enter.

4. Now start the app under PM2 (still in admin cmd):
   ```
   cd C:\AUTOMATOR
   pm2 start npm --name automator -- start
   pm2 save
   ```

5. Test that it survives a reboot:
   - **Restart your PC** (Start menu → Power → Restart).
   - After restart, log in. Wait 2 minutes.
   - Open cmd, type:
     ```
     pm2 status
     ```
   - You should see **automator** listed with status **"online"** (green).

✅ The app is now running in the background 24/7. It restarts itself if it crashes. It starts when Windows starts.

## STEP 18 — Open the app window when you want to check on it

The app is running in the background, but the window is closed. To see it:

```
cd C:\AUTOMATOR
npm run electron
```

Wait — the window opens. You can monitor it. Close the window when done — the bots keep running.

## Quick reference for managing it (run these in any cmd):

```
pm2 status                  → see if app is running
pm2 logs automator          → see what the bots are doing right now (Ctrl+C to exit)
pm2 restart automator       → restart the app (if something seems stuck)
pm2 stop automator          → stop everything
pm2 start automator         → start it again
```

---

# DAILY/WEEKLY ROUTINE

## Every day (5 minutes)
1. Open cmd → `cd C:\AUTOMATOR` → `npm run electron`.
2. Click **Dashboard**. Verify all 5 bots have green dots and recent timestamps.
3. Click **Content**. Scan the latest posts. Delete any that look bad (click → Delete).
4. Close the window.

## Every Monday morning
1. Open the app → click **Analytics**.
2. Read the **Weekly AI Digest** at the bottom — it tells you what worked.
3. Adjust your niche if needed (Niches → Edit → tweak Brand Voice).

## What runs while you sleep
- 12:00 AM, 2:00 AM, 4:00 AM... → Scout Bot finds new trends every 2 hours
- Every hour → Builder Bot writes new content
- Every hour 15 → Creator Bot makes images
- Every 15 minutes → Publisher Bot posts (only at scheduled times)
- Every 6 hours → Analyst Bot pulls metrics

You don't have to do ANYTHING. Just keep your PC on.

---

# IF SOMETHING BREAKS

## "The window won't open"
1. Open cmd → `pm2 logs automator` → look for red text.
2. If you see "Python is not recognized" — go redo Step 2.
3. If you see "EADDRINUSE: address already in use" — restart your PC.

## "All my posts say FAILED"
1. Click the failed post → read the error message at the bottom.
2. If it says "Instagram credentials not configured" — your Instagram tokens are wrong/expired. Redo step 7.8 to get a new long-lived token.
3. If it says "Image url is not accessible" — Instagram can't reach your local PC. You'd need to host images on a public URL (more advanced topic).

## "I don't see any content being created"
1. Make sure you have an active niche (Niches tab → niche has a green power icon).
2. Manually trigger Scout Bot first → wait → then Builder Bot → wait → then Creator Bot.
3. Check the Trends in the database — if Scout found 0 trends, your keywords might be too obscure. Edit your niche, use simpler keywords like "fitness" instead of "lower-back-rehabilitation".

## "Anthropic shows red"
Your `ANTHROPIC_API_KEY` is wrong or out of credits.
1. Go to console.anthropic.com → check Billing → make sure you have credit left.
2. Open `C:\AUTOMATOR\config\.env` in Notepad.
3. Double-check the key — no quotes, no spaces, starts with `sk-ant-api03-`.

## "Instagram token expired" (after ~60 days)
Tokens expire. To refresh:
1. Go back to Step 7.8.
2. Generate a new short-lived token in Graph API Explorer.
3. Convert it to long-lived using the URL in step 7.8 part 5.
4. Update `INSTAGRAM_ACCESS_TOKEN` in `config\.env`.
5. `pm2 restart automator`.

---

**That's literally everything. If you follow this top to bottom without skipping, your PC will be posting Instagram content 24/7 within 2 hours.**
