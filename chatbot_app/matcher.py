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

from .responses import QA_PAIRS, FALLBACK_RESPONSE

# Minimum score (0–1) to accept a match instead of returning fallback
_MATCH_THRESHOLD = 0.50


def _normalize(text: str) -> str:
    """Lowercase, collapse whitespace, strip non-alpha chars."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _token_overlap(query_tokens: set, keyword_tokens: set) -> float:
    """Jaccard-like overlap biased towards shorter keyword phrases."""
    if not keyword_tokens:
        return 0.0
    common = query_tokens & keyword_tokens
    # How much of the keyword is covered by the query?
    return len(common) / len(keyword_tokens)


def get_best_match(user_input: str) -> str:
    """Return the best hardcoded answer for *user_input*, or FALLBACK_RESPONSE."""

    query = _normalize(user_input)
    if not query:
        return FALLBACK_RESPONSE

    query_tokens = set(query.split())
    best_score = 0.0
    best_answer = FALLBACK_RESPONSE

    for entry in QA_PAIRS:
        for keyword_phrase in entry["keywords"]:
            norm_kw = _normalize(keyword_phrase)

            # Sequence similarity (handles typos and close phrasings)
            seq_score = difflib.SequenceMatcher(None, query, norm_kw).ratio()

            # Token overlap (handles single-word or partial queries)
            kw_tokens = set(norm_kw.split())
            overlap_score = _token_overlap(query_tokens, kw_tokens)

            # Combined score — favour whichever metric is better
            combined = max(seq_score, overlap_score)

            if combined > best_score:
                best_score = combined
                best_answer = entry["answer"]

    if best_score < _MATCH_THRESHOLD:
        return FALLBACK_RESPONSE

    return best_answer
