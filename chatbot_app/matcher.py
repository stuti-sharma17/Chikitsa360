"""
Fuzzy keyword matcher for the hardcoded AyurBot demo.

Uses Python's built-in ``difflib`` — no extra dependencies needed.
Strategy:
  1. Normalize the user query (lowercase, strip punctuation).
  2. For each Q&A entry, compute the best similarity score between
     the query and every keyword phrase.
  3. Also do a token-overlap check so short keyword hits still rank
     well (e.g. user types "turmeric" → matches the turmeric entry).
  4. Return the answer for the highest-scoring entry, falling back
     to the generic response when no entry exceeds the threshold.
"""

import re
import difflib
import hashlib
import random

from .responses import QA_PAIRS, FALLBACK_RESPONSE, SAFETY_NOTE

# Minimum score (0–1) to accept a match instead of returning fallback
# Slightly lower because we add bonuses for strong lexical hits
_MATCH_THRESHOLD = 0.45
_GENERIC_MATCH_TOKENS = {
    "pain",
    "ache",
    "problem",
    "problems",
    "issue",
    "issues",
    "symptom",
    "symptoms",
    "disease",
    "diseases",
    "condition",
    "conditions",
    "remedy",
    "remedies",
    "treatment",
    "ayurveda",
    "ayurvedic",
    "health",
    "care",
    "help",
}
_BODY_PART_PAIN_RE = re.compile(
    r"^(?:(?:pain|ache)\s+in\s+)?(?P<body_part>[a-z][a-z\s-]{1,40})\s+(?P<symptom>pain|ache)$"
)
_HIGH_RISK_BODY_PARTS = {
    "brain",
    "head",
    "chest",
    "heart",
    "abdomen",
    "stomach",
    "eye",
    "eyes",
    "testicle",
    "testicles",
}
_GREETING_TOKENS = {"hi", "hello", "hey", "namaste", "greetings"}
_FRESH_OPENERS = [
    "Here is an Ayurveda-focused overview:",
    "Here is a practical Ayurveda take:",
    "AyurBot guidance (general wellness):",
    "Based on your query, here is a supportive Ayurveda response:",
]
_REPEAT_OPENERS = [
    "Another way to look at this (Ayurveda perspective):",
    "Same topic, but here is a slightly different explanation:",
    "Here is a refresher with a different wording:",
    "Let me frame this again in a simpler way:",
]
_FOLLOW_UP_PROMPTS = {
    "pain": [
        "If you want a better suggestion, tell me the exact location, duration, swelling, fever, injury history, and pain severity (1-10).",
        "You can also share whether the pain is sharp/dull, with swelling, numbness, or after an injury.",
        "For pain issues, details like duration, movement restriction, and swelling help me guide more specifically.",
    ],
    "digestion": [
        "You can share your symptoms (bloating, constipation, acidity, appetite, bowel pattern) for a more specific Ayurveda routine.",
        "If digestion is the concern, tell me whether it is acidity, gas, constipation, loose motions, or low appetite.",
    ],
    "sleep": [
        "If sleep is the main issue, tell me sleep timing, stress level, caffeine intake, and whether you wake up at night.",
        "You can share if the problem is falling asleep, frequent waking, or early-morning waking.",
    ],
    "stress": [
        "If stress/anxiety is the issue, tell me sleep quality, appetite, palpitations, and how long it has been happening.",
        "You can share if you also have headaches, acidity, poor sleep, or fatigue so I can tailor the guidance.",
    ],
    "general": [
        "If you want a more personalized answer, tell me age, main symptoms, duration, and any known medical conditions.",
        "You can ask a follow-up with more detail (symptoms, duration, severity, triggers) for a better response.",
        "I can make this more specific if you share your main symptom, how long it has been happening, and any medicines you take.",
    ],
}
_FALLBACK_INTROS = [
    "I may not have a direct answer for that exact wording yet, but I can still help.",
    "I could not confidently match that query, so here are the closest Ayurveda topics I can help with.",
    "That wording is a bit outside my current quick-response set. Try one of these supported topics.",
]
_FALLBACK_BUCKET_SUGGESTIONS = {
    "pain": [
        "Try: <b>headache</b>, <b>back pain</b>, <b>joint pain</b>, <b>shoulder pain</b>, <b>migraine</b>",
        "Try: <b>cold and cough</b>, <b>fever</b>, <b>allergy</b>, <b>sinus</b>, <b>stress</b> (if pain is stress-related)",
    ],
    "digestive": [
        "Try: <b>improve digestion</b>, <b>bloating remedy</b>, <b>constipation ayurveda</b>, <b>agni</b>",
        "Try: <b>ayurvedic diet</b>, <b>triphala</b>, <b>acidity</b> (describe it), <b>digestive health</b>",
    ],
    "metabolic": [
        "Try: <b>diabetes</b>, <b>high blood sugar</b>, <b>weight loss</b>, <b>thyroid</b>, <b>fatty liver</b>",
        "Try: <b>high blood pressure</b>, <b>cholesterol</b>, <b>immunity</b>, <b>liver health</b>",
    ],
    "general": [
        "Try: <b>doshas</b>, <b>prakriti</b>, <b>immunity</b>, <b>stress relief</b>, <b>sleep problems</b>",
        "Try: <b>skin care</b>, <b>cold and cough</b>, <b>ayurvedic diet</b>, <b>dinacharya</b>, <b>yoga</b>",
    ],
}
_RESPONSE_MODES = {"short", "medium", "detailed"}
_LANGUAGE_STYLE_ALIASES = {
    "english": "english",
    "en": "english",
    "hinglish": "hinglish",
    "hindi-english": "hinglish",
    "hindi english": "hinglish",
    "mixed": "hinglish",
    "mix": "hinglish",
}
_RED_FLAG_PATTERNS = [
    re.compile(r"\bchest pain\b"),
    re.compile(r"\bshortness of breath\b"),
    re.compile(r"\bbreathless(?:ness)?\b"),
    re.compile(r"\bdifficulty breathing\b"),
    re.compile(r"\bslurred speech\b"),
    re.compile(r"\bone side weakness\b"),
    re.compile(r"\bfaint(?:ing|ed)?\b"),
    re.compile(r"\bseizure\b"),
    re.compile(r"\bunconscious\b"),
    re.compile(r"\bsevere headache\b"),
    re.compile(r"\bhead injury\b"),
    re.compile(r"\bstroke\b"),
    re.compile(r"\bsevere bleeding\b"),
    re.compile(r"\bblack stool\b"),
    re.compile(r"\bblood vomiting\b"),
]
_RED_FLAG_TOKEN_HINTS = {
    "chest",
    "heart",
    "breathing",
    "breathless",
    "stroke",
    "seizure",
    "fainting",
    "fainted",
    "unconscious",
    "bleeding",
}
_DETAILED_NEXT_STEPS = {
    "pain": [
        "Track pain severity (1-10), exact location, and what movements worsen it.",
        "Avoid self-medicating long-term without diagnosis if pain is recurring.",
        "Share swelling, redness, fever, numbness, or injury history for better guidance.",
    ],
    "digestion": [
        "Note meal timing, food triggers, bowel pattern, and sleep schedule.",
        "Prefer warm, freshly prepared meals and avoid overeating late night.",
        "Tell me if the issue is acidity, gas, constipation, or loose stools.",
    ],
    "sleep": [
        "Track bedtime, wake time, caffeine intake, and screen use before sleep.",
        "Keep a consistent sleep routine for at least 1-2 weeks.",
        "Share whether the issue is sleep onset, night waking, or early waking.",
    ],
    "stress": [
        "Track triggers, sleep quality, appetite changes, and palpitations.",
        "Daily breathing + routine stabilization usually helps more than one-time remedies.",
        "Share if you also have headache, acidity, or poor sleep.",
    ],
    "metabolic": [
        "Use lab reports and doctor follow-up; do not rely on symptoms alone.",
        "Lifestyle changes work best when tracked weekly (sleep, diet, activity, weight).",
        "Share your recent reports (sugar, thyroid, lipids, liver/kidney markers) for better guidance.",
    ],
    "general": [
        "Share age, main symptom, duration, severity, and known medical conditions.",
        "Mention current medicines before trying herbal formulations.",
        "If symptoms are severe or persistent, consult a doctor for diagnosis first.",
    ],
}


def _normalize(text: str) -> str:
    """Lowercase, collapse whitespace, strip non-alpha chars."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _normalize_response_mode(response_mode: str | None) -> str:
    mode = (response_mode or "medium").strip().lower()
    return mode if mode in _RESPONSE_MODES else "medium"


def _normalize_language_style(language_style: str | None) -> str:
    style = (language_style or "english").strip().lower().replace("_", "-")
    return _LANGUAGE_STYLE_ALIASES.get(style, "english")


def _is_hinglish(language_style: str) -> bool:
    return _normalize_language_style(language_style) == "hinglish"


def _extract_html_list_items(answer_text: str) -> list[str]:
    return re.findall(r"<li>(.*?)</li>", answer_text, flags=re.IGNORECASE | re.DOTALL)


def _apply_response_mode(
    answer_text: str,
    query_tokens: set,
    response_mode: str,
    language_style: str,
) -> str:
    mode = _normalize_response_mode(response_mode)
    if mode == "medium":
        return answer_text

    list_items = _extract_html_list_items(answer_text)
    if mode == "short":
        if list_items:
            keep_n = 2
            prefix = answer_text.split("<ul>", 1)[0]
            compact = prefix + "<ul>" + "".join(
                f"<li>{item}</li>" for item in list_items[:keep_n]
            ) + "</ul>"
            if len(list_items) > keep_n:
                more_text = (
                    "Need more detail? Ask in <b>detailed mode</b>."
                    if not _is_hinglish(language_style)
                    else "Aur detail chahiye? <b>detailed mode</b> me poochho."
                )
                compact += (
                    "<small style='color:rgba(255,255,255,0.68);display:block;margin-top:0.35rem;'>"
                    + more_text
                    + "</small>"
                )
            return compact
        return answer_text

    # detailed mode
    intent = _intent_bucket(query_tokens)
    next_steps = _DETAILED_NEXT_STEPS.get(intent, _DETAILED_NEXT_STEPS["general"])
    title = "Next Steps (Practical)" if not _is_hinglish(language_style) else "Next Steps (Practical / Kya karein)"
    block_intro = (
        "Use these details to make the advice safer and more personalized:"
        if not _is_hinglish(language_style)
        else "Yeh details dene se advice zyada safe aur personalized ho sakti hai:"
    )
    detailed_block = (
        "<br><div style='margin-top:0.4rem;padding:0.6rem 0.7rem;border-radius:12px;"
        "background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);'>"
        f"<b>{title}</b><br>"
        f"<small style='color:rgba(255,255,255,0.72);'>{block_intro}</small>"
        "<ul>"
        + "".join(f"<li>{item}</li>" for item in next_steps)
        + "</ul></div>"
    )
    return answer_text + detailed_block


def _token_overlap(query_tokens: set, keyword_tokens: set) -> float:
    """Jaccard-like overlap biased towards shorter keyword phrases."""
    if not keyword_tokens:
        return 0.0
    common = query_tokens & keyword_tokens
    # How much of the keyword is covered by the query?
    return len(common) / len(keyword_tokens)


def _specific_tokens(tokens: set) -> set:
    return {
        token
        for token in tokens
        if token and token not in _GENERIC_MATCH_TOKENS and not token.isdigit()
    }


def _has_close_token_match(query_tokens: set, keyword_tokens: set, threshold: float = 0.82) -> bool:
    for q_token in query_tokens:
        for kw_token in keyword_tokens:
            if difflib.SequenceMatcher(None, q_token, kw_token).ratio() >= threshold:
                return True
    return False


def _extract_body_part_pain(query: str):
    match = _BODY_PART_PAIN_RE.match(query)
    if not match:
        return None
    body_part = re.sub(r"\s+", " ", match.group("body_part")).strip()
    if not body_part or body_part in _GENERIC_MATCH_TOKENS:
        return None
    return body_part, match.group("symptom")


def _generic_body_part_pain_response(body_part: str, language_style: str = "english") -> str:
    body_part_label = body_part.title()
    hinglish = _is_hinglish(language_style)

    urgency_line = (
        "<li><b>Urgent care:</b> sudden severe "
        + body_part
        + (
            " pain, weakness/numbness, fever, swelling after injury, or severe persistent pain needs medical evaluation quickly</li>"
            if not hinglish
            else " pain, weakness/numbness, fever, ya injury ke baad swelling ho to doctor se jaldi evaluation karaiye</li>"
        )
    )
    if body_part in _HIGH_RISK_BODY_PARTS:
        urgency_line = (
            "<li><b>Urgent care:</b> pain involving the "
            + body_part
            + (
                " can be serious. If severe, sudden, associated with vomiting, fainting, confusion, vision change, breathing trouble, or chest pain, seek immediate medical care.</li>"
                if not hinglish
                else " area serious ho sakta hai. Agar severe/sudden ho ya vomiting, fainting, confusion, vision change, breathing trouble, ya chest pain ke saath ho to immediate medical care lijiye.</li>"
            )
        )

    title = (
        f"For <b>{body_part_label} pain</b> (general supportive guidance):"
        if not hinglish
        else f"<b>{body_part_label} pain</b> ke liye (general supportive guidance):"
    )
    line1 = (
        "Rest the area and avoid activities that worsen the pain"
        if not hinglish
        else "Affected area ko rest dein aur jo activity pain badhati hai use avoid karein"
    )
    line2 = (
        "If there is <b>stiffness</b> (no swelling/redness), gentle warmth and light massage may help"
        if not hinglish
        else "Agar <b>stiffness</b> ho (swelling/redness na ho), gentle warmth aur light massage help kar sakta hai"
    )
    line3 = (
        "If there is <b>recent injury, swelling, or heat</b>, use a cold compress first and avoid strong massage"
        if not hinglish
        else "Agar <b>recent injury, swelling, ya heat</b> ho to pehle cold compress use karein aur strong massage avoid karein"
    )
    line4 = (
        "Supportive Ayurveda routine: warm meals, hydration, good sleep, and gentle movement as tolerated"
        if not hinglish
        else "Supportive Ayurveda routine: warm meals, hydration, achchi sleep, aur gentle movement as tolerated"
    )
    line5 = (
        "Please share more details (duration, injury, swelling, fever, exact location) for a more specific suggestion"
        if not hinglish
        else "Aur specific suggestion ke liye duration, injury, swelling, fever, aur exact location share karein"
    )

    return (
        title
        + "<ul>"
        + f"<li>{line1}</li>"
        + f"<li>{line2}</li>"
        + f"<li>{line3}</li>"
        + f"<li>{line4}</li>"
        + f"<li>{line5}</li>"
        + urgency_line
        + "</ul>"
    )


def _stable_rng(query: str, repeat_count: int) -> random.Random:
    digest = hashlib.sha256(f"{query}|{repeat_count}".encode("utf-8")).hexdigest()
    return random.Random(int(digest[:16], 16))


def _is_greeting_query(query_tokens: set) -> bool:
    return bool(query_tokens and query_tokens <= _GREETING_TOKENS)


def _intent_bucket(query_tokens: set) -> str:
    if query_tokens & {"pain", "ache", "migraine", "headache"}:
        return "pain"
    if query_tokens & {"digestion", "agni", "bloating", "constipation", "acidity"}:
        return "digestion"
    if query_tokens & {"sleep", "insomnia", "nidra"}:
        return "sleep"
    if query_tokens & {"stress", "anxiety", "calm"}:
        return "stress"
    if query_tokens & {"diabetes", "sugar", "thyroid", "cholesterol", "bp", "blood", "weight"}:
        return "metabolic"
    return "general"


def _needs_red_flag_alert(query: str, query_tokens: set) -> bool:
    if any(pattern.search(query) for pattern in _RED_FLAG_PATTERNS):
        return True
    if "pain" in query_tokens and bool(query_tokens & _RED_FLAG_TOKEN_HINTS):
        return True
    return False


def _doctor_safe_alert_template(query: str, language_style: str) -> str:
    if _is_hinglish(language_style):
        heading = "Doctor-Safe Alert (Important)"
        body = (
            "Agar symptom severe hai, achanak start hua hai, ya breathing issue / fainting / chest pain / weakness / confusion ke saath hai, "
            "to home remedies par depend mat kariye - doctor ya emergency care turant lijiye."
        )
        bullets = [
            "Severe ya worsening pain",
            "Breathing problem, chest pain, fainting, seizure",
            "Sudden weakness, confusion, slurred speech",
            "High fever, uncontrolled bleeding, repeated vomiting",
        ]
    else:
        heading = "Doctor-Safe Alert (Important)"
        body = (
            "If the symptom is severe, sudden, worsening, or associated with breathing difficulty, chest pain, fainting, weakness, or confusion, "
            "do not rely only on home remedies. Seek urgent medical care."
        )
        bullets = [
            "Severe or rapidly worsening pain",
            "Breathing trouble, chest pain, fainting, seizure",
            "Sudden weakness, confusion, slurred speech",
            "High fever, uncontrolled bleeding, repeated vomiting",
        ]

    return (
        "<div style='margin-top:0.45rem;padding:0.65rem 0.75rem;border-radius:12px;"
        "background:rgba(231,76,60,0.10);border:1px solid rgba(231,76,60,0.35);'>"
        f"<b>{heading}</b><br>"
        f"<small style='color:rgba(255,255,255,0.78);'>{body}</small>"
        "<ul style='margin-top:0.4rem;'>"
        + "".join(f"<li>{item}</li>" for item in bullets)
        + "</ul></div>"
    )


def _dynamic_fallback_response(
    query: str,
    query_tokens: set,
    repeat_count: int,
    response_mode: str = "medium",
    language_style: str = "english",
) -> str:
    mode = _normalize_response_mode(response_mode)
    style = _normalize_language_style(language_style)
    rng = _stable_rng(query, repeat_count)
    if style == "hinglish":
        fallback_intros = [
            "Is exact wording ka direct match mujhe nahi mila, but main help kar sakta hoon.",
            "Is query ka confident match nahi mila, to yeh closest Ayurveda topics try karo.",
            "Yeh wording mere quick-response set se thodi bahar hai. In supported topics me try karo.",
        ]
    else:
        fallback_intros = _FALLBACK_INTROS

    if repeat_count > 0:
        intro = fallback_intros[(repeat_count - 1) % len(fallback_intros)]
    else:
        intro = rng.choice(fallback_intros)
    bucket = _intent_bucket(query_tokens)
    suggestions = list(_FALLBACK_BUCKET_SUGGESTIONS.get(bucket, []))
    if bucket != "general":
        suggestions.extend(_FALLBACK_BUCKET_SUGGESTIONS["general"])
    rng.shuffle(suggestions)
    if mode == "short":
        suggestions = suggestions[:1]
    elif mode == "detailed":
        suggestions = suggestions[:3]
    else:
        suggestions = suggestions[:2]

    repeat_note = ""
    if repeat_count > 0:
        repeat_note_text = (
            "I noticed you asked a similar question again. Try adding more detail (symptom + duration + severity + triggers) for a more specific reply."
            if style != "hinglish"
            else "Aapne similar question phir poocha hai. Better reply ke liye symptom + duration + severity + triggers add karein."
        )
        repeat_note = (
            "<br><small style='color:rgba(255,255,255,0.68);display:block;margin-top:0.35rem;'>"
            + repeat_note_text
            + "</small>"
        )

    upload_line = (
        "You can also upload a report (PDF/image) for report-based guidance."
        if style != "hinglish"
        else "Aap report (PDF/image) upload karke report-based guidance bhi le sakte hain."
    )

    response = (
        intro
        + "<ul>"
        + "".join(f"<li>{item}</li>" for item in suggestions)
        + "</ul>"
        + upload_line
        + repeat_note
    )
    if mode == "detailed":
        ask_better = (
            "Better query format: symptom + duration + severity + triggers + age + known conditions"
            if style != "hinglish"
            else "Better query format: symptom + duration + severity + triggers + age + known conditions"
        )
        response += (
            "<br><small style='color:rgba(255,255,255,0.72);display:block;margin-top:0.35rem;'>"
            + ask_better
            + "</small>"
        )
    if _needs_red_flag_alert(query, query_tokens):
        response += _doctor_safe_alert_template(query, style)
    return response


def _format_answer_response(
    answer_text: str,
    query: str,
    query_tokens: set,
    repeat_count: int,
    response_mode: str = "medium",
    language_style: str = "english",
) -> str:
    mode = _normalize_response_mode(response_mode)
    style = _normalize_language_style(language_style)
    answer_text = _apply_response_mode(answer_text, query_tokens, mode, style)

    if _is_greeting_query(query_tokens):
        if _needs_red_flag_alert(query, query_tokens):
            answer_text += _doctor_safe_alert_template(query, style)
        return answer_text

    rng = _stable_rng(query, repeat_count)
    fresh_openers = _FRESH_OPENERS
    repeat_openers = _REPEAT_OPENERS
    if style == "hinglish":
        fresh_openers = [
            "Yeh raha Ayurveda-focused overview:",
            "Practical Ayurveda take (general guidance):",
            "AyurBot se supportive guidance:",
            "Aapke query ke basis par yeh Ayurveda response hai:",
        ]
        repeat_openers = [
            "Isi topic ko ek aur tarike se samjhte hain (Ayurveda view):",
            "Same topic, but thoda different wording me:",
            "Chaliye isko phir se simple way me dekhte hain:",
            "Refresher answer (Ayurveda perspective):",
        ]

    opener_pool = repeat_openers if repeat_count > 0 else fresh_openers
    if repeat_count > 0:
        opener = opener_pool[(repeat_count - 1) % len(opener_pool)]
    else:
        opener = rng.choice(opener_pool)
    followups = _FOLLOW_UP_PROMPTS.get(_intent_bucket(query_tokens), _FOLLOW_UP_PROMPTS["general"])
    if style == "hinglish":
        followups = {
            "pain": [
                "Better suggestion ke liye exact location, duration, swelling, fever, injury history, aur pain severity (1-10) batayein.",
                "Yeh bhi batayein pain sharp hai ya dull, swelling/numbness hai ya injury ke baad start hua.",
                "Pain cases me duration, movement restriction aur swelling details helpful hoti hain.",
            ],
            "digestion": [
                "Digestive issue me bloating, constipation, acidity, appetite aur bowel pattern share karein.",
                "Batayein problem acidity/gas/constipation/loose motions/low appetite me se kya hai.",
            ],
            "sleep": [
                "Sleep issue me sleep timing, stress level, caffeine intake, aur night waking details share karein.",
                "Yeh batayein problem sleep aane me hai, beech me jagne me, ya jaldi uthne me.",
            ],
            "stress": [
                "Stress/anxiety ke saath sleep, appetite, palpitations aur duration batayein.",
                "Headache/acidity/poor sleep/fatigue bhi ho to mention karein for better guidance.",
            ],
            "general": [
                "More personalized reply ke liye age, main symptoms, duration, severity, aur conditions share karein.",
                "Follow-up me symptom + duration + severity + triggers likhen to answer better hoga.",
                "Medicines le rahe hain to woh bhi mention karein before herbal suggestions.",
            ],
        }.get(_intent_bucket(query_tokens), _FOLLOW_UP_PROMPTS["general"])
    if repeat_count > 0:
        followup = followups[(repeat_count - 1) % len(followups)]
    else:
        followup = rng.choice(followups)

    # Rotate light response framing styles so repeat answers look less template-like.
    style_mode = repeat_count % 3 if repeat_count > 0 else rng.randint(0, 2)
    opener_html = (
        "<small style='color:rgba(255,255,255,0.72);display:block;margin-bottom:0.35rem;'>"
        + opener
        + "</small>"
    )
    followup_html = (
        "<br><small style='color:rgba(255,255,255,0.70);display:block;margin-top:0.35rem;'>"
        + followup
        + "</small>"
    )

    if style_mode == 0:
        formatted = opener_html + answer_text + followup_html
    elif style_mode == 1:
        formatted = answer_text + followup_html
    else:
        formatted = opener_html + answer_text

    if _needs_red_flag_alert(query, query_tokens):
        formatted += _doctor_safe_alert_template(query, style)
    return formatted


def get_best_match(
    user_input: str,
    repeat_count: int = 0,
    response_mode: str = "medium",
    language_style: str = "english",
) -> str:
    """Return the best hardcoded answer for *user_input*, or FALLBACK_RESPONSE."""

    query = _normalize(user_input)
    mode = _normalize_response_mode(response_mode)
    style = _normalize_language_style(language_style)
    if not query:
        return _dynamic_fallback_response(query, set(), repeat_count, mode, style) + SAFETY_NOTE

    query_tokens = set(query.split())
    best_score = 0.0
    best_entry = None
    best_keyword_tokens = set()

    for entry in QA_PAIRS:
        entry_best = 0.0
        entry_best_keyword_tokens = set()
        for keyword_phrase in entry["keywords"]:
            norm_kw = _normalize(keyword_phrase)

            # Sequence similarity (handles typos and close phrasings)
            seq_score = difflib.SequenceMatcher(None, query, norm_kw).ratio()

            # Token overlap (handles single-word or partial queries)
            kw_tokens = set(norm_kw.split())
            overlap_score = _token_overlap(query_tokens, kw_tokens)
            shared_tokens = kw_tokens & query_tokens
            shared_specific = _specific_tokens(kw_tokens) & _specific_tokens(query_tokens)

            # Bonus if keyword appears as whole phrase or query is contained in keyword
            bonus = 0.0
            if norm_kw and (norm_kw in query or query in norm_kw):
                bonus += 0.25
            # Bonus if any keyword token is exactly in the query tokens
            if shared_specific:
                bonus += 0.1
            elif shared_tokens:
                # Small bonus for generic overlap like "pain", but don't let it dominate body-part mismatches.
                bonus += 0.02
                if _specific_tokens(query_tokens) and _specific_tokens(kw_tokens):
                    bonus -= 0.08

            combined = max(seq_score, overlap_score) + bonus
            if combined > entry_best:
                entry_best = combined
                entry_best_keyword_tokens = kw_tokens

        if entry_best > best_score:
            best_score = entry_best
            best_entry = entry
            best_keyword_tokens = entry_best_keyword_tokens

    if best_score < _MATCH_THRESHOLD:
        body_part_pain = _extract_body_part_pain(query)
        if body_part_pain:
            response_text = _generic_body_part_pain_response(body_part_pain[0], style)
            response_text = _format_answer_response(
                response_text, query, query_tokens, repeat_count, mode, style
            )
            return response_text + SAFETY_NOTE
        return _dynamic_fallback_response(query, query_tokens, repeat_count, mode, style) + SAFETY_NOTE

    # Support optional answer variants
    if best_entry is None:
        return _dynamic_fallback_response(query, query_tokens, repeat_count, mode, style) + SAFETY_NOTE

    # Generic fuzzy matching can produce false positives for unrelated text
    # (e.g. "unknown xyz symptom" ~ "know my dosha"). Require either meaningful
    # token overlap or a stronger similarity score to accept such matches.
    query_specific = _specific_tokens(query_tokens)
    match_specific = _specific_tokens(best_keyword_tokens)
    if query_specific and match_specific and not (query_specific & match_specific):
        if _has_close_token_match(query_specific, match_specific):
            pass
        elif best_score < 0.72:
            return _dynamic_fallback_response(query, query_tokens, repeat_count, mode, style) + SAFETY_NOTE

    # If the query is a body-part pain query and the best match only overlaps generic tokens
    # (e.g. "brain pain" accidentally matching "back pain"), return a safer generic pain response.
    body_part_pain = _extract_body_part_pain(query)
    if body_part_pain:
        if not (query_specific & match_specific) and not _has_close_token_match(query_specific, match_specific):
            response_text = _generic_body_part_pain_response(body_part_pain[0], style)
            response_text = _format_answer_response(
                response_text, query, query_tokens, repeat_count, mode, style
            )
            return response_text + SAFETY_NOTE

    if "answers" in best_entry and best_entry["answers"]:
        answers = best_entry["answers"]
        if repeat_count > 0:
            rng = _stable_rng(query, repeat_count)
            answer_text = answers[rng.randrange(len(answers))]
        else:
            answer_text = random.choice(answers)
    else:
        answer_text = best_entry["answer"]

    answer_text = _format_answer_response(
        answer_text, query, query_tokens, repeat_count, mode, style
    )
    return answer_text + SAFETY_NOTE
