

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from altair import Axis, Scale, Tooltip, X, Y, Color
from typing import List, Dict, Tuple, Optional
import os

# Page configuration
st.set_page_config(
    page_title="StrainMatch Pro | Cannabis Recommendation Engine",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# FIXED UI STYLING - Better contrast and spacing
# ============================================================================
st.markdown("""
<style>
/* Import fonts */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* Root variables */
:root {
    --bg-primary: #0a0f1c;
    --bg-secondary: #111827;
    --bg-card: #1a2234;
    --bg-hover: #243044;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --accent-green: #10b981;
    --accent-green-glow: rgba(16, 185, 129, 0.3);
    --accent-purple: #8b5cf6;
    --accent-orange: #f59e0b;
    --accent-blue: #3b82f6;
    --accent-pink: #ec4899;
    --accent-red: #ef4444;
    --border-subtle: rgba(255, 255, 255, 0.08);
    --gradient-mesh: radial-gradient(ellipse at 20% 20%, rgba(16, 185, 129, 0.15) 0%, transparent 50%),
                     radial-gradient(ellipse at 80% 80%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
}

/* Global styles */
.stApp {
    background: var(--bg-primary);
    background-image: var(--gradient-mesh);
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
}

/* Hide Streamlit branding */
#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}

/* Main container */
.main .block-container {
    padding: 1.5rem 2rem;
    max-width: 1600px;
}

/* Typography */
h1 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2.5rem !important;
    letter-spacing: -0.03em !important;
    background: linear-gradient(135deg, #10b981 0%, #8b5cf6 50%, #3b82f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0 !important;
}

h2 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    font-size: 1.5rem !important;
    margin-top: 1.5rem !important;
}

h3 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    font-size: 1.1rem !important;
}

p, li, span {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: var(--text-secondary) !important;
}

/* Strain cards - glassmorphism style */
.strain-card {
    background: linear-gradient(135deg, rgba(26, 34, 52, 0.9) 0%, rgba(17, 24, 39, 0.95) 100%);
    border: 1px solid var(--border-subtle);
    border-radius: 20px;
    padding: 1.5rem;
    margin: 1rem 0;
    backdrop-filter: blur(10px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.strain-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent-green), var(--accent-purple));
    opacity: 0;
    transition: opacity 0.3s ease;
}

.strain-card:hover {
    border-color: rgba(16, 185, 129, 0.3);
    transform: translateY(-2px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 0 0 60px var(--accent-green-glow);
}

.strain-card:hover::before {
    opacity: 1;
}

/* Match score badge */
.match-score {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 50px;
    font-weight: 700;
    font-size: 1.1rem;
    font-family: 'JetBrains Mono', monospace;
}

.match-excellent { 
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.match-good { 
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(245, 158, 11, 0.1) 100%);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.match-fair { 
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

/* Strain type badges */
.strain-type {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 0.8rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.type-indica {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(139, 92, 246, 0.1) 100%);
    color: #a78bfa;
    border: 1px solid rgba(139, 92, 246, 0.3);
}

.type-sativa {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(245, 158, 11, 0.1) 100%);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.type-hybrid {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

/* ==================================================================
   FIX #1: IMPROVED BUTTON CONTRAST
   White text on green = maximum readability
   ================================================================== */
.stButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: #ffffff !important; /* PURE WHITE for maximum contrast */
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important; /* Subtle shadow for crispness */
    letter-spacing: 0.02em !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4) !important;
    background: linear-gradient(135deg, #34d399 0%, #10b981 100%) !important;
    color: #ffffff !important; /* Keep white on hover too */
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ==================================================================
   FIX #2: PREVENT METRIC OVERLAP
   Proper spacing and min-heights
   ================================================================== */
.stMetric {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 16px !important;
    padding: 1.2rem !important;
    min-height: 110px !important; /* Increased from 90px */
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    margin-bottom: 0.5rem !important;
}

.stMetric label {
    color: var(--text-muted) !important;
    font-size: 0.75rem !important;
    white-space: normal !important; /* Allow wrapping if needed */
    overflow: visible !important;
    text-overflow: clip !important;
    margin-bottom: 0.5rem !important;
    line-height: 1.4 !important;
}

.stMetric [data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.4rem !important;
    white-space: nowrap !important;
    overflow: visible !important;
    margin-top: 0.25rem !important;
    line-height: 1.2 !important;
}

.stMetric [data-testid="stMetricDelta"] {
    display: none; /* Hide deltas to prevent crowding */
}

/* Cannabinoid pills - prevent text wrapping */
.cannabinoid-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem; /* Increased gap */
    margin: 1.5rem 0; /* More vertical space */
}

.cannabinoid-pill {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 0.8rem 1.2rem; /* More padding */
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    min-width: 85px; /* Wider to prevent cramping */
    min-height: 70px; /* Taller for better spacing */
}

.cannabinoid-pill .label {
    font-size: 0.7rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
    white-space: nowrap;
    margin-bottom: 0.25rem; /* Space between label and value */
}

.cannabinoid-pill .value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.2rem; /* Slightly larger */
    font-weight: 600;
    color: var(--text-primary);
    white-space: nowrap;
    margin-top: 0.25rem;
}

/* ==================================================================
   FIX #3: PREVENT TEXT OVERLAP IN EXPANDERS
   Better line-height and spacing
   ================================================================== */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    margin-bottom: 0.5rem !important;
}

.streamlit-expanderContent {
    background: var(--bg-card) !important;
    border-radius: 0 0 12px 12px !important;
    padding: 1.5rem !important;
    margin-top: -12px !important;
    line-height: 1.8 !important; /* Better line spacing */
}

.streamlit-expanderContent p {
    margin: 0.75rem 0 !important; /* More vertical space between paragraphs */
    line-height: 1.7 !important;
    color: var(--text-secondary) !important;
}

.streamlit-expanderContent h3,
.streamlit-expanderContent h4 {
    margin-top: 1.5rem !important; /* More space before headers */
    margin-bottom: 0.75rem !important;
    clear: both !important; /* Prevent floating issues */
}

.streamlit-expanderContent strong {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

/* Effect tags */
.effect-tag {
    display: inline-block;
    padding: 0.4rem 0.9rem; /* More padding */
    margin: 0.3rem 0.2rem; /* More margin */
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border-subtle);
    border-radius: 50px;
    font-size: 0.85rem;
    color: var(--text-secondary);
    transition: all 0.2s ease;
    line-height: 1.5 !important;
}

.effect-tag:hover {
    background: rgba(16, 185, 129, 0.1);
    border-color: rgba(16, 185, 129, 0.3);
    color: var(--accent-green);
}

/* Select boxes */
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
}

/* Search input */
.stTextInput > div > div > input {
    background: var(--bg-card) !important;
    border: 2px solid var(--border-subtle) !important;
    border-radius: 16px !important;
    color: var(--text-primary) !important;
    padding: 0.75rem 1rem !important;
    font-size: 1rem !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent-green) !important;
    box-shadow: 0 0 0 3px var(--accent-green-glow) !important;
}

/* Consumer-friendly explanation cards */
.explain-card {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
    border: 1px solid rgba(59, 130, 246, 0.2);
    border-radius: 16px;
    padding: 1.5rem; /* More padding */
    margin: 1.5rem 0; /* More margin */
    line-height: 1.7 !important;
}

.explain-card h4 {
    color: #60a5fa !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    margin-bottom: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.explain-card p {
    color: var(--text-secondary) !important;
    font-size: 1rem !important;
    line-height: 1.7 !important;
    margin: 0.5rem 0 !important;
}

/* Horizontal rule */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-subtle), transparent);
    margin: 2rem 0; /* More space */
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-primary);
}

::-webkit-scrollbar-thumb {
    background: var(--bg-card);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--bg-hover);
}

/* Altair charts */
.vega-embed {
    background: transparent !important;
}

/* Quick stats bar */
.stats-bar {
    display: flex;
    gap: 1.5rem;
    padding: 1rem 0;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 1.5rem;
}

.stat-item {
    display: flex;
    flex-direction: column;
}

.stat-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
}

.stat-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
</style>
""", unsafe_allow_html=True)

# Detailed terpene encyclopedia  
TERPENE_INFO = {
    "myrcene": {
        "name": "Myrcene",
        "aroma": "Earthy, musky, herbal, mango",
        "found_in": "Mangoes, hops, lemongrass, thyme",
        "effects": ["Sedating", "Muscle Relaxant", "Anti-inflammatory", "Analgesic"],
        "vibe": "The 'couch-lock' terpene - relaxing and sedative",
        "color": "#8b5cf6",
        "science": "Enhances cannabinoid absorption across the blood-brain barrier via increased cell membrane permeability. Acts as an agonist at α2-adrenergic receptors (sedation), blocks inflammation through TNF-α inhibition.",
        "citations": "[1] do Vale et al. (2002) Phytotherapy Research; [2] Russo (2011) British Journal of Pharmacology"
    },
    "limonene": {
        "name": "Limonene",
        "aroma": "Citrus, lemon, orange, fresh",
        "found_in": "Citrus peels, juniper, rosemary",
        "effects": ["Mood Elevation", "Stress Relief", "Anti-anxiety", "Energizing"],
        "vibe": "The 'happy' terpene - uplifting like a sunny day",
        "color": "#f59e0b",
        "science": "Increases serotonin and dopamine neurotransmitter levels via modulation of 5-HT1A and D2 receptors. Rapidly crosses blood-brain barrier, reduces cortisol (stress hormone), enhances immune function via increased lymphocyte activity.",
        "citations": "[1] Lima et al. (2013) Phytomedicine; [2] Komiya et al. (2006) Behavioural Brain Research"
    },
    "caryophyllene": {
        "name": "β-Caryophyllene",
        "aroma": "Spicy, peppery, woody, clove",
        "found_in": "Black pepper, cloves, cinnamon, hops",
        "effects": ["Anti-inflammatory", "Pain Relief", "Neuroprotective", "Stress Relief"],
        "vibe": "The 'healing' terpene - the only one that's also a cannabinoid",
        "color": "#ef4444",
        "science": "Unique among terpenes: selectively binds CB2 cannabinoid receptors (K_i = 155 nM) without binding CB1, avoiding psychoactivity. Reduces inflammatory cytokines (IL-1β, TNF-α) via NF-κB pathway inhibition. Demonstrates neuroprotective effects in Alzheimer's models.",
        "citations": "[1] Gertsch et al. (2008) PNAS; [2] Fidyt et al. (2016) Nutrients; [3] Cheng et al. (2014) ACS Chemical Neuroscience"
    },
    "linalool": {
        "name": "Linalool",
        "aroma": "Floral, lavender, sweet, citrus",
        "found_in": "Lavender, coriander, basil, mint",
        "effects": ["Calming", "Anti-anxiety", "Sedative", "Anticonvulsant"],
        "vibe": "The 'spa day' terpene - like lavender aromatherapy",
        "color": "#a855f7",
        "science": "Modulates glutamate (excitatory) and GABA (inhibitory) neurotransmission via NMDA receptor antagonism and GABAergic enhancement. Acts on 5-HT1A serotonin receptors (anxiolytic effect), blocks voltage-gated sodium channels (anticonvulsant), reduces acetylcholine release.",
        "citations": "[1] Elisabetsky et al. (1995) Journal of Ethnopharmacology; [2] Batista et al. (2008) Phytomedicine; [3] Buchbauer et al. (1993) Flavour and Fragrance Journal"
    },
    "pinene": {
        "name": "α-Pinene",
        "aroma": "Pine, fresh, sharp, forest",
        "found_in": "Pine needles, rosemary, basil, dill",
        "effects": ["Alertness", "Memory Retention", "Anti-inflammatory", "Bronchodilator"],
        "vibe": "The 'clear-headed' terpene - forest-fresh focus",
        "color": "#22c55e",
        "science": "Enhances memory and alertness via inhibition of acetylcholinesterase (AChE), increasing acetylcholine availability in the hippocampus. Counteracts THC-induced short-term memory impairment. Bronchodilator through relaxation of tracheal smooth muscle. Anti-inflammatory via NF-κB suppression.",
        "citations": "[1] Perry et al. (2000) Journal of Agricultural and Food Chemistry; [2] Russo (2011) British Journal of Pharmacology; [3] Yang et al. (2016) Molecules"
    },
    "humulene": {
        "name": "Humulene",
        "aroma": "Earthy, woody, hoppy, spicy",
        "found_in": "Hops, coriander, cloves, basil",
        "effects": ["Anti-inflammatory", "Appetite Suppressant", "Antibacterial"],
        "vibe": "The 'beer' terpene - earthy and grounding",
        "color": "#78716c",
        "science": "Potent anti-inflammatory via reduction of pro-inflammatory mediators (PGE-2, iNOS, COX-2). Unlike most cannabinoids/terpenes, suppresses appetite through unknown mechanisms. Aerosol inhalation demonstrates rapid systemic anti-inflammatory effects.",
        "citations": "[1] Fernandes et al. (2007) European Journal of Pharmacology; [2] Rogerio et al. (2009) European Journal of Pharmacology"
    },
    "terpinolene": {
        "name": "Terpinolene",
        "aroma": "Floral, herbal, piney, sweet",
        "found_in": "Lilacs, nutmeg, cumin, apples",
        "effects": ["Uplifting", "Antioxidant", "Sedative (high doses)", "Fresh feeling"],
        "vibe": "The 'adventure' terpene - rare and energizing",
        "color": "#06b6d4",
        "science": "Rare terpene (found in ~10% of strains) with biphasic effects: energizing at low doses, sedative at high doses. Potent antioxidant and antiproliferative properties. Modulates AChE activity and enhances focus. Often dominant in classic Sativa strains like Jack Herer and Dutch Treat.",
        "citations": "[1] Ito & Ito (2013) Journal of Toxicological Sciences; [2] Mercier et al. (2009) Planta Medica"
    },
    "ocimene": {
        "name": "Ocimene",
        "aroma": "Sweet, herbal, woody, citrus",
        "found_in": "Mint, parsley, orchids, kumquats",
        "effects": ["Antiviral", "Antifungal", "Decongestant", "Uplifting"],
        "vibe": "The 'fresh' terpene - sweet and herbaceous",
        "color": "#84cc16",
        "science": "Exhibits broad-spectrum antimicrobial activity. Acts as a plant defense compound (herbivore deterrent). Decongestant properties via airway smooth muscle relaxation. Common in tropical Sativa varieties, contributes to uplifting effects.",
        "citations": "[1] Kiran et al. (2017) Natural Product Communications; [2] Pichersky & Raguso (2018) Plant Physiology"
    }
}

# Symptom profiles and recommendation criteria
SYMPTOM_PROFILES = {
    "need Sleep": {
        "icon": "😴",
        "customer_pitch": "Looking for deep, restorative sleep? We have strains designed to help you drift off and stay asleep.",
        "best_time": "Evening/Bedtime",
        "onset": "30-60 minutes",
        "duration": "6-8 hours",
        "science_note": "Myrcene enhances GABA neurotransmission (the brain's 'off switch') while linalool blocks glutamate (the brain's 'on switch') via NMDA receptor antagonism, creating sedation. CBN (cannabinol) forms when THC oxidizes and binds weakly to CB1 receptors while strongly modulating GABA-A receptors for sleep onset.",
        "target_terpenes": {
            "myrcene": {"weight": 0.3, "min": 0.005},
            "linalool": {"weight": 0.25, "min": 0.004},
            "caryophyllene": {"weight": 0.15, "min": 0.003}
        },
        "target_cannabinoids": {
            "thc_percent": {"weight": 0.3, "min": 10},
            "cbn_percent": {"weight": 0.2, "min": 0.5},
            "cbd_percent": {"weight": 0.1, "preferred_range": (0.5, 3)}
        },
        "avoid_terpenes": ["pinene", "terpinolene"],
        "strain_type_preference": "Indica"
    },
    "need Pain Relief": {
        "icon": "💪",
        "customer_pitch": "Chronic or acute pain getting you down? These strains combine THC, CBD, and anti-inflammatory terpenes for real relief.",
        "best_time": "Anytime (symptom-dependent)",
        "onset": "15-45 minutes",
        "duration": "4-6 hours",
        "science_note": "β-Caryophyllene selectively activates CB2 receptors (K_i = 155 nM), reducing inflammatory cytokines IL-1β and TNF-α via NF-κB pathway inhibition. THC blocks pain transmission by activating CB1 receptors in the periaqueductal gray and dorsal horn. CBD inhibits FAAH enzyme, increasing endogenous anandamide (the 'bliss molecule'), providing sustained anti-inflammatory effects without psychoactivity.",
        "target_terpenes": {
            "caryophyllene": {"weight": 0.35, "min": 0.004},
            "myrcene": {"weight": 0.25, "min": 0.005},
            "humulene": {"weight": 0.15, "min": 0.003}
        },
        "target_cannabinoids": {
            "thc_percent": {"weight": 0.25, "min": 12},
            "cbd_percent": {"weight": 0.25, "min": 0.8},
            "cbc_percent": {"weight": 0.1, "min": 0.1}
        },
        "avoid_terpenes": [],
        "strain_type_preference": "Indica"
    },
    "need Focus": {
        "icon": "🧠",
        "customer_pitch": "Need laser focus without the jitters? High-pinene, low-myrcene strains keep you clear-headed and motivated.",
        "best_time": "Morning/Daytime",
        "onset": "10-20 minutes",
        "duration": "3-4 hours",
        "science_note": "α-Pinene inhibits acetylcholinesterase enzyme, increasing acetylcholine in the hippocampus for memory formation and alertness. Counteracts THC's short-term memory impairment through this mechanism. THCV acts as a CB1 antagonist at low doses (blocking THC's sedative effects), while increasing dopamine and norepinephrine for energized focus. Limonene elevates dopamine in the prefrontal cortex. Terpinolene modulates AChE for enhanced cognition.",
        "target_terpenes": {
            "pinene": {"weight": 0.35, "min": 0.003},
            "limonene": {"weight": 0.3, "min": 0.002},
            "terpinolene": {"weight": 0.15, "min": 0.002}
        },
        "target_cannabinoids": {
            "thc_percent": {"weight": 0.2, "preferred_range": (5, 15)},
            "thcv_percent": {"weight": 0.2, "min": 0.3},
            "cbd_percent": {"weight": 0.1, "preferred_range": (0, 2)}
        },
        "avoid_terpenes": ["myrcene"],
        "strain_type_preference": "Sativa"
    },
    "need Anxiety Relief": {
        "icon": "🧘",
        "customer_pitch": "Anxious? These strains feature calming terpenes and CBD to ease racing thoughts without total sedation.",
        "best_time": "Anytime (as needed)",
        "onset": "20-40 minutes",
        "duration": "4-5 hours",
        "science_note": "Linalool acts as an agonist at 5-HT1A serotonin receptors (the same target as buspirone, an anti-anxiety medication), reducing stress hormone release. Limonene increases both serotonin and dopamine via modulation of 5-HT1A and D2 receptors while reducing cortisol. CBD blocks anxiety-triggering signals through 5-HT1A agonism, CB1 receptor negative allosteric modulation (reducing THC's anxiety potential), and GPR55 antagonism.",
        "target_terpenes": {
            "linalool": {"weight": 0.3, "min": 0.004},
            "limonene": {"weight": 0.3, "min": 0.003},
            "myrcene": {"weight": 0.15, "min": 0.002}
        },
        "target_cannabinoids": {
            "cbd_percent": {"weight": 0.4, "min": 1.0},
            "thc_percent": {"weight": -0.2, "preferred_range": (0, 12)},
            "cbn_percent": {"weight": 0.1, "min": 0.2}
        },
        "avoid_terpenes": ["pinene"],
        "strain_type_preference": "Hybrid"
    },
    "need Creativity": {
        "icon": "🎨",
        "customer_pitch": "Creative block? These strains enhance divergent thinking and inspiration through unique terpene combinations.",
        "best_time": "Daytime/Afternoon",
        "onset": "15-30 minutes",
        "duration": "3-5 hours",
        "science_note": "Limonene increases dopamine in the nucleus accumbens and prefrontal cortex via D2 receptor modulation, enhancing divergent thinking and pattern recognition. Terpinolene (found in only ~10% of strains) modulates acetylcholinesterase for heightened associative thinking. Moderate THC activates CB1 receptors in the frontal cortex, temporarily reducing latent inhibition (the brain's filter), allowing novel connections and creative insights.",
        "target_terpenes": {
            "limonene": {"weight": 0.3, "min": 0.003},
            "terpinolene": {"weight": 0.25, "min": 0.001},
            "ocimene": {"weight": 0.2, "min": 0.001}
        },
        "target_cannabinoids": {
            "thc_percent": {"weight": 0.25, "preferred_range": (10, 18)},
            "cbd_percent": {"weight": 0.1, "preferred_range": (0, 2)},
            "thcv_percent": {"weight": 0.1, "min": 0.2}
        },
        "avoid_terpenes": [],
        "strain_type_preference": "Sativa"
    },
    "need Appetite": {
        "icon": "🍽️",
        "customer_pitch": "Lost your appetite? THC + CBG combo triggers hunger signals. Perfect for medication side effects or recovery.",
        "best_time": "Mealtime",
        "onset": "20-45 minutes",
        "duration": "4-6 hours",
        "science_note": "THC activates CB1 receptors in the hypothalamus and nucleus accumbens, triggering ghrelin (hunger hormone) release and making food more rewarding via dopamine enhancement. CBG (cannabigerol) increases appetite through CB1 agonism and interaction with α2-adrenergic receptors, boosting hunger hormones. Myrcene enhances the pleasure of eating through sedation and anxiolysis (reducing food-related anxiety in patients with eating disorders).",
        "target_terpenes": {
            "myrcene": {"weight": 0.3, "min": 0.005},
            "caryophyllene": {"weight": 0.2, "min": 0.003},
            "humulene": {"weight": -0.1, "min": 0}
        },
        "target_cannabinoids": {
            "thc_percent": {"weight": 0.35, "min": 12},
            "cbg_percent": {"weight": 0.25, "min": 0.3},
            "cbd_percent": {"weight": 0.1, "preferred_range": (0, 1)}
        },
        "avoid_terpenes": [],
        "strain_type_preference": "Indica"
    }
}

# Cannabinoid information
CANNABINOID_INFO = {
    "thc_percent": {
        "name": "THC",
        "full_name": "Δ9-Tetrahydrocannabinol",
        "description": "The main psychoactive compound - produces the 'high'",
        "effects": ["Euphoria", "Relaxation", "Altered perception", "Appetite stimulation"],
        "mechanism": "Partial agonist at CB1 receptors (K_i = 10 nM) in the brain and CB2 receptors (K_i = 25 nM) in immune tissue. Mimics anandamide, modulating neurotransmitter release (dopamine, GABA, glutamate). Produces psychoactivity through CB1 activation in prefrontal cortex, hippocampus, and basal ganglia.",
        "citations": "[1] Pertwee (2008) British Journal of Pharmacology; [2] Mechoulam & Parker (2013) Annual Review of Psychology",
        "color": "#10b981"
    },
    "cbd_percent": {
        "name": "CBD",
        "full_name": "Cannabidiol",
        "description": "Non-intoxicating - therapeutic without the 'high'",
        "effects": ["Anti-anxiety", "Anti-inflammatory", "Neuroprotective", "Modulates THC"],
        "mechanism": "Negative allosteric modulator of CB1 receptors (reduces THC binding), agonist at 5-HT1A serotonin receptors (anti-anxiety), inhibits FAAH enzyme (increases anandamide), antagonizes GPR55 (anti-inflammatory). Non-intoxicating due to lack of CB1 agonism.",
        "citations": "[1] Laprairie et al. (2015) British Journal of Pharmacology; [2] Blessing et al. (2015) Neurotherapeutics; [3] Campos et al. (2016) Frontiers in Immunology",
        "color": "#3b82f6"
    },
    "cbn_percent": {
        "name": "CBN",
        "full_name": "Cannabinol",
        "description": "The 'sleepy' cannabinoid - forms as THC ages",
        "effects": ["Sedation", "Sleep aid", "Pain relief", "Anti-inflammatory"],
        "mechanism": "Weak CB1 partial agonist (1/10th potency of THC) and stronger CB2 agonist. Forms when THC oxidizes over time. Potentiates GABA-A receptor activity (sedation). Sedative effects amplified when combined with THC and myrcene (entourage effect).",
        "citations": "[1] Appendino et al. (2008) Journal of Natural Products; [2] Bonn-Miller et al. (2021) Sleep",
        "color": "#8b5cf6"
    },
    "cbg_percent": {
        "name": "CBG",
        "full_name": "Cannabigerol",
        "description": "The 'mother' cannabinoid - precursor to THC/CBD in the plant",
        "effects": ["Appetite stimulation", "Antibacterial", "Neuroprotective", "Anti-inflammatory"],
        "mechanism": "The acidic form (CBGA) is the precursor to THCA, CBDA, and CBCA in cannabis biosynthesis. Partial agonist at CB1 and CB2 receptors, agonist at α2-adrenergic receptors (appetite stimulation), activates TRPV1 channels (pain modulation). Potent antibacterial against MRSA. Increases anandamide via FAAH inhibition.",
        "citations": "[1] Deiana et al. (2012) CNS & Neurological Disorders; [2] Appendino et al. (2008) Journal of Natural Products; [3] Farha et al. (2020) ACS Infectious Diseases",
        "color": "#f59e0b"
    },
    "thcv_percent": {
        "name": "THCV",
        "full_name": "Tetrahydrocannabivarin",
        "description": "The 'sports car' cannabinoid - fast onset, short duration, energizing",
        "effects": ["Energy", "Appetite suppression", "Clear-headed", "Short duration"],
        "mechanism": "Dose-dependent effects: CB1 antagonist at low doses (<3mg) blocking some THC effects and suppressing appetite; CB1 agonist at higher doses (>10mg). Increases dopamine and norepinephrine without significant psychoactivity. Faster onset and shorter duration than THC (2-3 hours vs 4-6 hours). May improve insulin sensitivity.",
        "citations": "[1] McPartland et al. (2015) Cannabis and Cannabinoid Research; [2] Jadoon et al. (2016) Diabetes Care; [3] Englund et al. (2016) Journal of Psychopharmacology",
        "color": "#ec4899"
    },
    "cbc_percent": {
        "name": "CBC",
        "full_name": "Cannabichromene",
        "description": "Non-intoxicating with unique therapeutic effects",
        "effects": ["Anti-inflammatory", "Antidepressant", "Pain relief", "Neurogenesis"],
        "mechanism": "Does not significantly bind CB1/CB2 receptors. Instead activates TRPV1 and TRPA1 channels (pain, inflammation). Inhibits endocannabinoid reuptake, increasing anandamide levels (antidepressant effect). Stimulates neural stem progenitor cells (NSPCs) in the hippocampus, promoting neurogenesis. Anti-inflammatory via COX-2 inhibition.",
        "citations": "[1] DeLong et al. (2010) Journal of Neurochemistry; [2] Shinjyo & Di Marzo (2013) British Journal of Pharmacology; [3] Izzo et al. (2012) Trends in Pharmacological Sciences",
        "color": "#14b8a6"
    },
    "cbdv_percent": {
        "name": "CBDV",
        "full_name": "Cannabidivarin",
        "description": "CBD's propyl analog - powerful anticonvulsant and anti-nausea properties",
        "effects": ["Anticonvulsant", "Anti-nausea", "Anti-inflammatory", "Neurological support"],
        "mechanism": "Structural analog of CBD with a propyl (3-carbon) side chain instead of pentyl (5-carbon). Modulates TRPV1, TRPV2, TRPA1, and TRPM8 channels. Reduces neuronal hyperexcitability (anticonvulsant) without psychoactivity. Shows promise in autism spectrum disorder (ASD) and Rett syndrome trials. Potent anti-nausea effects via 5-HT1A activation.",
        "citations": "[1] Hill et al. (2012) British Journal of Pharmacology; [2] Zamberletti et al. (2019) Neurotherapeutics; [3] Pretzsch et al. (2019) Translational Psychiatry",
        "color": "#06b6d4"
    }
}

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_strain_data() -> pd.DataFrame:
    """Load the enhanced strain database"""
    enhanced_path = 'strain_database_enhanced_v2.csv'
    
    if not os.path.exists(enhanced_path):
        st.error("❌ Database not found! Please ensure strain_database_enhanced_v2.csv exists.")
        st.stop()
    
    df = pd.read_csv(enhanced_path)
    
    # Calculate total terpene content
    terp_cols = ['myrcene', 'limonene', 'caryophyllene', 'linalool', 'pinene', 'humulene', 'terpinolene', 'ocimene']
    available_terps = [col for col in terp_cols if col in df.columns]
    df['total_terpenes'] = df[available_terps].sum(axis=1)
    
    # Identify dominant terpene
    df['dominant_terpene'] = df[available_terps].idxmax(axis=1)
    
    return df

def calculate_strain_score(strain: pd.Series, symptom_profile: Dict) -> Tuple[float, Dict]:
    """Calculate how well a strain matches the target profile"""
    score = 0.0
    max_score = 0.0
    details = {"terpenes": {}, "cannabinoids": {}, "bonuses": []}
    
    # Score terpenes
    for terp, criteria in symptom_profile.get('target_terpenes', {}).items():
        weight = criteria['weight']
        min_threshold = criteria['min']
        max_score += weight * 100
        
        strain_value = strain.get(terp, 0)
        if strain_value >= min_threshold:
            terp_score = weight * 100 * min(1.5, (strain_value / min_threshold))
            score += terp_score
            details["terpenes"][terp] = {"status": "excellent", "value": strain_value, "target": min_threshold}
        elif strain_value >= min_threshold * 0.5:
            terp_score = weight * 100 * (strain_value / min_threshold)
            score += terp_score
            details["terpenes"][terp] = {"status": "partial", "value": strain_value, "target": min_threshold}
        else:
            details["terpenes"][terp] = {"status": "low", "value": strain_value, "target": min_threshold}
    
    # Penalize avoid terpenes
    avoid_terps = symptom_profile.get('avoid_terpenes', [])
    for terp in avoid_terps:
        if strain.get(terp, 0) > 0.005:
            score -= 10
            details["bonuses"].append(f"High {terp} (may counteract desired effects)")
    
    # Score cannabinoids
    for cann, criteria in symptom_profile.get('target_cannabinoids', {}).items():
        weight = criteria['weight']
        max_score += abs(weight) * 100
        
        strain_value = strain.get(cann, 0)
        
        if 'min' in criteria:
            min_threshold = criteria['min']
            if strain_value >= min_threshold:
                cann_score = abs(weight) * 100
                score += cann_score
                details["cannabinoids"][cann] = {"status": "excellent", "value": strain_value, "target": min_threshold}
            else:
                cann_score = abs(weight) * 100 * (strain_value / min_threshold)
                score += max(0, cann_score)
                details["cannabinoids"][cann] = {"status": "low", "value": strain_value, "target": min_threshold}
        
        elif 'preferred_range' in criteria:
            pref_min, pref_max = criteria['preferred_range']
            if pref_min <= strain_value <= pref_max:
                cann_score = abs(weight) * 100
                score += cann_score if weight > 0 else 0
                details["cannabinoids"][cann] = {"status": "optimal", "value": strain_value, "range": (pref_min, pref_max)}
            elif strain_value < pref_min:
                distance = pref_min - strain_value
                cann_score = abs(weight) * 100 * max(0, 1 - (distance / pref_min))
                score += cann_score if weight > 0 else 0
                details["cannabinoids"][cann] = {"status": "low", "value": strain_value, "range": (pref_min, pref_max)}
            else:
                distance = strain_value - pref_max
                cann_score = abs(weight) * 100 * max(0, 1 - (distance / pref_max))
                score += cann_score if weight > 0 else 0
                details["cannabinoids"][cann] = {"status": "high", "value": strain_value, "range": (pref_min, pref_max)}
    
    # Strain type bonus
    strain_type_pref = symptom_profile.get('strain_type_preference', '')
    if strain_type_pref and strain['strain_type'] == strain_type_pref:
        score += 15
        max_score += 15
        details["bonuses"].append(f"✓ {strain_type_pref} genetics (preferred)")
    else:
        max_score += 15
    
    # Entourage effect bonuses
    if strain.get('thc_percent', 0) > 10 and strain.get('cbd_percent', 0) > 0.5:
        score += 8
        max_score += 8
        details["bonuses"].append("✓ THC+CBD entourage (anxiety reduction)")
    else:
        max_score += 8
    
    if strain.get('thc_percent', 0) > 12 and strain.get('myrcene', 0) > 0.005:
        score += 7
        max_score += 7
        details["bonuses"].append("✓ THC+Myrcene entourage (sedation boost)")
    else:
        max_score += 7
    
    if strain.get('cbd_percent', 0) > 1.0 and strain.get('caryophyllene', 0) > 0.004:
        score += 10
        max_score += 10
        details["bonuses"].append("✓ CBD+Caryophyllene (anti-inflammatory power)")
    else:
        max_score += 10
    
    if strain.get('limonene', 0) > 0.003 and strain.get('linalool', 0) > 0.004:
        score += 6
        max_score += 6
        details["bonuses"].append("✓ Limonene+Linalool (calm + uplift)")
    else:
        max_score += 6
    
    if strain.get('cbg_percent', 0) > 0.3 and strain.get('cbc_percent', 0) > 0.15:
        score += 5
        max_score += 5
        details["bonuses"].append("✓ CBG+CBC (brain health synergy)")
    else:
        max_score += 5
    
    if strain.get('thc_percent', 0) > 15 and strain.get('pinene', 0) > 0.003:
        score += 4
        max_score += 4
        details["bonuses"].append("✓ THC+Pinene (counteracts memory loss)")
    else:
        max_score += 4
    
    # High terpene content bonus
    total_terps = strain.get('total_terpenes', 0)
    if total_terps > 0.02:
        score += 8
        max_score += 8
        details["bonuses"].append(f"✓ Rich terpene profile ({total_terps*100:.2f}% total)")
    elif total_terps > 0.01:
        score += 4
        max_score += 8
        details["bonuses"].append(f"✓ Good terpene content ({total_terps*100:.2f}%)")
    else:
        max_score += 8
    
    # Normalize to 0-100
    normalized_score = min(100, (score / max_score) * 100) if max_score > 0 else 0
    
    return normalized_score, details

def get_recommendations(symptom: str, df: pd.DataFrame, top_n: int = 6) -> pd.DataFrame:
    """Get top strain recommendations"""
    if symptom not in SYMPTOM_PROFILES:
        return pd.DataFrame()
    
    symptom_profile = SYMPTOM_PROFILES[symptom]
    
    scores = []
    details_list = []
    for idx, strain in df.iterrows():
        score, details = calculate_strain_score(strain, symptom_profile)
        scores.append(score)
        details_list.append(details)
    
    df_copy = df.copy()
    df_copy['match_score'] = scores
    df_copy['match_details'] = details_list
    
    return df_copy.nlargest(top_n, 'match_score')

def search_strains(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Search strains by name"""
    if not query:
        return df
    query_lower = query.lower()
    return df[df['strain_name'].str.lower().str.contains(query_lower, na=False)]

# ============================================================================
# VISUALIZATION
# ============================================================================

def create_terpene_radar(strain: pd.Series) -> Optional[alt.Chart]:
    """Create terpene profile visualization"""
    terp_cols = ['myrcene', 'limonene', 'caryophyllene', 'linalool', 'pinene', 'humulene', 'terpinolene']
    
    data = []
    for terp in terp_cols:
        if terp in strain and strain[terp] > 0:
            data.append({
                'Terpene': TERPENE_INFO[terp]['name'],
                'Percentage': float(strain[terp]) * 100,
                'Color': TERPENE_INFO[terp]['color'],
                'Vibe': TERPENE_INFO[terp]['vibe']
            })
    
    if not data:
        return None

    df_chart = pd.DataFrame(data)
    # Sort by percentage descending (highest at top) for horizontal bar chart
    df_chart = df_chart.sort_values('Percentage', ascending=False)

    chart = alt.Chart(df_chart).mark_bar(  # type: ignore
        cornerRadiusEnd=6,  # type: ignore
        height=20  # type: ignore
    ).encode(
        x=alt.X('Percentage:Q',  # type: ignore
                title='Concentration (%)',  # type: ignore
                scale=alt.Scale(domain=[0, max(df_chart['Percentage'].max() * 1.2, 1)])),  # type: ignore
        y=alt.Y('Terpene:N',  # type: ignore
                title=None,  # type: ignore
                sort=list(df_chart['Terpene']),  # type: ignore - Explicitly set order to match sorted DataFrame
                axis=alt.Axis(labelFontSize=12, labelFontWeight=500)),  # type: ignore
        color=alt.Color('Color:N', scale=None, legend=None),  # type: ignore
        tooltip=[
            alt.Tooltip('Terpene:N', title='Terpene'),  # type: ignore
            alt.Tooltip('Percentage:Q', title='%', format='.3f'),  # type: ignore
            alt.Tooltip('Vibe:N', title='Effect')  # type: ignore
        ]
    ).properties(
        height=180
    ).configure_axis(
        labelColor='#94a3b8',
        titleColor='#94a3b8',
        gridColor='#1f2937'
    ).configure_view(
        strokeWidth=0
    )
    
    return chart

def render_strain_card(strain: pd.Series, rank: int):
    """Render strain recommendation card"""
    score = strain['match_score']
    
    # Score class
    if score >= 80:
        score_class = "match-excellent"
        score_icon = "🎯"
    elif score >= 60:
        score_class = "match-good"
        score_icon = "✨"
    else:
        score_class = "match-fair"
        score_icon = "💫"
    
    # Type class
    strain_type = strain['strain_type']
    if strain_type == "Indica":
        type_class = "type-indica"
        type_icon = "🌙"
    elif strain_type == "Sativa":
        type_class = "type-sativa"
        type_icon = "☀️"
    else:
        type_class = "type-hybrid"
        type_icon = "⚖️"
    
    # Card HTML
    st.markdown(f"""
    <div class="strain-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
            <div>
                <h3 style="margin: 0; font-size: 1.4rem; color: #f8fafc;">#{rank} {strain['strain_name']}</h3>
                <span class="strain-type {type_class}">{type_icon} {strain_type}</span>
            </div>
            <span class="match-score {score_class}">{score_icon} {score:.0f}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Cannabinoid grid - THC removed as it varies too much batch-to-batch
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        cbd = strain.get('cbd_percent', 0)
        st.metric("CBD", f"{cbd:.1f}%", help="Non-intoxicating, modulates THC effects, reduces anxiety and inflammation. Works on serotonin receptors and inhibits FAAH enzyme.")
    with col2:
        cbn = strain.get('cbn_percent', 0)
        st.metric("CBN", f"{cbn:.2f}%", help="Sedative cannabinoid formed when THC degrades. Binds weakly to CB1 receptors, potent for sleep via GABA modulation.")
    with col3:
        cbg = strain.get('cbg_percent', 0)
        st.metric("CBG", f"{cbg:.2f}%", help="Cannabigerol: The 'mother cannabinoid' - precursor to THC/CBD. Binds to CB1/CB2, TRPV1, and α2-adrenergic receptors. Neuroprotective, antibacterial, increases anandamide.")
    with col4:
        thcv = strain.get('thcv_percent', 0)
        st.metric("THCV", f"{thcv:.2f}%", help="Tetrahydrocannabivarin: CB1 antagonist at low doses (energizing, appetite suppressing), agonist at high doses. Faster onset, shorter duration than THC.")
    with col5:
        cbc = strain.get('cbc_percent', 0)
        st.metric("CBC", f"{cbc:.2f}%", help="Cannabichromene: Non-intoxicating, binds to TRPV1 and TRPA1 receptors. Anti-inflammatory via COX-2 inhibition, increases neurogenesis and anandamide.")
    
    # Terpene visualization
    with st.expander("🧬 Terpene Profile & Effects", expanded=True):
        col_chart, col_info = st.columns([2, 1])
        
        with col_chart:
            chart = create_terpene_radar(strain)
            if chart:
                st.altair_chart(chart, use_container_width=True)
        
        with col_info:
            dominant = strain.get('dominant_terpene', 'myrcene')
            if dominant in TERPENE_INFO:
                terp_info = TERPENE_INFO[dominant]
                st.markdown(f"""
                <div class="explain-card">
                    <h4>🌟 Dominant: {terp_info['name']}</h4>
                    <p><strong>Aroma:</strong> {terp_info['aroma']}</p>
                    <p><strong>Vibe:</strong> {terp_info['vibe']}</p>
                    <p><strong>Also in:</strong> {terp_info['found_in']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Effects and uses
    col_effects, col_uses = st.columns(2)
    
    with col_effects:
        st.markdown("**🎭 Primary Effects**")
        effects = strain.get('primary_effects', '').split(',')
        effects_html = ' '.join([f'<span class="effect-tag">{e.strip()}</span>' for e in effects if e.strip()])
        st.markdown(effects_html, unsafe_allow_html=True)
    
    with col_uses:
        st.markdown("**💊 Medical Uses**")
        uses = strain.get('medical_uses', '').split(',')
        uses_html = ' '.join([f'<span class="effect-tag">{u.strip()}</span>' for u in uses if u.strip()])
        st.markdown(uses_html, unsafe_allow_html=True)
    
    # Data source
    source = strain.get('data_source', 'Lab-verified data')
    st.caption(f"📊 Source: {source}")
    
    st.markdown("---")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Load data
    df = load_strain_data()
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1>🧬 StrainMatch Pro</h1>
        <p style="font-size: 1.1rem; color: #94a3b8; margin-top: 0.5rem;">
            Science-Based Cannabis Recommendations • Powered by Lab Data & Entourage Effect Research
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Strains", len(df), help="Lab-tested strains in database")
    with col2:
        indica_count = len(df[df['strain_type'] == 'Indica'])
        st.metric("Indica", indica_count)
    with col3:
        sativa_count = len(df[df['strain_type'] == 'Sativa'])
        st.metric("Sativa", sativa_count)
    with col4:
        hybrid_count = len(df[df['strain_type'] == 'Hybrid'])
        st.metric("Hybrid", hybrid_count)
    
    st.markdown("---")
    
    # Main tabs
    tab_recommend, tab_browse, tab_learn = st.tabs([
        "🎯 Find By Need",
        "🔍 Browse All Strains",
        "📚 Learn The Science"
    ])
    
    # TAB 1: RECOMMENDATION ENGINE
    with tab_recommend:
        st.markdown("## What are you looking to address?")
        st.markdown("*Select a category to see strains scientifically matched to your needs*")
        
        # Symptom buttons
        cols = st.columns(3)
        symptom_keys = list(SYMPTOM_PROFILES.keys())
        
        selected_symptom = None
        for i, symptom in enumerate(symptom_keys):
            profile = SYMPTOM_PROFILES[symptom]
            with cols[i % 3]:
                if st.button(
                    f"{profile['icon']} {symptom.split(' ', 1)[1] if ' ' in symptom else symptom}",
                    key=f"btn_{symptom}",
                    use_container_width=True
                ):
                    st.session_state['selected_symptom'] = symptom
        
        # Get selected
        selected_symptom = st.session_state.get('selected_symptom', None)
        
        if selected_symptom:
            profile = SYMPTOM_PROFILES[selected_symptom]
            
            st.markdown("---")
            
            # Customer pitch
            st.markdown(f"""
            <div class="explain-card" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%); border-color: rgba(16, 185, 129, 0.3);">
                <h4 style="color: #34d399 !important;">💬 Tell Your Customer</h4>
                <p style="font-size: 1.1rem; color: #f8fafc !important; font-style: italic;">"{profile['customer_pitch']}"</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick info removed - best time, onset, duration vary too much by individual
            
            # Science note
            with st.expander("🔬 The Science (for curious customers)", expanded=False):
                st.markdown(f"""
                <div class="explain-card">
                    <h4>Why This Works</h4>
                    <p>{profile['science_note']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("## 🏆 Top Matches")
            
            # Get recommendations
            recommendations = get_recommendations(selected_symptom, df, top_n=6)
            
            if not recommendations.empty:
                for rank, (idx, strain) in enumerate(recommendations.iterrows(), 1):
                    render_strain_card(strain, rank)
            else:
                st.warning("No strains found matching this profile.")
    
    # TAB 2: BROWSE
    with tab_browse:
        st.markdown("## Browse Strain Library")
        
        # Search and filters
        col_search, col_type, col_sort = st.columns([2, 1, 1])
        
        with col_search:
            search_query = st.text_input("🔍 Search by name", placeholder="e.g., Blue Dream, OG Kush...")
        
        with col_type:
            type_filter = st.selectbox("Strain Type", ["All", "Indica", "Sativa", "Hybrid"])
        
        with col_sort:
            sort_by = st.selectbox("Sort By", ["Name (A-Z)", "THC (High→Low)", "CBD (High→Low)"])
        
        # Apply filters
        filtered_df = df.copy()
        
        if search_query:
            filtered_df = search_strains(filtered_df, search_query)
        
        if type_filter != "All":
            filtered_df = filtered_df[filtered_df['strain_type'] == type_filter]
        
        # Apply sorting
        if sort_by == "Name (A-Z)":
            filtered_df = filtered_df.sort_values('strain_name')
        elif sort_by == "THC (High→Low)":
            filtered_df = filtered_df.sort_values('thc_percent', ascending=False)
        elif sort_by == "CBD (High→Low)":
            filtered_df = filtered_df.sort_values('cbd_percent', ascending=False)
        
        st.markdown(f"*Showing {len(filtered_df)} strains*")
        
        # Display strains
        for idx, strain in filtered_df.head(20).iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    strain_type = strain['strain_type']
                    type_icon = "🌙" if strain_type == "Indica" else "☀️" if strain_type == "Sativa" else "⚖️"
                    st.markdown(f"**{strain['strain_name']}** {type_icon}")
                
                with col2:
                    st.markdown(f"THC: {strain['thc_percent']:.1f}%")
                
                with col3:
                    st.markdown(f"CBD: {strain['cbd_percent']:.1f}%")
                
                with col4:
                    dom_terp = strain.get('dominant_terpene', 'N/A')
                    if dom_terp in TERPENE_INFO:
                        st.markdown(f"🌿 {TERPENE_INFO[dom_terp]['name']}")
                
                with st.expander("View Details"):
                    strain['match_score'] = 0
                    render_strain_card(strain, 0)
    
    # TAB 3: EDUCATION
    with tab_learn:
        st.markdown("## 📚 Understanding Cannabis Science")
        st.markdown("*Knowledge that helps you help your customers*")
        
        learn_tab1, learn_tab2, learn_tab3 = st.tabs(["🌿 Terpenes", "💊 Cannabinoids", "🔄 Entourage Effect"])
        
        with learn_tab1:
            st.markdown("### The Terpene Guide")
            st.markdown("*Terpenes are aromatic compounds that shape each strain's unique effects*")
            
            for terp_key, terp_info in TERPENE_INFO.items():
                with st.expander(f"{terp_info['name']} — {terp_info['vibe']}", expanded=False):
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown(f"""
                        <div style="background: {terp_info['color']}20; border-left: 4px solid {terp_info['color']}; padding: 1rem; border-radius: 8px;">
                            <strong style="color: {terp_info['color']};">Aroma</strong><br>
                            {terp_info['aroma']}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"**Found In:** {terp_info['found_in']}")
                        st.markdown(f"**Effects:** {', '.join(terp_info['effects'])}")
                        st.markdown(f"**Mechanism:** {terp_info['science']}")
                        if 'citations' in terp_info:
                            st.markdown(f"**References:** {terp_info['citations']}")
        
        with learn_tab2:
            st.markdown("### Cannabinoid Profiles")
            st.markdown("*Beyond THC and CBD - the full spectrum*")
            
            for cann_key, cann_info in CANNABINOID_INFO.items():
                with st.expander(f"{cann_info['name']} ({cann_info['full_name']})", expanded=False):
                    st.markdown(f"**What It Is:** {cann_info['description']}")
                    st.markdown(f"**Effects:** {', '.join(cann_info['effects'])}")
                    if 'mechanism' in cann_info:
                        st.markdown(f"**Mechanism of Action:** {cann_info['mechanism']}")
                    if 'citations' in cann_info:
                        st.markdown(f"**References:** {cann_info['citations']}")
        
        with learn_tab3:
            st.markdown("### The Entourage Effect")
            st.markdown("""
            <div class="explain-card" style="margin-bottom: 1.5rem;">
                <h4>What Is It?</h4>
                <p>The entourage effect is the theory that cannabis compounds work better together than in isolation. 
                THC alone feels different than THC + CBD + terpenes. The whole plant creates a unique experience 
                that isolated compounds can't replicate.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            #### Key Synergies to Know:
            
            | Combination | Effect |
            |-------------|--------|
            | **THC + CBD** | CBD modulates THC, reducing anxiety and paranoia |
            | **THC + Myrcene** | Enhanced sedation and body effects |
            | **THC + Limonene** | Uplifted mood, reduced anxiety |
            | **CBD + Caryophyllene** | Doubled anti-inflammatory action |
            | **THC + Pinene** | Counteracts short-term memory effects |
            | **CBN + Myrcene + Linalool** | Maximum sedation for sleep |
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #64748b; font-size: 0.85rem; padding: 1rem 0;'>
        <p><strong>StrainMatch Pro v2.1</strong> | Powered by science, designed for budtenders</p>
        <p>Data sources: 43,000+ lab tests from state-certified facilities</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
