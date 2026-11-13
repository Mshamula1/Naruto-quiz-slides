# Daily "Guess That Character" TikTok posts

Each daily run makes **two** Naruto "Guess That Character" photo carousels and schedules them in Metricool
for **11:50 AM** and **7:50 PM America/New_York** (10 minutes early, because TikTok takes ~10 min to process a carousel, so posts appear around 12:00 and 8:00) on TikTok account Naruto.quiz.hun (Metricool brand "Naruto Quiz Hun", blogId `8075815`). NEVER use blogId 7999182: that is the owner's separate One Piece account and must not be touched.

## Fixed pieces (never change these)
- **Slide 1, the cover:** `slides/cover.jpg`. It's the owner's chosen Naruto cover image with the title overlaid (source art: `templates/cover_art.jpg`). Use this exact file every time; never re-render or redraw it.
- **Slide 7, the ending:** the "WHO DO YOU THINK IT WAS?" slide. `templates/build.py` produces it identically each run.
- **Layout and style:** `templates/base.html` (CSS, cover, final) and the clue-section shell in `templates/example_clues.html`.

## Steps for each run
1. **Pick 2 characters** from Naruto / Naruto Shippuden (the original series; Boruto-only characters are out) that are NOT in `used.txt`.
   - Lean niche and hard: side characters and one-arc characters, not Team 7 or the most famous Hokage/Akatsuki leads.
   - Make the two posts different difficulty levels: one "HARD MODE" and one "EXTREME MODE".
2. **Write 5 clues per character,** ordered hardest to easiest.
   - Clue 1 is obscure trivia; clue 5 is a near-giveaway (an epithet or iconic moment).
   - **Verify every clue with WebSearch** (Naruto wiki / Narutopedia on fandom) before using it. If a fact can't be verified, drop it.
   - Write in first person, 60–90 characters each, and wrap the key phrase in `<em>`.
   - Never use the character's name in a clue.
3. **Write `clues_<name>.html`** with 5 `<section class="slide">` blocks, copying the structure of `templates/example_clues.html`:
   - header tag + "CLUE N/5"
   - `<svg class="art" viewBox="0 0 1080 960">` illustration
   - parchment card with "CLUE #N" ribbon and the clue text
   - rank badge: 🧠 GENIUS / 🔥 TRUE FAN / 😎 SOLID / 👍 NOT BAD / 😅 ...it's ok
   - swipe label: "next clue →" ×3, "last clue →", "answer time →"
   - Give each slide its own color scheme. Shared SVG defs available from build.py: `#parch #roll #gold #cane #steel2 #grille #dropsh #fogblur #stormsea #bluesea #rope`.
   - JS helpers available: `#laurel #candles #snow #chests #xgrid #rows #tally #crowd`.
4. **ART RULE (strict).** Illustrations must be ORIGINAL drawings of generic objects, places, animals or ideas: a scroll, a forest at night, a bowl of noodles, a toad, a mountain village, a full moon, a stone bridge, and so on. Style them as bold ninja-adventure cartoon art: thick ink outlines, gradients, speed lines, smoke puffs, comic bursts. (The shared defs/helpers in build.py are generic and can still be used.)
   - **Never** draw any Naruto character: no faces, recognizable silhouettes, outfits or hairstyles.
   - **Never** draw their signature items or designs: no forehead protectors/headbands or village symbols (Leaf, Sand, Mist, etc.), no Sharingan/Rinnegan/Byakugan or other eye patterns, no Akatsuki red-cloud design, no Uzumaki swirl crest, no clan crests, no named weapons, no curse marks or seals, no Ichiraku sign, and no series logo.
   - Use no official artwork or images from the web.
5. **Render:**
   - `cd templates && python3 build.py ../work/clues_<name>.html ../work/<name>.html`
   - `python3 shoot.py ../work/<name>.html ../work/<name>`
6. **Check:** make a side-by-side contact sheet of slides 2–7 and look at it. Look for:
   - text overflowing cards, banners or bubbles
   - elements cut off at the edges
   - badges covering text
   - anything that depicts a character

   Fix and re-render as needed.
7. **Publish the images:**
   - Convert slides 2–7 to JPEG (quality 92). TikTok's API doesn't accept PNG.
   - Save them to `slides/<YYYY-MM-DD>-<name>/slide_2.jpg … slide_7.jpg`.
   - Commit and push to `main`.
   - Confirm each `https://raw.githubusercontent.com/Mshamula1/naruto-quiz-slides/main/slides/...` URL returns HTTP 200 before scheduling.
8. **Schedule in Metricool** with `createScheduledPost` (blogId `8075815`):
   - **providers:** tiktok
   - **autoPublish:** true
   - **privacyOption:** PUBLIC_TO_EVERYONE
   - **photoCoverIndex:** 0
   - **autoAddMusic:** true. REQUIRED on every post, so TikTok attaches a trending sound to the carousel; posts without it publish silent. The owner wants sound on every post. (The Metricool API can't pick a specific song for TikTok; only this random-music option is available.)
   - **media**, in this order: `.../slides/cover.jpg`, then slide_2 … slide_7 of that character
   - **times:** 11:50 and 19:50 America/New_York that day (NOT 12:00/20:00; the 10-minute lead covers TikTok processing).
     - If a slot is less than 10 minutes away or already past, skip it, and make only as many characters as there are open slots.
     - First call `getScheduledPosts` for that day with blogId `8075815` (only this brand); if a slot already has a TikTok post, don't add another.
   - **tiktokData.title (required by Metricool):** `Guess That Character: HARD MODE 💀` or `Guess That Character: EXTREME MODE 💀💀`. Never put the answer in the title.
   - **Caption: always a LONG description,** 1,000–1,800 characters (owner's standing request), no line breaks (the TikTok API strips them), ending with
     `#naruto #narutoshippuden #guessthecharacter #animequiz #anime #animetiktok`.
     Fill the length with engagement copy, not answer hints: a vague teaser about the character type (never names, villages, clans, teams or jutsu that give it away), how the clues get easier, a "no googling" challenge, a "got it on clue 1 = genius" brag prompt, a tag-a-friend line, and "Follow for a new Guess That Character quiz every day at 12 PM and 8 PM ET."
     It must still include the style of the earlier captions:
     - a mode label ("HARD MODE 💀" / "EXTREME MODE 💀💀")
     - a challenge hook
     - "swipe through all 5 clues"
     - "comment your answer AND which clue you got it on"
     - "I'll pin the answer later"
     - "who should I do next?"
   - **firstCommentText:** leave empty. Don't reveal the answer.
9. **Record:**
   - Append both names to `used.txt` with the date and scheduled time.
   - Add the answers to `answers.md` (date, time, character, clues), so the owner can pin them.
   - Commit and push.
10. **Report** in one short message which characters were scheduled for which times and their answers.
