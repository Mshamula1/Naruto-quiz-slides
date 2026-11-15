# Daily Naruto "Shinobi Quiz" TikTok posts

> **FORMAT (since 2026-11-16): narrated VIDEO posts, not photo carousels.** The owner approved the video format on 2026-11-15 ("Draft 6"). Each quiz is still built from the same Ink & Washi slides, then turned into a ~55 s 1080x1920 MP4 with a bright female quiz-host voice, captions, countdowns and music by `templates/video/`. Do not change the voice, script template, caption style or pacing without the owner's approval.

Each daily run makes **two** Naruto "Guess That Character" quiz videos and schedules them in Metricool
for **11:50 AM** and **11:50 PM America/New_York** (10 minutes early, because TikTok takes ~10 min to process a carousel, so posts appear around 12:00 PM (noon) and 12:00 AM (midnight)) on TikTok account Naruto.quiz.hun (Metricool brand "Naruto Quiz Hun", blogId `8075815`). NEVER use blogId 7999182: that is the owner's separate One Piece account and must not be touched.

## Fixed pieces (never change these)
- **Slide 1, the cover:** `slides/cover.jpg`. It's the owner's chosen Naruto cover image with the title overlaid (source art: `templates/cover_art.jpg`). Use this exact file every time; never re-render or redraw it.
- **Slide 7, the ending:** the black "WHO WAS IT?" reveal slide with the red brush circle. `templates/build.py` produces it identically each run.
- **Layout and style ("Ink & Washi"):** all CSS, SVG filters and the final slide live in `templates/build.py`; fonts (Anton, Oswald) are bundled in `templates/fonts/`. `templates/base.html` only holds the cover. The finished example to copy is `templates/example_naruto_clues.html`.
- **This style must stay clearly different from the owner's One Piece account** (which uses colorful cartoon art, parchment clue cards, emoji rank badges and a yellow "?" ending). Never bring any of those elements in here.

## Steps for each run
1. **Pick 2 characters** from Naruto / Naruto Shippuden (the original series; Boruto-only characters are out) that are NOT in `used.txt`.
   - Lean niche and hard: side characters and one-arc characters, not Team 7 or the most famous Hokage/Akatsuki leads.
   - Make the two posts different difficulty levels: one "B-RANK MISSION" (hard) and one "S-RANK MISSION" (extreme).
2. **Write 5 clues per character,** ordered hardest to easiest.
   - Clue 1 is obscure trivia; clue 5 is a near-giveaway (an epithet or iconic moment).
   - **Verify every clue with WebSearch** (Naruto wiki / Narutopedia on fandom) before using it. If a fact can't be verified, drop it.
   - Write in first person, 60–90 characters each, and wrap the key phrase in `<em>`.
   - Never use the character's name in a clue.
3. **Write `clues_<name>.html`** with 5 `<section class="slide ink">` blocks, copying the structure of `templates/example_naruto_clues.html` exactly:
   - `<!--PAPER-->` placeholder first (build.py swaps in the washi paper texture)
   - optional `<div class="sun">` red circle placed behind the art (vary its size/position, or leave it out)
   - red hanko stamp `<div class="stamp"><b>CLUE</b><i>N/5</i></div>` and the vertical `<div class="label">GUESS THAT CHARACTER</div>`
   - `<svg class="art" viewBox="0 0 1080 900">` illustration (keep the right ~120px clear for the vertical label)
   - `<!--BAND-->` placeholder (build.py swaps in the black brush-stroke band), then `<div class="cluebox"><div class="num">01 — HARDEST</div><div class="clue">…</div></div>` (numbers: "01 — HARDEST", "02", "03", "04", "05 — EASIEST")
   - level line `<div class="lvl">GOT IT HERE? <span>…</span></div>`: KAGE LEVEL / JONIN / CHUNIN / GENIN / ACADEMY
   - swipe line: "KEEP SWIPING →" ×3, "LAST CLUE NEXT →", "THE REVEAL →"
   - No emoji anywhere on clue slides.
4. **ART RULE (strict).** Illustrations must be ORIGINAL drawings of generic objects, places, animals or ideas: a scroll, a forest at night, a bowl of noodles, a toad, a mountain village, a full moon, a stone bridge, a cargo ship, and so on.
   - **Style: Japanese sumi-ink.** Black ink (`#141210`) on cream paper, ONE accent color only (vermilion `#d8361f` / `#ff6a3d`). Bold silhouettes and brush strokes, soft gray ink washes. No gradients other than `#vsun`, no drop shadows, no other colors, no cartoon outlines-with-color-fill.
   - Put `filter="url(#brush)"` on ink strokes and silhouettes, `filter="url(#roughen)"` on red shapes and stamps, and `filter="url(#wash)"` (with ~.12–.25 opacity) on gray background washes. Available defs: `#brush #roughen #wash #grain #fibers #vsun #mist`.
   - **Never** draw any Naruto character: no faces, recognizable silhouettes, outfits or hairstyles.
   - **Never** draw their signature items or designs: no forehead protectors/headbands or village symbols (Leaf, Sand, Mist, etc.), no Sharingan/Rinnegan/Byakugan or other eye patterns, no Akatsuki red-cloud design, no Uzumaki swirl crest, no clan crests, no named weapons, no curse marks or seals, no Ichiraku sign, and no series logo.
   - Use no official artwork or images from the web.
5. **Render:**
   - `cd templates && python3 build.py ../work/clues_<name>.html ../work/<name>.html`
   - `python3 shoot.py ../work/<name>.html ../work/<name>`
6. **Make the video** (after build.py made `work/<name>.html`; slides are the video's frames):
   - Once per session: `sh templates/video/setup.sh` (pip deps + Kokoro voice model from GitHub releases; prints SETUP_OK).
   - `nohup sh templates/video/make_video.sh <name> > work/<name>_video.log 2>&1 &` then poll the log (`sleep 60; tail -3 work/<name>_video.log`) until it prints `FIN` (about 3-4 min per video; Bash calls time out at 2 min, so never run it in the foreground). Output: `work/<name>_video/<name>.mp4`.
   - What it does: hides the clue text/swipe line to make a "blank" version of each slide, generates the narration from `templates/video/make_script.py` (fixed hook, "Clue one!"... "Last clue!", the clue read aloud exactly as on the slide, a rank call-out after each clue: Kage / Jonin / Chunin / Genin / Academy, fixed outro), voices it with Kokoro `af_heart` at speed 1.15, renders: cover with soft white captions → per clue: blank slide, clue appears as it is read, 3-2-1 "LOCK IN YOUR GUESS" countdown, red caption sticker for the rank line → "WHO WAS IT?" outro; then mixes voice + SFX + generated koto/taiko music and loudness-normalizes to -14 LUFS.
   - Clue text is read aloud, so write clues that read naturally (no emoji, no symbols the voice can't say).
7. **Check:** make a side-by-side contact sheet of slides 2–7 and look at it. Look for:
   - text overflowing the black band or highlights cutting into neighbouring lines
   - elements cut off at the edges
   - the art running under the vertical label or the stamp
   - anything that depicts a character

   Fix and re-render as needed. Also look at `work/<name>_video/check_20s.jpg` and confirm the video duration printed before FIN is 45-75 s.
8. **Publish the video:**
   - Copy it to `slides/<YYYY-MM-DD>-<name>/<name>.mp4` (no JPEG slides needed any more).
   - Commit and push to `main`.
   - Confirm `https://raw.githubusercontent.com/Mshamula1/naruto-quiz-slides/main/slides/<YYYY-MM-DD>-<name>/<name>.mp4` returns HTTP 200 before scheduling.
9. **Schedule in Metricool** with `createScheduledPost` (blogId `8075815`):
   - **providers:** tiktok
   - **autoPublish:** true
   - **privacyOption:** PUBLIC_TO_EVERYONE
   - **autoAddMusic:** false. The video already has its own narration and music (TikTok's auto-music only applies to photo posts). Do not set photoCoverIndex, videoThumbnailUrl or videoCoverMilliseconds.
   - **media:** exactly one item, the raw.githubusercontent.com URL of that day's `<name>.mp4`.
   - **times:** 11:50 and 23:50 America/New_York that day (NOT 12:00/00:00; the 10-minute lead covers TikTok processing). Both slots belong to the same calendar day as the run.
     - If a slot is less than 10 minutes away or already past, skip it, and make only as many characters as there are open slots.
     - First call `getScheduledPosts` for that day with blogId `8075815` (only this brand); if a slot already has a TikTok post, don't add another.
   - **tiktokData.title (required by Metricool):** `Shinobi Quiz: B-RANK MISSION 📜` for the HARD post, `Shinobi Quiz: S-RANK MISSION 🔥📜` for the EXTREME post. Never put the answer in the title.
   - **Caption: the Naruto account's OWN "mission briefing" voice.** It must NOT reuse the One Piece account's wording ("Guess That Character", "HARD MODE 💀", "swipe through all 5 clues", "I'll pin the answer later", "who should I do next?", "got it on clue 1 = genius", skull emojis). Always a LONG description, 1,000–1,800 characters (owner's standing request), no line breaks (the TikTok API strips them), ending with
     `#naruto #narutoshippuden #narutoquiz #animequiz #shinobi #animetiktok`.
     Write it as a ninja mission briefing. It must include, in your own fresh wording each day (vary the sentences; don't paste the same caption twice):
     - the mission rank up front (and mention it's a video quiz: "watch to the end") ("📜 MISSION BRIEFING: B-RANK" / "📜 MISSION BRIEFING: S-RANK 🔥")
     - a target teaser about the character type that gives nothing away (never names, villages, clans, teams or jutsu)
     - "5 scrolls, hardest to easiest" (unroll / open every scroll)
     - "drop your guess AND the scroll number that gave it away"
     - "answer gets pinned once the mission ends"
     - a no-googling line in ninja terms (e.g. "no peeking, no copy ninja tactics, no search engine jutsu")
     - the rank brag ladder matching the slides: scroll 1 = Kage level, 2 = Jonin, 3 = Chunin, 4 = Genin, 5 = back to the Academy
     - "tag your squad / your teammate who thinks they know every shinobi"
     - "which shinobi should be the next target?"
     - "Follow for a new mission every day at 12 PM and 12 AM ET."
     Use only these emojis, sparingly: 📜 🔥 🍥 🥷 🎯 🍃. Example of the voice (do not copy verbatim):
     `📜 MISSION BRIEFING: S-RANK 🔥 Your target today is a face most fans forgot the second their arc ended, but they mattered more than you think. Intel has been split across 5 scrolls, hardest to easiest, so unroll every one before you lock in. Drop your guess AND the scroll number that gave it away in the comments 🎯 Answer gets pinned once the mission ends, so no edits after the reveal. Rules of engagement: no peeking, no copy ninja tactics, no search engine jutsu. Your rank depends on where you cracked it: scroll 1 = Kage level, scroll 2 = Jonin, scroll 3 = Chunin, scroll 4 = Genin, scroll 5 = straight back to the Academy 🥷 ...`
   - **firstCommentText:** leave empty. Don't reveal the answer.
10. **Record:**
   - Append both names to `used.txt` with the date and scheduled time.
   - Add the answers to `answers.md` (date, time, character, clues), so the owner can pin them.
   - Commit and push.
11. **Report** in one short message which characters were scheduled for which times and their answers.
