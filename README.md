This is a Telegram Bot written in Python for Downloading Videos From Terabox.

## Free tier and premium

Free users get separate daily allowances that reset at **12:00 AM IST**:

- 10 single-file TeraBox downloads per day
- 10 `/random` uses per day
- 10 `/search` uses per day
- 1 folder download per day, limited to folders with at most 20 files

Folder files do not consume the 10 single-file downloads. Folders with more
than 20 files are refused for free users. A folder counts against the daily
allowance only when at least one file is delivered.

Only successful results are counted. Failed downloads are refunded, and
invalid links or searches with no results never use an allowance. The owner
bypasses every limit.

Two plans unlock unlimited downloads, folders, `/random` and `/search`:

| Plan | Price | Duration | Dump channel |
| --- | --- | --- | --- |
| ⭐ Jet Premium | ₹59 via UPI only | 30 days | No |
| 💾 Permanent Dump Access | ₹250 or 2.75 USDT | Permanent | Yes |

Payments are verified manually. Send the payment screenshot to
[@rtx5069](https://t.me/rtx5069).

## Bot commands

The bot replies only in private chat. All commands and features work in PM;
groups are ignored completely, except `/user_info` in the premium audit chat.

- `/subscribe` or `/plans` shows the premium plans and payment buttons.
- `/mystatus` shows your current plan, remaining free uses and reset time.
- `/random` sends a random indexed file.
- `/search <keyword> [keyword] [keyword]` lists indexed filenames containing
  all supplied keywords. Search accepts one to three keywords and displays five
  results per page. Inactive search menus expire after 60 seconds.
- `/dump` displays the available payment methods for permanent dump-channel
  access and sends the selected payment QR.
- `/user_settings` opens user settings with a `Language/भाषा` button and
  shows the current plan (`🆓 Free`, `⭐ Paid` with days remaining, or
  `💾 Dump Member`).
  It supports 18 languages, each shown in its own native script
  (English, हिन्दी, मराठी, বাংলা, தமிழ், తెలుగు, ಕನ್ನಡ, മലയാളം, اردو,
  ਪੰਜਾਬੀ, ગુજરાતી, Español, Français, Deutsch, Italiano, 日本語, 한국어,
  中文). The chosen language is
  saved per user and confirmed with a button in that language.
- `/user_settings` also offers **🖼️ Thumbnail** and **📥 Leech Destination**
  options (with `← Back` navigation in every sub-menu) and a **❌ Close**
  button that deletes the settings menu along with the `/user_settings`
  command message:
  - **Thumbnail:** send a photo to set a custom video thumbnail. It is
    normalized to a small JPEG and applied to uploaded videos (including
    every part of split uploads). Remove restores auto-generated thumbs.
  - **Leech Destination:** send a `-100…` channel/group ID. The bot must
    be an admin there and the user must also be an admin of that chat.
    Videos are always uploaded to `DUMP_CHAT_ID` first, then copied to the
    chosen destination. Copies to a custom destination are permanent —
    the 10-minute auto-delete only applies when no destination is set.
    If the copy fails at upload time, the video is sent to the user's chat
    instead with an error note.
  - **Folder Settings:** choose how folder links are delivered. **📄 Single
    files** (the default) sends every file separately; **🗜️ Zipped** packs
    the folder into an archive. The choice is saved per user.
- Folder links are detected automatically. Every Terabox link is preflighted
  against the download API's `/api` endpoint: single-file links stream from
  `/download` exactly as before, while folder links are expanded and all
  downloadable files are sent. Folder files are queued in aria2 together
  (up to 8 concurrent downloads) instead of one at a time, and in *Single
  files* mode each file is sent as soon as its own download finishes. Media
  sends are spaced out and automatically retried on `FloodWait`, so large
  folders are not cut short by Telegram rate limits. Videos
  use the normal video pipeline, images are sent as photos (up to Telegram's
  10 MB photo limit; larger images are sent as documents), and everything
  else is sent as a document. In *Zipped* mode the same parallel downloads
  are archived with the `zip` binary (falling back to `7z` and then Python's
  `zipfile`), split into numbered volumes when the archive exceeds the
  upload limit.
- Pending setting inputs expire after 5 minutes and can be aborted with
  `/cancel`.

### Owner commands

Owner-only commands work in PM. The bot ignores every other group, including
the premium log chat (`PREMIUM_INFO_ID`), with one exception: the owner can
run `/user_info` there (plain or as `/user_info@YourBot`). It never accepts
links or replies to normal messages in groups.

- `/user_info` lists every premium record grouped into permanent,
  active monthly and expired-awaiting-removal, with name, username, user ID,
  DC ID, date of joining, current period start, expiry, remaining time and
  status.
- `/add USER_ID` grants a 30-day subscription. New or expired users start
  now; active users get 30 days added to their current expiry.
- `/adddump USER_ID` grants permanent dump access and unlimited bot use.
- `/remove USER_ID` deletes a premium record. Expired records are never
  removed automatically; the log chat asks the owner before removal.

When a monthly subscription ends, benefits stop immediately, the record is
kept, and the log chat receives one notification with a copy-paste
`/remove@YourBot USER_ID` command.

---

<b>Fill this Values in [config.env](config.env)</b>
- `BOT_TOKEN`: The Telegram Bot Token that you got from [@BotFather](https://t.me/BotFather). `Str`
- `TELEGRAM_API`: This is to authenticate your Telegram account for downloading Telegram files. You can get this from <https://my.telegram.org>. `Int`
- `TELEGRAM_HASH`: This is to authenticate your Telegram account for downloading Telegram files. You can get this from <https://my.telegram.org>. `Str`
- `FSUB_ID`: The Force Subscribe Channel, users will not be able to use your bot without joining the Channel. (Enter the Channel/Group ID starting with -100). `Int`
- `DUMP_CHAT_ID`: The Dump Channel, all leeched videos will be Forwared Here. (Enter the Channel/Group ID starting with -100). `Int`
- `USER_SESSION_STRING`: Pyrogram Session String For 4GB Upload, also add this var for better Uploading Speeds. `Str`
- `DOWNLOAD_API`: Base URL of your Terabox download API, e.g. `http://your-server:8000` (the bot uses `/api` to detect files/folders and `/download?url=...` for single-file streams). `Str`
- `PREMIUM_INFO_ID`: Numeric chat ID (e.g. `-1001234567890`) of the owner-only premium audit chat. It receives premium activation, renewal, removal and expiry events only. It is the only group where the bot replies, and only to the owner's `/user_info`. Leave empty to disable premium logs. `Int`
- `TELEGRAM_MEDIA_DELAY`: Optional. Minimum seconds between Telegram media sends/copies, defaults to `1.0`. Folder uploads retry automatically on `FloodWait` instead of marking files as failed. `Float`

---
### For farther assistance visit my support group: [**@JetMirror**](https://t.me/jetmirrorchatz).
---

## Deploy using CLI on Heroku

- Deployment instructions uploaded [**HERE**](https://gist.github.com/Hrishi2861/3f04a05b4d86241a454bd284ed1c3dee)
- Carefully copy-paste every CMD one by one. If you miss maybe your BOT will not run.

---
## Deploy on VPS
---
## Prerequisites

### 1. Installing requirements

- Clone this repo:

```
git clone https://github.com/Hrishi2861/Terabox-Downloader-Bot/ && cd Terabox-Downloader-Bot
```

- For Debian based distros

```
sudo apt install python3 python3-pip
```

Install Docker by following the [Official docker docs](https://docs.docker.com/engine/install/#server).
Or you can use the convenience script: `curl -fsSL https://get.docker.com |  bash`


- For Arch and it's derivatives:

```
sudo pacman -S docker python
```

------

### 2. Build And Run the Docker Image

Make sure you still mount the app folder and installed the docker from official documentation.

- There are two methods to build and run the docker:
  1. Using official docker commands.
  2. Using docker-compose.

------

#### Build And Run The Docker Image Using Official Docker Commands

- Start Docker daemon (SKIP if already running, mostly you don't need to do this):

```
sudo dockerd
```

- Build Docker image:

```
sudo docker build . -t terabox
```

- Run the image:

```
sudo docker run -p 80:80 -p 8080:8080 terabox
```

- To stop the running image:

```
sudo docker ps
```

```
sudo docker stop id
```

----

#### Build And Run The Docker Image Using docker-compose

**NOTE**: If you want to use ports other than 80 and 8080 change it in [docker-compose.yml](docker-compose.yml).

- Install docker compose

```
sudo apt install docker-compose
```

- Build and run Docker image:

```
sudo docker-compose up --build
```

- To stop the running image:

```
sudo docker-compose stop
```

- To run the image:

```
sudo docker-compose start
```

- To get latest log from already running image (after mounting the folder):

```
sudo docker-compose up
```
