import os
from datetime import date, datetime, timezone, timedelta
from google import genai

# 1. Calculate Target Chapter using Thailand Time (UTC+7)
tz_th = timezone(timedelta(hours=7))
today = datetime.now(tz_th).date()
start_date = date(2026, 11, 2)
days_elapsed = (today - start_date).days

# Canonical NT Chapter Map starting from John 18
NT_BOOKS = [
    ("John", range(18, 22)),
    ("Acts", range(1, 29)),
    ("Romans", range(1, 17)),
    ("1-Corinthians", range(1, 17)),
    ("2-Corinthians", range(1, 14)),
    ("Galatians", range(1, 7)),
    ("Ephesians", range(1, 7)),
    ("Philippians", range(1, 5)),
    ("Colossians", range(1, 5)),
    ("1-Thessalonians", range(1, 6)),
    ("2-Thessalonians", range(1, 4)),
    ("1-Timothy", range(1, 7)),
    ("2-Timothy", range(1, 5)),
    ("Titus", range(1, 4)),
    ("Philemon", range(1, 2)),
    ("Hebrews", range(1, 14)),
    ("James", range(1, 6)),
    ("1-Peter", range(1, 6)),
    ("2-Peter", range(1, 4)),
    ("1-John", range(1, 6)),
    ("2-John", range(1, 2)),
    ("3-John", range(1, 2)),
    ("Jude", range(1, 2)),
    ("Revelation", range(1, 23)),
]

chapters = [f"{book}-{ch}" for book, ch_range in NT_BOOKS for ch in ch_range]
target_slug = chapters[days_elapsed % len(chapters)]
target_display = target_slug.replace("-", " ")

PROMPT = f"""Generate a complete, deep-dive 5-Lens Exegetical & Pedagogical Bible Study package for {target_display} (Day {days_elapsed}).
Strictly unpack the passage using this exact structure:
1. Phase 0: Pre-study illumination prayer and canonical macro-sweep (1-sentence thesis, literary structure, and context).
2. Phase 1 (The 5-Lens Exegetical Matrix):
   - Lens 1 (Linguistic & Textual Architecture): Greek morphological breakdown (tense, voice, mood) of 5-6 key terms, semantic range, and KJV/ESV/NASB comparison table.
   - Lens 2 (Historical, Cultural & Second Temple Context): First-century Greco-Roman/Jewish customs, Old Testament intertextual echoes, and Second Temple context.
   - Lens 3 (Geographical & Anthropological Grounding): Exact topography, spatial mechanics, and honor/shame or social dynamics.
   - Lens 4 (Philosophical & Doctrinal Logic): Deductive argument spine (Premises & Conclusion), systematic theology integration, and a mid-study Phase 2 Prayer (Meditation).
   - Lens 5 (Commentary Triangulation): Comparison table across Patristic/Classical, Contemporary Academic, and Apostolic/Expository (Kumuyi, Watchman Nee, Arome Osayi) streams.
3. Phase 2 (Praxis & 'Jesus' Arrows' Pedagogical Pipeline):
   - Personal & Family Application ('The Kneeling Christian' Filter) and Phase 3 Prayer Points for personal consecration and family protection.
   - 'Jesus' Arrows' Homeschool Curriculum Translation: The 1-sentence 'Big Idea', a concrete Visual/Narrative Object Lesson, Age-Tiered Dialectic Questions tailored for Age 6, Age 8, and Age 10, plus a Memory Verse Anchor with hand motions/hooks."""

# 2. Call Gemini API
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=PROMPT,
)

# 3. Save Markdown File
os.makedirs("studies", exist_ok=True)
filename = f"studies/{today.isoformat()}-{target_slug}.md"
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"# {target_display} — 5-Lens Exegetical & Pedagogical Study\n")
    f.write(f"**Date:** {today.isoformat()} (Day {days_elapsed})\n\n---\n\n")
    f.write(response.text)

# Export variables for GitHub Actions step
with open(os.environ["GITHUB_ENV"], "a") as env_file:
    env_file.write(f"STUDY_FILE={filename}\n")
    env_file.write(f"TARGET_CHAPTER={target_display}\n")
