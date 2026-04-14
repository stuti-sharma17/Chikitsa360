"""
Hardcoded Q&A pairs for the AyurBot demo.

Each entry maps a list of trigger phrases to a concise HTML-formatted
Ayurvedic answer.  Answers use simple HTML so they render as styled
lists in the chat UI.
"""

QA_PAIRS = [
    # -- 0. Greetings --
    {
        "keywords": [
            "hello", "hi", "hey", "good morning", "good evening",
            "hello there", "namaste", "greetings",
        ],
        "answer": (
            "Namaste! 🙏 I'm <b>AyurBot</b> — your Ayurvedic health assistant."
            "<br><br>Try asking me:"
            "<ul>"
            "<li>What is Ayurveda?</li>"
            "<li>Tell me about Ashwagandha</li>"
            "<li>How to boost immunity?</li>"
            "<li>Ayurvedic remedies for stress</li>"
            "</ul>"
        ),
    },
    # -- 1. What is Ayurveda --
    {
        "keywords": [
            "what is ayurveda", "explain ayurveda", "tell me about ayurveda",
            "define ayurveda", "ayurveda meaning", "introduction to ayurveda",
        ],
        "answer": (
            "<b>Ayurveda</b> — the 'Science of Life' — is a 5,000-year-old "
            "holistic healing system from India."
            "<ul>"
            "<li>Balances <b>mind, body &amp; spirit</b> through diet, herbs, yoga &amp; meditation</li>"
            "<li>Built on three bio-energies called <b>Doshas</b> — Vata, Pitta, Kapha</li>"
            "<li>Focuses on <b>prevention</b> over cure</li>"
            "<li>Uses natural remedies &amp; personalised lifestyle practices</li>"
            "</ul>"
        ),
    },
    # -- 2. Three Doshas --
    {
        "keywords": [
            "what are the three doshas", "three doshas", "tell me about doshas",
            "explain doshas", "types of doshas", "dosha types",
            "about doshas", "vata pitta kapha",
        ],
        "answer": (
            "The <b>three Doshas</b> are the fundamental bio-energies in Ayurveda:"
            "<ul>"
            "<li><b>Vata</b> (Air + Space) — governs movement, creativity &amp; the nervous system</li>"
            "<li><b>Pitta</b> (Fire + Water) — governs digestion, metabolism &amp; intellect</li>"
            "<li><b>Kapha</b> (Earth + Water) — governs structure, stability &amp; immunity</li>"
            "</ul>"
            "Good health = keeping all three in balance."
        ),
    },
    # -- 3. Vata Dosha --
    {
        "keywords": [
            "what is vata dosha", "tell me about vata", "vata dosha",
            "vata characteristics", "vata imbalance",
        ],
        "answer": (
            "<b>Vata</b> (Air + Space) controls all movement in the body."
            "<ul>"
            "<li><b>Traits:</b> Light frame, creative, energetic, quick learner</li>"
            "<li><b>Imbalance signs:</b> Anxiety, dry skin, insomnia, bloating</li>"
            "<li><b>Balance tips:</b> Warm foods, regular routine, sesame oil massage</li>"
            "</ul>"
        ),
    },
    # -- 4. Pitta Dosha --
    {
        "keywords": [
            "what is pitta dosha", "tell me about pitta", "pitta dosha",
            "pitta characteristics", "pitta imbalance",
        ],
        "answer": (
            "<b>Pitta</b> (Fire + Water) governs digestion &amp; metabolism."
            "<ul>"
            "<li><b>Traits:</b> Medium build, sharp intellect, strong appetite, natural leader</li>"
            "<li><b>Imbalance signs:</b> Acid reflux, skin rashes, irritability, excess heat</li>"
            "<li><b>Balance tips:</b> Cooling foods (cucumber, coconut, mint), avoid spicy food</li>"
            "</ul>"
        ),
    },
    # -- 5. Kapha Dosha --
    {
        "keywords": [
            "what is kapha dosha", "tell me about kapha", "kapha dosha",
            "kapha characteristics", "kapha imbalance",
        ],
        "answer": (
            "<b>Kapha</b> (Earth + Water) provides structure &amp; stability."
            "<ul>"
            "<li><b>Traits:</b> Sturdy build, calm nature, excellent memory, steady energy</li>"
            "<li><b>Imbalance signs:</b> Weight gain, congestion, sluggishness, oversleeping</li>"
            "<li><b>Balance tips:</b> Vigorous exercise, light &amp; spicy foods, wake up early</li>"
            "</ul>"
        ),
    },
    # -- 6. Prakriti --
    {
        "keywords": [
            "what is prakriti", "prakriti", "body constitution",
            "ayurvedic constitution", "know my dosha", "determine my dosha",
        ],
        "answer": (
            "<b>Prakriti</b> is your unique Ayurvedic constitution — the dosha "
            "balance you're born with."
            "<ul>"
            "<li>Determined at birth; stays constant for life</li>"
            "<li>Guides your ideal <b>diet, lifestyle &amp; treatments</b></li>"
            "<li>Assessed via <b>pulse diagnosis</b> (Nadi Pariksha) by a practitioner</li>"
            "<li>Helps predict disease tendencies early</li>"
            "</ul>"
        ),
    },
    # -- 7. Panchakarma --
    {
        "keywords": [
            "what is panchakarma", "panchakarma", "panchakarma treatment",
            "detox ayurveda", "ayurvedic detox", "five actions",
        ],
        "answer": (
            "<b>Panchakarma</b> ('Five Actions') — Ayurveda's primary detox therapy:"
            "<ul>"
            "<li><b>Vamana</b> — therapeutic emesis (Kapha cleansing)</li>"
            "<li><b>Virechana</b> — purgation (Pitta cleansing)</li>"
            "<li><b>Basti</b> — medicated enema (Vata treatment)</li>"
            "<li><b>Nasya</b> — nasal herbal oil administration</li>"
            "</ul>"
            "Always done under professional supervision."
        ),
    },
    # -- 8. Turmeric --
    {
        "keywords": [
            "benefits of turmeric", "turmeric", "haldi", "curcumin",
            "turmeric uses", "turmeric in ayurveda",
        ],
        "answer": (
            "<b>Turmeric (Haldi)</b> — one of Ayurveda's most powerful herbs:"
            "<ul>"
            "<li>Strong <b>anti-inflammatory</b> &amp; antioxidant (active compound: curcumin)</li>"
            "<li>Boosts immunity &amp; aids digestion</li>"
            "<li>Promotes <b>glowing skin</b> &amp; wound healing</li>"
            "<li><b>Tip:</b> Take as Golden Milk with black pepper to boost absorption 20x</li>"
            "</ul>"
        ),
    },
    # -- 9. Ashwagandha --
    {
        "keywords": [
            "ashwagandha", "tell me about ashwagandha", "ashwagandha benefits",
            "withania somnifera", "indian ginseng",
        ],
        "answer": (
            "<b>Ashwagandha</b> ('Indian Ginseng') — a top Ayurvedic adaptogen:"
            "<ul>"
            "<li>Reduces <b>stress &amp; anxiety</b> by lowering cortisol</li>"
            "<li>Improves energy, strength &amp; stamina</li>"
            "<li>Enhances <b>memory &amp; sleep</b> quality</li>"
            "<li><b>Dosage:</b> 300-600 mg root extract daily, with warm milk at bedtime</li>"
            "</ul>"
        ),
    },
    # -- 10. Tulsi --
    {
        "keywords": [
            "tulsi benefits", "tulsi", "holy basil",
            "ocimum sanctum", "tulsi uses", "tulsi tea",
        ],
        "answer": (
            "<b>Tulsi (Holy Basil)</b> — the 'Queen of Herbs':"
            "<ul>"
            "<li>Relieves <b>cough, cold &amp; respiratory</b> issues</li>"
            "<li>Natural <b>immune booster</b> rich in antioxidants</li>"
            "<li>Acts as a <b>stress-relieving</b> adaptogen</li>"
            "<li><b>Tip:</b> Drink Tulsi tea daily or chew 4-5 fresh leaves on an empty stomach</li>"
            "</ul>"
        ),
    },
    # -- 11. Triphala --
    {
        "keywords": [
            "what is triphala", "triphala", "triphala benefits",
            "three fruits", "triphala churna",
        ],
        "answer": (
            "<b>Triphala</b> — a classic Ayurvedic blend of three fruits:"
            "<ul>"
            "<li><b>Amla</b> (Vitamin C), <b>Bibhitaki</b> &amp; <b>Haritaki</b></li>"
            "<li>Gentle <b>detox &amp; bowel cleanser</b></li>"
            "<li>Powerful antioxidant; supports eye health &amp; weight management</li>"
            "<li><b>Tip:</b> 1/2 tsp powder in warm water before bedtime</li>"
            "</ul>"
        ),
    },
    # -- 12. Digestion / Agni --
    {
        "keywords": [
            "improve digestion", "digestive health", "agni",
            "digestive fire", "indigestion ayurveda",
            "bloating remedy", "constipation ayurveda",
        ],
        "answer": (
            "<b>Agni</b> (digestive fire) is the cornerstone of health in Ayurveda:"
            "<ul>"
            "<li>Drink <b>warm water</b> throughout the day; avoid cold drinks with meals</li>"
            "<li>Chew fresh <b>ginger + lemon + salt</b> before meals to ignite Agni</li>"
            "<li>Use digestive spices: <b>cumin, coriander, fennel, ginger</b></li>"
            "<li>Eat your <b>largest meal at noon</b> when Agni is strongest</li>"
            "</ul>"
        ),
    },
    # -- 13. Immunity --
    {
        "keywords": [
            "boost immunity", "immunity", "improve immune system",
            "ayurvedic immunity", "ojas", "immune booster herbs",
        ],
        "answer": (
            "Ayurveda links immunity to <b>Ojas</b> — the vital essence of health:"
            "<ul>"
            "<li><b>Chyawanprash</b> — 1-2 tsp daily (Amla + 40 herbs)</li>"
            "<li><b>Giloy (Guduchi)</b> — known as 'the nectar herb'</li>"
            "<li><b>Golden Milk</b> — turmeric + warm milk + black pepper at bedtime</li>"
            "<li><b>Pranayama</b> — Kapalbhati &amp; Anulom-Vilom boost lung function</li>"
            "</ul>"
        ),
    },
    # -- 14. Stress & Anxiety --
    {
        "keywords": [
            "stress relief", "anxiety", "ayurvedic stress remedies",
            "calm mind", "mental health ayurveda", "reduce stress",
        ],
        "answer": (
            "Stress is a <b>Vata imbalance</b> in Ayurveda. Key remedies:"
            "<ul>"
            "<li><b>Ashwagandha</b> — lowers cortisol &amp; calms the mind</li>"
            "<li><b>Brahmi</b> — enhances cognition &amp; reduces anxiety</li>"
            "<li><b>Abhyanga</b> — warm sesame oil self-massage</li>"
            "<li><b>Daily yoga &amp; meditation</b> — even 15 min helps ground Vata</li>"
            "</ul>"
        ),
    },
    # -- 15. Sleep / Insomnia --
    {
        "keywords": [
            "insomnia", "sleep problems", "ayurvedic sleep remedies",
            "better sleep", "can't sleep", "nidra",
        ],
        "answer": (
            "<b>Sleep (Nidra)</b> is one of the three pillars of health:"
            "<ul>"
            "<li><b>Ashwagandha + warm milk</b> before bed promotes deep sleep</li>"
            "<li>A pinch of <b>nutmeg</b> in warm milk is a natural sedative</li>"
            "<li><b>Foot massage</b> with warm sesame oil calms the nervous system</li>"
            "<li>Maintain a regular schedule — <b>sleep by 10 PM</b></li>"
            "</ul>"
        ),
    },
    # -- 16. Skin Care --
    {
        "keywords": [
            "skin care", "ayurvedic skin care", "glowing skin",
            "acne ayurveda", "skin problems", "skin treatment",
        ],
        "answer": (
            "Skin health is linked to <b>Pitta dosha</b> &amp; blood purity:"
            "<ul>"
            "<li><b>Turmeric + honey mask</b> for glowing skin</li>"
            "<li><b>Neem</b> — anti-bacterial, great for acne</li>"
            "<li><b>Kumkumadi oil</b> — traditional Ayurvedic face oil for radiance</li>"
            "<li>Drink <b>warm lemon water</b> in the morning to flush toxins</li>"
            "</ul>"
        ),
    },
    # -- 17. Cold & Cough --
    {
        "keywords": [
            "cold and cough", "cough remedy", "common cold",
            "flu ayurveda", "sore throat", "running nose", "blocked nose",
        ],
        "answer": (
            "Cold &amp; cough = <b>Kapha imbalance</b>. Effective remedies:"
            "<ul>"
            "<li><b>Tulsi-Ginger tea</b> with black pepper &amp; honey</li>"
            "<li><b>Turmeric milk</b> (Golden Milk) before bed</li>"
            "<li><b>Steam inhalation</b> with eucalyptus or Tulsi leaves</li>"
            "<li>Avoid <b>cold foods, dairy &amp; fried items</b> during illness</li>"
            "</ul>"
        ),
    },
    # -- 18. Diet / Ahara --
    {
        "keywords": [
            "ayurvedic diet", "diet principles", "ahara",
            "food in ayurveda", "eating habits",
            "what to eat ayurveda", "healthy diet",
        ],
        "answer": (
            "In Ayurveda, <b>food is medicine</b>. Core diet principles:"
            "<ul>"
            "<li>Eat according to your <b>dosha</b> — Vata: warm, Pitta: cooling, Kapha: light</li>"
            "<li><b>Largest meal at noon</b> when Agni (digestive fire) peaks</li>"
            "<li>Include all <b>6 tastes</b> — sweet, sour, salty, pungent, bitter, astringent</li>"
            "<li>Eat <b>fresh, warm food</b>; avoid stale, processed or reheated meals</li>"
            "</ul>"
        ),
    },
    # -- 19. Yoga & Ayurveda --
    {
        "keywords": [
            "yoga and ayurveda", "yoga", "pranayama",
            "yoga benefits", "connection yoga ayurveda",
            "breathing exercises",
        ],
        "answer": (
            "<b>Yoga &amp; Ayurveda</b> are sister sciences — body + mind wellness:"
            "<ul>"
            "<li><b>Vata:</b> Gentle, grounding poses (Tadasana, slow Surya Namaskar)</li>"
            "<li><b>Pitta:</b> Cooling, calming poses (forward bends, Shavasana)</li>"
            "<li><b>Kapha:</b> Energising poses (backbends, Kapalbhati breathing)</li>"
            "<li><b>Pranayama:</b> Anulom-Vilom balances all doshas — practise daily</li>"
            "</ul>"
        ),
    },
    # -- 20. Dinacharya --
    {
        "keywords": [
            "dinacharya", "daily routine", "ayurvedic daily routine",
            "morning routine ayurveda", "ritucharya", "daily habits",
        ],
        "answer": (
            "<b>Dinacharya</b> — the ideal Ayurvedic daily routine:"
            "<ul>"
            "<li><b>Wake before sunrise</b> → tongue scrape → oil pulling → warm lemon water</li>"
            "<li><b>Abhyanga</b> (oil self-massage) before your morning bath</li>"
            "<li><b>Yoga + Pranayama</b> for 30-45 minutes</li>"
            "<li><b>Biggest meal at noon</b>, light dinner, sleep by 10 PM</li>"
            "</ul>"
        ),
    },
]


# -- Fallback response when no match is found --
FALLBACK_RESPONSE = (
    "I don't have a specific answer for that yet, but I can help with:"
    "<ul>"
    "<li>🌿 <b>Ayurveda basics</b> — Doshas, Prakriti, Dinacharya</li>"
    "<li>🌿 <b>Herbs</b> — Ashwagandha, Tulsi, Turmeric, Triphala</li>"
    "<li>🌿 <b>Treatments</b> — Panchakarma, digestion, immunity</li>"
    "<li>🌿 <b>Lifestyle</b> — Diet, yoga, sleep, stress, skin care</li>"
    "</ul>"
    "For personalised advice, book a consultation with a doctor on our platform."
)
