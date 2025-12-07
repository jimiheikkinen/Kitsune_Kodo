# Kitsune_Kodo
Kitsune_Kodo artwork lies here in this repository

# Links:
https://opensea.io/0x158fc9698baa1f390a43642b60a318a7ee2557c9/created

https://opensea.io/collection/kitsune-kodo

---

## 🦊 Tweet Generator CLI

A powerful Python command-line tool to generate commercial tweets for X (Twitter) using OpenAI API, with direct posting capability. Built with argparse for clean, intuitive syntax.

### Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure your OpenAI API key and X credentials:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   X_API_KEY=your_x_api_key_here
   X_API_SECRET=your_x_api_secret_here
   X_ACCESS_TOKEN=your_access_token_here
   X_ACCESS_TOKEN_SECRET=your_access_token_secret_here
   ```

   - Get OpenAI API key from: https://platform.openai.com/api-keys
   - Get X API credentials from: https://developer.twitter.com/en/portal/dashboard

### Recreate the working demo on Windows (tested flow)

**What worked:** OAuth 1.0a with local callback `http://127.0.0.1:8080` (no public tunnel needed). The app posted successfully with regenerated read/write tokens.

1) **App permissions**
   - In X Developer Portal → App Settings → User authentication settings: set permissions to **Read and Write** (not read-only).
   - Callback / Redirect URL: `http://127.0.0.1:8080`
   - Website URL: any valid URL (e.g., `https://opensea.io/collection/kitsune-kodo`).

2) **Regenerate tokens (must be after enabling Read/Write)**
   - Keys and tokens → Regenerate **Access Token** and **Access Token Secret** (they must say Read and Write).

3) **Set up environment on Windows**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   copy .env.example .env
   notepad .env   # paste OPENAI_API_KEY, X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
   ```

4) **Run the tool**
   ```powershell
   python tweet_generator.py --product kitsune_kodo --tone hype --length short --post
   ```
   - When prompted `Post this tweet to X? (yes/no):` enter `yes`.
   - On success you will see the posted URL (example from the working demo: `https://x.com/jiiiihooooooo/status/1997667529464897975`).

5) **If posting fails with 401/403**
   - Re-check app permissions are Read/Write.
   - Regenerate Access Token and Secret after changing permissions.
   - Ensure `.env` values match the regenerated tokens (no extra spaces/newlines).
   - Keep `.env` out of git (already gitignored).

### Usage

**Basic syntax:**
```bash
python tweet_generator.py --product <product_name> --tone <tone> --length <length>
```

**Generate and post a tweet:**
```bash
python tweet_generator.py --product kitsune_kodo --tone hype --length short --post
```

**Generate multiple variations (interactive posting):**
```bash
python tweet_generator.py --product kitsune_kodo --tone professional --length medium --variations 3 --post
```

**Generate without posting:**
```bash
python tweet_generator.py --product kitsune_kodo --tone hype --length short
```

**Add a custom message:**
```bash
python tweet_generator.py --product kitsune_kodo --tone urgent --length long --message "Limited edition drop tonight!" --post
```

### Command-Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--product` | Yes | - | Product to market. Available: `kitsune_kodo` |
| `--tone` | No | `professional` | Tone of the tweet |
| `--length` | No | `medium` | Maximum tweet length |
| `--variations` | No | `1` | Number of tweet variations to generate |
| `--message` | No | - | Custom message or marketing angle |
| `--post` | No | - | Post generated tweet(s) to X (requires confirmation) |
| `--help` | No | - | Show help message |

#### Available Tones
- `professional` - Business-like, polished
- `casual` - Relaxed, friendly
- `hype` - Energetic, exciting
- `urgent` - Time-sensitive, compelling
- `friendly` - Warm, approachable
- `humorous` - Fun, witty
- `mysterious` - Enigmatic, intriguing

#### Length Presets
- `short` - Maximum 140 characters
- `medium` - Maximum 220 characters
- `long` - Maximum 280 characters (X limit)

### Examples

```bash
# Generate and post a hype tweet
python tweet_generator.py --product kitsune_kodo --tone hype --length short --post

# Generate 5 professional variations and choose which to post
python tweet_generator.py --product kitsune_kodo --tone professional --variations 5 --post

# Urgent tone with custom message, ready to post
python tweet_generator.py --product kitsune_kodo --tone urgent --message "Last chance to mint!" --post

# Mysterious vibe, long format, without posting
python tweet_generator.py --product kitsune_kodo --tone mysterious --length long

# Casual tone, 3 variations, medium length
python tweet_generator.py --product kitsune_kodo --tone casual --length medium --variations 3
```

### Posting Tweets

When you use the `--post` flag:

1. **Single Tweet**: You'll be asked for confirmation before posting
   ```
   📤 Post this tweet to X? (yes/no): yes
   ✅ Tweet posted successfully!
   🔗 URL: https://x.com/your_username/status/...
   ```

2. **Multiple Variations**: You can choose which variations to post
   ```
   [1] Tweet text here...
   Post this tweet? (yes/no): yes
   ✅ Posted: https://x.com/your_username/status/...
   ```

### Product Configuration

The tool includes a product database with details for each product:
- Product name and description
- Suggested hashtags
- Product URL (OpenSea link)

**Current Products:**
- `kitsune_kodo` - Fox spirit NFT collection with traditional Japanese aesthetics

To add more products, edit the `PRODUCTS` dictionary in `tweet_generator.py`.

### Features

- ✨ AI-powered tweet generation using GPT-4
- 🎨 7 different tone options (professional, casual, hype, urgent, friendly, humorous, mysterious)
- 📏 3 length presets (short, medium, long)
- 🔄 Generate multiple variations to choose from
- 📊 Automatic character count validation
- 🏷️ Product-specific hashtags and URLs
- 💬 Custom message support for specific campaigns
- 📤 Direct posting to X (Twitter) with confirmation
- 🦊 Clean argparse interface for easy scripting
- 🔐 Secure API key management via .env file

### Output Format

The tool displays:
- Generated tweet text
- Character count (e.g., 184/280)
- For multiple variations, numbered list with individual character counts
- Posting confirmation and tweet URL (when posted)

### Error Handling

- Validates OpenAI API key presence
- Validates X API credentials presence
- Checks product availability
- Ensures tweets stay within character limits
- Provides clear error messages for debugging
- Handles X API errors gracefully

---

## 🎨 Kitsune Art Generator CLI

Generate AI-powered Kitsune (fox spirit) artwork using DALL-E 3. Creates unique images based on type and custom specifications, saved in L33t-style filenames to a dedicated folder.

### Setup (same as tweet generator)

Already configured if you ran the tweet generator setup above. Requirements already include `requests` for image downloads.

### Quick Start Guide

1. **Ensure OpenAI API key is in `.env`** (same key used for tweet generator)

2. **Generate your first Kitsune:**
   ```bash
   python kitsune_art_generator.py --type fire
   ```

3. **Check the output:**
   - Look in the `kitsune_art/` folder
   - You'll see a PNG file like: `K1tsun3_fire_20251207_160053.png`

4. **Try with custom specifications:**
   ```bash
   python kitsune_art_generator.py --type ice --specs "9-tailed fox with silver fur and sapphire eyes"
   ```

5. **Experiment with all types:**
   - `--type fire` → Crimson and gold flames
   - `--type dark` → Shadow and purple mystique
   - `--type ice` → Crystalline blue and white frost
   - `--type demon` → Red and gray with horns
   - `--type spirit` → Ethereal white and silver
   - `--type sacred` → Golden and radiant divine light

### Usage

**Generate a Kitsune artwork:**
```bash
python kitsune_art_generator.py --type fire
```

**Generate with custom specs:**
```bash
python kitsune_art_generator.py --type dark --specs "9-tailed fox with crimson fur and golden eyes"
```

**Try different types:**
```bash
python kitsune_art_generator.py --type ice
python kitsune_art_generator.py --type demon
python kitsune_art_generator.py --type spirit --specs "ethereal white fox with glowing wisps"
python kitsune_art_generator.py --type sacred --specs "celestial kitsune with divine aura"
```

### Command-Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--type` | Yes | - | Kitsune type: `fire`, `dark`, `ice`, `demon`, `spirit`, `sacred` |
| `--specs` | No | - | Custom features/description (e.g., "9-tailed with golden eyes") |
| `--help` | No | - | Show help message |

### Kitsune Types

- **fire** - Crimson and gold, blazing energy, mystical flames
- **dark** - Shadow-infused, dark purples and blacks, sinister mystique
- **ice** - Crystalline blue and white, frosty aura, glacial elegance
- **demon** - Demonic red and gray, horns and claws, malevolent presence
- **spirit** - Ethereal white and silver, glowing wisps, divine presence
- **sacred** - Golden and radiant, holy light, celestial majesty

### Output

- **Location:** `kitsune_art/` folder
- **Filenames:** L33t-style Kitsune names (e.g., `K1tsun3_fire_20251207_160053.png`)
- **Format:** PNG, 1024x1024px
- **Size:** ~1.9MB per image

### Generated Examples

```
✅ Kuva tallennettu: kitsune_art/G0ld3n_F1r3_fire_20251207_160053.png
✅ Kuva tallennettu: kitsune_art/T41l_0f_F1r3_ice_20251207_160120.png
```

### Features

- ✨ DALL-E 3 powered image generation
- 🎨 6 unique Kitsune types with custom visual styles
- 🦊 L33t-style filenames for generated images
- 📁 Dedicated `kitsune_art/` folder for all outputs
- 💬 Custom specs support for fine-tuning artwork
- 🎯 Automatic timestamp and type tagging in filenames
- 🔐 Uses existing OpenAI API key from `.env`

### Notes

- Each image costs OpenAI API credits (DALL-E 3).
- Images are 1024x1024px, high quality.
- Filenames are randomized L33t-style Kitsune names with timestamp to avoid duplicates.
- All files saved to `kitsune_art/` for easy organization.

---

- Asennus: `pip install -r requirements.txt`, kopioi `.env.example` → `.env` ja lisää OpenAI + X (OAuth1) avaimet.
- X-asetukset: luvat **Read ja Write**, callback `http://127.0.0.1:8080`, Website URL mikä tahansa (esim. OpenSea-linkki).
- Uusi Access Token & Secret: regeneroi ne vasta, kun Read/Write on päällä.
- Ajo: `python tweet_generator.py --product kitsune_kodo --tone hype --length short --post` → vastaa `yes` postauskysymykseen.
- Jos 401/403: tarkista luvat, regeneroi tokenit, varmista että `.env` sisältää viimeisimmät arvot.

#### Kitsune Art Generator
- Luo AI-taidetta DALL-E 3:lla kuuden eri tyypin Kitsun-eille (fire, dark, ice, demon, spirit, sacred).
- Ajo: `python kitsune_art_generator.py --type fire --specs "9-tailed fox with golden eyes"`
- Tiedostot tallennetaan `kitsune_art/` -kansioon L33t-tyyli nimillä (esim. `K1tsun3_fire_20251207_160053.png`).
- Käyttää samaa OpenAI API-avainta `.env`:stä.
