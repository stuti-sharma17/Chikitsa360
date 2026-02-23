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
        "answers": [
            (
                "Namaste! 🙏 I'm <b>AyurBot</b> — your Ayurvedic health guide."
                "<br><br>Ask me about doshas, herbs, or daily routines to stay balanced."
            ),
            (
                "Hey there! 🤖 <b>AyurBot</b> here. I can help with Ayurvedic remedies, diet tips, and wellness routines."
                "<br>Try: <i>\"Ayurvedic remedy for stress\"</i> or <i>\"What is Ashwagandha?\"</i>"
            ),
            (
                "Welcome! 🌿 I'm <b>AyurBot</b>. Curious about your dosha, immunity boosters, or a weight-loss plan?"
                "<br>Type any health query and I'll share an Ayurvedic perspective."
            ),
        ],
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
    # -- 21. Dental / Oral health --
    {
        "keywords": [
            "dental health", "oral health", "tooth pain", "teeth care",
            "toothache remedy", "gum care", "oil pulling benefits", "mouth ulcers",
        ],
        "answer": (
            "Ayurvedic tips for <b>healthy teeth &amp; gums</b>:"
            "<ul>"
            "<li><b>Oil pulling</b> (sesame or coconut) for 5-10 min daily reduces plaque &amp; bad breath</li>"
            "<li><b>Triphala mouth rinse</b> soothes gums and mouth ulcers</li>"
            "<li><b>Clove oil</b> dab for toothache (temporary relief)</li>"
            "<li>Avoid excess <b>sugar &amp; acidic drinks</b>; sip warm water instead of cold sodas</li>"
            "<li>Chew <b>neem sticks</b> or use neem-based paste for antimicrobial care</li>"
            "</ul>"
        ),
    },
    # -- 22. Pollution — lungs & breathing --
    {
        "keywords": [
            "pollution", "air pollution", "breathing problems", "smog", "cough pollution",
            "pollution lungs", "pollution remedies", "asthma pollution",
        ],
        "answer": (
            "To protect lungs in <b>polluted air</b>:"
            "<ul>"
            "<li><b>Steam inhalation</b> with tulsi or eucalyptus clears mucus</li>"
            "<li><b>Turmeric + black pepper</b> in warm milk supports respiratory immunity</li>"
            "<li><b>Pippali (long pepper)</b> and <b>Vasaka</b> are traditional for cough &amp; breath ease</li>"
            "<li>Do <b>Anulom-Vilom &amp; Bhramari</b> pranayama daily to strengthen lungs</li>"
            "<li>Wear a <b>well-fitted mask</b> outdoors; keep indoor air clean with ventilation</li>"
            "</ul>"
        ),
    },
    # -- 22b. Brain health / focus / pollution effects --
    {
        "keywords": [
            "brain health", "mental clarity", "focus", "concentration", "memory",
            "brain fog", "pollution brain", "smog brain", "cognitive health",
        ],
        "answer": (
            "<b>Brain &amp; cognitive support</b> (esp. when feeling foggy or after pollution exposure):"
            "<ul>"
            "<li><b>Brahmi</b> and <b>Shankhpushpi</b> are classical medhya rasayanas for memory &amp; focus</li>"
            "<li><b>Ashwagandha</b> lowers stress cortisol that can cloud thinking</li>"
            "<li>Keep <b>hydrated</b>; add warm <b>ginger-lemon</b> water to improve circulation</li>"
            "<li>Do <b>alternate-nostril breathing (Anulom-Vilom)</b> for 5-7 minutes to clear mental fog</li>"
            "<li>Sleep 7-8 hours; reduce screens late night; add <b>walnuts &amp; ghee</b> for brain nourishment</li>"
            "</ul>"
        ),
    },
    # -- 23. Pollution — skin protection --
    {
        "keywords": [
            "pollution skin", "skin pollution", "dull skin pollution", "anti pollution skincare",
            "pollution face care", "skin barrier pollution",
        ],
        "answer": (
            "For <b>skin exposed to pollution</b>:"
            "<ul>"
            "<li>Cleanse with a gentle <b>gram flour + milk</b> paste; avoid harsh soaps</li>"
            "<li>Use <b>kumkumadi taila</b> or light facial oils to support the skin barrier</li>"
            "<li><b>Neem</b> or <b>manjistha</b> face packs help with acne &amp; detox</li>"
            "<li><b>Amla + aloe vera juice</b> nourishes skin from within</li>"
            "<li>Rinse face after commuting; keep a soft cloth to wipe pollution dust</li>"
            "</ul>"
        ),
    },
    # -- 24. Pollution — eyes protection --
    {
        "keywords": [
            "pollution eyes", "burning eyes", "red eyes pollution", "itchy eyes pollution",
            "eye irritation smog",
        ],
        "answer": (
            "If <b>eyes feel irritated</b> from pollution:"
            "<ul>"
            "<li>Wash with cool clean water; avoid rubbing</li>"
            "<li>Use <b>rose water</b> or sterile soothing drops for comfort</li>"
            "<li><b>Triphala eyewash</b> (mild) is traditional for cleansing; ensure hygiene</li>"
            "<li>Wear <b>wraparound glasses</b> outdoors to block dust/smog</li>"
            "<li>Eat <b>Vitamin A/C rich foods</b> (carrot, amla, spinach) for eye health</li>"
            "</ul>"
        ),
    },
    # -- 25. Headache / Migraine --
    {
        "keywords": [
            "headache", "migraine", "head pain", "pain in head", "brain pain", "brain ache",
            "pitta headache", "vata headache", "stress headache",
        ],
        "answer": (
            "For <b>headache / migraine</b>:"
            "<ul>"
            "<li><b>Shirodhara</b> (medicated oil on forehead) is classic for chronic migraines</li>"
            "<li>Apply cool <b>ghee + camphor</b> or <b>sandalwood paste</b> on temples (Pitta soothing)</li>"
            "<li><b>Nasya</b>: 2-3 drops warm <b>anuthailam</b> or sesame oil per nostril (Vata calming)</li>"
            "<li>Avoid triggers: bright screens, skipping meals, excess coffee, heat</li>"
            "<li>Hydrate; practise <b>sheetali breath</b> and <b>forward bends</b> for cooling</li>"
            "</ul>"
        ),
    },
    # -- 26. Back pain --
    {
        "keywords": [
            "back pain", "low back pain", "lumbar pain", "slip disc ayurveda", "back ache",
        ],
        "answer": (
            "For <b>back pain</b> (often Vata-aggravation):"
            "<ul>"
            "<li><b>Kati basti</b> (warm medicated oil pooling on lower back) for stiffness</li>"
            "<li><b>Mahanarayan taila</b> warm massage, then gentle heat pad</li>"
            "<li>Stretch: <b>cat-cow, bhujangasana, setu bandhasana</b> (avoid pain-inducing moves)</li>"
            "<li><b>Triphala</b> + fiber if constipation worsens pain</li>"
            "<li>Keep core warm; avoid cold drafts and long sitting</li>"
            "</ul>"
        ),
    },
    # -- 27. Hair fall / Dandruff --
    {
        "keywords": [
            "hair fall", "hair loss", "dandruff", "dry scalp", "hair thinning",
        ],
        "answer": (
            "For <b>hair fall &amp; dandruff</b>:"
            "<ul>"
            "<li>Weekly <b>warm oiling</b>: bhringraj or coconut + curry leaves</li>"
            "<li><b>Triphala</b> or <b>amla</b> internally for scalp nourishment</li>"
            "<li>Apply <b>neem + yogurt</b> or <b>fenugreek</b> paste for dandruff</li>"
            "<li>Gentle shampoo; avoid very hot water and harsh chemicals</li>"
            "<li>Protein + iron rich diet; manage stress with pranayama</li>"
            "</ul>"
        ),
    },
    # -- 28. Weight management --
    {
        "keywords": [
            "weight loss", "weight gain", "lose weight ayurveda", "kapha weight", "metabolism boost",
        ],
        "answer": (
            "<b>Ayurvedic weight balance</b>:"
            "<ul>"
            "<li><b>Kapha-pacifying diet</b>: warm, light, spicy; avoid sugar and cold dairy</li>"
            "<li><b>Trikatu</b> (black pepper + pippali + ginger) to kindle Agni</li>"
            "<li><b>Early dinner</b>, finish 3 hrs before sleep; biggest meal at noon</li>"
            "<li>Daily <b>brisk walk + surya namaskar</b> 12 cycles; add dry brushing (garshana)</li>"
            "<li>Stay hydrated with <b>jeera-coriander-fennel</b> water</li>"
            "</ul>"
        ),
    },
    # -- 29. Diabetes / High blood sugar --
    {
        "keywords": [
            "diabetes", "high blood sugar", "type 2 diabetes", "madhumeha", "sugar control",
        ],
        "answer": (
            "For <b>blood sugar balance</b> (Madhumeha):"
            "<ul>"
            "<li><b>Vijaysar tumbler water</b> (overnight) or <b>Gudmar</b> (Gymnema) under guidance</li>"
            "<li><b>Fenugreek seeds</b> soaked overnight; consume in morning</li>"
            "<li>Plate rule: 1/2 veggies, 1/4 protein, 1/4 whole grains; avoid refined carbs</li>"
            "<li>Walk 10-15 minutes after meals to improve glucose uptake</li>"
            "<li>Monitor regularly; work with your physician for meds/insulin adjustments</li>"
            "</ul>"
        ),
    },
    # -- 30. Hypertension / Heart --
    {
        "keywords": [
            "high blood pressure", "hypertension", "heart health", "bp control", "cholesterol",
        ],
        "answer": (
            "<b>Heart &amp; blood pressure care</b>:"
            "<ul>"
            "<li><b>Arjuna bark</b> decoction is classical cardiotonic; use under medical advice</li>"
            "<li><b>Garlic</b> and <b>flaxseed</b> support lipids; reduce fried/salty foods</li>"
            "<li>Daily <b>mindful breathing</b>: 5-10 minutes slow belly breathing lowers BP</li>"
            "<li><b>Pranayama:</b> Anulom-Vilom; avoid intense Kapalbhati if BP high</li>"
            "<li>Consistent sleep and weight control are key for long-term BP stability</li>"
            "</ul>"
        ),
    },
    # -- 31. Arthritis / Joint pain --
    {
        "keywords": [
            "arthritis", "joint pain", "knee pain", "osteoarthritis", "rheumatoid", "sandhivata",
        ],
        "answer": (
            "For <b>joint pain</b> (Sandhivata):"
            "<ul>"
            "<li><b>Nirgundi</b> or <b>shallaki</b> (Boswellia) for inflammation; consult practitioner</li>"
            "<li><b>Mahanarayan</b> or <b>dashmool</b> oil massage + mild heat</li>"
            "<li><b>Castor oil</b> at night (small dose) can ease Vata in joints</li>"
            "<li>Gentle <b>range-of-motion yoga</b>; avoid impact loading</li>"
            "<li>Keep joints warm; include omega-3s and turmeric in diet</li>"
            "</ul>"
        ),
    },
    # -- 32. Allergies / Sinus --
    {
        "keywords": [
            "allergy", "allergies", "sinus", "allergic rhinitis", "sneezing", "hay fever",
        ],
        "answer": (
            "For <b>allergic rhinitis / sinus</b>:"
            "<ul>"
            "<li>Daily <b>nasya</b>: 2 drops warm sesame or ghee in each nostril</li>"
            "<li><b>Trikatu</b> and <b>sitopaladi</b> are traditional for Kapha congestion</li>"
            "<li><b>Neti pot</b> with saline (lukewarm) to clear passages; dry well after</li>"
            "<li>Avoid cold foods, curd at night, and dust triggers; keep bedding clean</li>"
            "<li><b>Ginger-tulsi-pepper tea</b> for daily defence</li>"
            "</ul>"
        ),
    },
    # -- 33. Menstrual cramps / PCOS support --
    {
        "keywords": [
            "period pain", "menstrual cramps", "pcos", "pcod", "irregular periods", "dysmenorrhea",
        ],
        "answer": (
            "For <b>period pain &amp; PCOS support</b>:"
            "<ul>"
            "<li><b>Ajwain + dry ginger tea</b> eases cramps; apply warm compress on lower abdomen</li>"
            "<li><b>Dashmool</b> or <b>hingvastak</b> churna for Vata-related pain (per practitioner)</li>"
            "<li>Stabilize blood sugar: balanced meals, avoid frequent sugary snacks</li>"
            "<li>Daily <b>walk + yoga</b> (malasana, supta baddha konasana, gentle twists)</li>"
            "<li>Sleep hygiene &amp; stress reduction to balance hormones</li>"
            "</ul>"
        ),
    },
    # -- 34. Eye strain (screens) --
    {
        "keywords": [
            "eye strain", "computer vision syndrome", "tired eyes", "burning eyes screen",
        ],
        "answer": (
            "For <b>screen-related eye strain</b>:"
            "<ul>"
            "<li>Follow <b>20-20-20</b> rule; blink consciously to avoid dryness</li>"
            "<li>Cool <b>rose water pads</b> or cucumber slices for soothing</li>"
            "<li><b>Triphaladi ghrita</b> is traditional for eye nourishment (under guidance)</li>"
            "<li>Adjust screen brightness, use anti-glare, keep screen at eye level</li>"
            "<li>Include <b>carrot, amla, ghee</b> for eye-supportive nutrients</li>"
            "</ul>"
        ),
    },
    # -- 35. Ear care / Mild ear pain --
    {
        "keywords": [
            "ear pain", "ear ache", "ear care", "ear wax", "ear infection mild",
        ],
        "answer": (
            "For mild <b>ear discomfort</b> (not severe infection):"
            "<ul>"
            "<li>2-3 drops warm <b>sesame oil</b> (lukewarm) can soften wax; avoid if infection suspected</li>"
            "<li>Keep ears dry; avoid earbuds that push wax deeper</li>"
            "<li><b>Ginger-tulsi steam</b> may ease Eustachian congestion</li>"
            "<li>If pain, fever, or discharge persists, seek medical evaluation promptly</li>"
            "</ul>"
        ),
    },
    # -- 35b. Shoulder pain / frozen shoulder --
    {
        "keywords": [
            "shoulder pain", "shoulder ache", "pain in shoulder", "shoulder stiffness",
            "frozen shoulder", "shoulder joint pain", "rotator cuff pain", "shoulder muscle pain",
        ],
        "answer": (
            "For <b>shoulder pain / stiffness</b> (often Vata aggravation or strain):"
            "<ul>"
            "<li><b>Warm oil massage</b> (Mahanarayan taila or sesame oil) followed by mild heat can reduce stiffness</li>"
            "<li>Do gentle mobility exercises: <b>pendulum swings, wall walks, shoulder rolls</b> (avoid painful jerks)</li>"
            "<li><b>Turmeric + ginger</b> in diet may support inflammation management</li>"
            "<li>Avoid sleeping on the painful side and avoid heavy overhead lifting until pain improves</li>"
            "<li>If there is severe pain, weakness, swelling, numbness, injury/trauma, or reduced movement for weeks, get medical evaluation</li>"
            "</ul>"
        ),
    },
    # -- 36. Weight-loss day schedule / diet plan --
    {
        "keywords": [
            "weight loss schedule", "diet schedule", "diet plan weight loss", "meal plan weight loss",
            "weight loss routine", "day plan for weight loss", "diet chart weight loss", "lose weight diet chart",
        ],
        "answer": (
            "<b>Sample Ayurvedic-inspired day plan for weight loss</b> (Kapha-balancing):"
            "<ul>"
            "<li><b>Upon waking</b>: warm water with lemon + pinch of ginger</li>"
            "<li><b>Breakfast</b> (light): veggie upma/poha or mung dal chilla; avoid sugar-laden cereals</li>"
            "<li><b>Mid-morning</b>: herbal tea (cumin-coriander-fennel) or buttermilk with roasted cumin</li>"
            "<li><b>Lunch</b> (largest): 1/2 plate veggies, 1/4 dal/lean protein, 1/4 millets/brown rice; salad with lemon</li>"
            "<li><b>Evening</b>: nuts (5-6 soaked almonds) or roasted chana; brisk 20-min walk</li>"
            "<li><b>Dinner</b> (light, 3 hrs before bed): clear veggie soup + small khichdi; no fried/heavy foods</li>"
            "<li><b>Spice support</b>: trikatu or ginger before meals to kindle Agni (per practitioner)</li>"
            "<li><b>Sleep</b>: in bed by 10-10:30 PM; consistent routine aids metabolism</li>"
            "</ul>"
        ),
    },
    # -- 37. Kidney stones / renal health --
    {
        "keywords": [
            "kidney stone", "renal stone", "kidney pain", "kidney health", "stone prevention",
        ],
        "answer": (
            "For <b>kidney stone care</b> (supportive):"
            "<ul>"
            "<li><b>Hydration</b>: 2.5â€“3 L water/day unless medically restricted</li>"
            "<li><b>Fresh lemon water</b> (citrate helps prevent stone formation)</li>"
            "<li>Reduce high-oxalate foods (spinach, beet, nuts) if you form oxalate stones</li>"
            "<li><b>Varuna</b> and <b>gokshura</b> are traditional; use only under practitioner guidance</li>"
            "<li>Severe flank pain, fever, or vomiting = seek urgent medical care</li>"
            "</ul>"
        ),
    },
    # -- 38. Liver health / fatty liver --
    {
        "keywords": [
            "liver health", "fatty liver", "liver detox", "elevated sgpt", "liver care",
        ],
        "answer": (
            "<b>Liver support</b> (fatty liver/raised enzymes):"
            "<ul>"
            "<li><b>Zero alcohol</b>; cut sugary drinks and refined carbs</li>"
            "<li><b>Bhumi amla</b> (Phyllanthus niruri) and <b>turmeric</b> support the liver (use per expert)</li>"
            "<li><b>Weight loss</b> 5-10% body weight improves fatty liver</li>"
            "<li>Eat bitter greens (karela, methi), adequate protein, good fats (olive, nuts)</li>"
            "<li>Regular liver function tests with your physician</li>"
            "</ul>"
        ),
    },
    # -- 39. Thyroid (hypothyroid support) --
    {
        "keywords": [
            "thyroid", "hypothyroid", "low thyroid", "thyroxine", "tsh high",
        ],
        "answer": (
            "<b>Thyroid support</b> (with doctor-managed medication):"
            "<ul>"
            "<li>Take prescribed <b>thyroxine</b> on empty stomach; don’t self-adjust dose</li>"
            "<li><b>Selenium &amp; zinc</b> rich foods: pumpkin seeds, nuts, lentils</li>"
            "<li>Avoid excess raw goitrogens (raw cabbage/soy) near medication time</li>"
            "<li>Light exercise + regular sleep improve metabolism</li>"
            "<li><b>Kanchanar guggulu</b> is classical; only under Ayurvedic physician supervision</li>"
            "</ul>"
        ),
    },
    # -- 40. Anemia / low hemoglobin --
    {
        "keywords": [
            "anemia", "low hemoglobin", "hb low", "iron deficiency", "low iron",
        ],
        "answer": (
            "For <b>low hemoglobin</b> (screen cause with labs):"
            "<ul>"
            "<li><b>Iron-rich</b> foods: beet, spinach, sesame, dates, jaggery, pomegranate</li>"
            "<li>Pair with <b>Vitamin C</b> (amla, lemon) to boost absorption</li>"
            "<li><b>Lohasava</b> / <b>punarnava mandur</b> used traditionally; only under supervision</li>"
            "<li>Avoid tea/coffee close to iron intake; they inhibit absorption</li>"
            "<li>Check B12/folate; treat per doctor if deficient</li>"
            "</ul>"
        ),
    },
    # -- 41. Dehydration / electrolytes --
    {
        "keywords": [
            "dehydration", "electrolytes", "heat exhaustion", "heat stroke prevention",
        ],
        "answer": (
            "<b>Hydration &amp; electrolytes</b>:"
            "<ul>"
            "<li>Signs: dry mouth, dark urine, dizziness, rapid pulse</li>"
            "<li>Sip <b>ORS</b> or homemade mix (1L water + 6 tsp sugar + 1/2 tsp salt + lemon)</li>"
            "<li><b>Buttermilk</b> with roasted cumin is light and rehydrating</li>"
            "<li>Avoid excessive caffeinated/energy drinks in heat</li>"
            "<li>If confusion, very low urine, or fainting â†’ seek urgent care</li>"
            "</ul>"
        ),
    },
    # -- 42. Fever (general) --
    {
        "keywords": [
            "fever", "high temperature", "viral fever", "pyrexia", "fever remedy",
        ],
        "answer": (
            "For <b>fever</b> (general supportive care):"
            "<ul>"
            "<li>Rest + light warm fluids: rice kanji, tulsi-ginger tea, clear soups</li>"
            "<li><b>Sponge with lukewarm water</b> if very hot; avoid cold showers</li>"
            "<li>Avoid heavy/oily foods; keep meals small and warm</li>"
            "<li>Monitor temperature; if >102Â°F (38.9Â°C), rash, breathlessness, or lasts >3 days â†’ see a doctor</li>"
            "<li>Do not mix/unprescribed antipyretics; follow physician guidance</li>"
            "</ul>"
        ),
    },
    # -- 43. Urinary tract discomfort (UTI support) --
    {
        "keywords": [
            "uti", "urinary infection", "burning urination", "urine burning", "urinary tract",
        ],
        "answer": (
            "For <b>UTI support</b> (medical evaluation needed):"
            "<ul>"
            "<li><b>Hydrate</b>: frequent water; don’t hold urine</li>"
            "<li><b>Coriander seed water</b> (soaked overnight) is cooling traditionally</li>"
            "<li><b>Cranberry</b> may reduce recurrence (evidence mixed)</li>"
            "<li>If fever, flank pain, blood in urine, or pregnancy â†’ seek prompt doctor care for antibiotics</li>"
            "</ul>"
        ),
    },
    # -- 44. Muscle recovery / workout nutrition --
    {
        "keywords": [
            "post workout", "muscle recovery", "muscle gain diet", "protein intake", "gym diet",
        ],
        "answer": (
            "<b>Muscle recovery &amp; lean gain</b>:"
            "<ul>"
            "<li><b>Protein</b>: 1.2â€“1.6 g/kg/day from dal, paneer, tofu, eggs/lean meat per tolerance</li>"
            "<li><b>Carb + protein</b> within 1 hr post-workout: banana + whey/soaked almonds + milk/curd</li>"
            "<li><b>Hydrate</b>; add electrolytes after heavy sweat sessions</li>"
            "<li><b>Ashwagandha</b> is an adaptogen for strength; use per practitioner</li>"
            "<li>Sleep 7-8 hrs; progressive overload with rest days prevents injury</li>"
            "</ul>"
        ),
    },
    # -- 45. Schedule appointment CTA --
    {
        "keywords": [
            "schedule appointment", "book appointment", "book a doctor", "schedule me appointment",
            "doctor appointment", "book consultation", "need appointment", "book a visit",
        ],
        "answer": (
            "<b>Sure, I can book it for you.</b><br>"
            "<ul>"
            "<li>Tell me: <b>specialty</b>, <b>date</b>, and a <b>time window</b> (e.g., 10–12 AM).</li>"
            "<li>If you already picked a slot, send its <b>slot ID</b> and I'll auto-book.</li>"
            "<li>You can also browse: <a href=\"/doctors/search/\" style=\"color:#8cd4f5;text-decoration:underline;\">Find a doctor</a></li>"
            "</ul>"
            "Once I have a slot ID, I’ll reserve it instantly."
        ),
    },
]


# Safety footer appended to every reply
SAFETY_NOTE = (
    "<br><small style='color:rgba(255,255,255,0.65);display:block;margin-top:0.35rem;'>"
    "Note: This is general wellness information, not a medical diagnosis or prescription. "
    "Consult a qualified doctor for personalised care, especially for persistent or severe symptoms.</small>"
)

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
