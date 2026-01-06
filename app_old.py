import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from typing import List, Dict, Tuple
import os

# Page configuration
st.set_page_config(
    page_title="Terpene Profile Recommender",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Apple-like design
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f7;
    }
    .stButton>button {
        background-color: #007aff;
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 500;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 122, 255, 0.2);
    }
    .stButton>button:hover {
        background-color: #0051d5;
        box-shadow: 0 6px 12px rgba(0, 122, 255, 0.3);
    }
    h1 {
        color: #1d1d1f;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    h2 {
        color: #1d1d1f;
        font-weight: 500;
        margin-top: 2rem;
    }
    h3 {
        color: #424245;
        font-weight: 500;
    }
    .strain-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    </style>
""", unsafe_allow_html=True)

# Symptom to Terpene/Cannabinoid Profile Mapping
SYMPTOM_PROFILES = {
    "Insomnia / Sleep Issues": {
        "description": "For deep, restful sleep",
        "target_terpenes": {
            "myrcene": {"weight": 1.0, "min": 0.40},
            "linalool": {"weight": 0.8, "min": 0.08},
            "caryophyllene": {"weight": 0.6, "min": 0.15}
        },
        "target_cannabinoids": {
            "cbn_percent": {"weight": 1.0, "min": 0.2},
            "thc_percent": {"weight": 0.3, "preferred_range": (15, 20)}
        },
        "strain_type_preference": "Indica"
    },
    "Anxiety / Stress": {
        "description": "Calming without sedation",
        "target_terpenes": {
            "linalool": {"weight": 1.0, "min": 0.08},
            "limonene": {"weight": 0.7, "min": 0.15},
            "caryophyllene": {"weight": 0.6, "min": 0.15}
        },
        "target_cannabinoids": {
            "cbd_percent": {"weight": 0.8, "min": 0.1},
            "thc_percent": {"weight": -0.2, "preferred_range": (10, 18)}
        },
        "strain_type_preference": "Hybrid"
    },
    "Depression / Low Mood": {
        "description": "Uplifting and mood-boosting",
        "target_terpenes": {
            "limonene": {"weight": 1.0, "min": 0.25},
            "pinene": {"weight": 0.6, "min": 0.10},
            "terpinolene": {"weight": 0.5, "min": 0.02}
        },
        "target_cannabinoids": {
            "thc_percent": {"weight": 0.5, "preferred_range": (16, 22)}
        },
        "strain_type_preference": "Sativa"
    },
    "Chronic Pain": {
        "description": "Anti-inflammatory and analgesic",
        "target_terpenes": {
            "caryophyllene": {"weight": 1.0, "min": 0.18},
            "myrcene": {"weight": 0.8, "min": 0.30},
            "humulene": {"weight": 0.5, "min": 0.02}
        },
        "target_cannabinoids": {
            "cbd_percent": {"weight": 0.7, "min": 0.1},
            "thc_percent": {"weight": 0.6, "preferred_range": (15, 25)}
        },
        "strain_type_preference": "Hybrid"
    },
    "Focus / ADHD": {
        "description": "Mental clarity and concentration",
        "target_terpenes": {
            "pinene": {"weight": 1.0, "min": 0.12},
            "limonene": {"weight": 0.7, "min": 0.20},
            "terpinolene": {"weight": 0.6, "min": 0.05}
        },
        "target_cannabinoids": {
            "thc_percent": {"weight": 0.4, "preferred_range": (15, 20)}
        },
        "strain_type_preference": "Sativa"
    },
    "Fatigue / Low Energy": {
        "description": "Energizing and invigorating",
        "target_terpenes": {
            "limonene": {"weight": 1.0, "min": 0.25},
            "pinene": {"weight": 0.8, "min": 0.10},
            "terpinolene": {"weight": 0.6, "min": 0.03}
        },
        "target_cannabinoids": {
            "thc_percent": {"weight": 0.5, "preferred_range": (16, 22)}
        },
        "strain_type_preference": "Sativa"
    },
    "Nausea / Appetite Loss": {
        "description": "Digestive comfort and appetite stimulation",
        "target_terpenes": {
            "myrcene": {"weight": 0.8, "min": 0.30},
            "caryophyllene": {"weight": 0.7, "min": 0.15},
            "limonene": {"weight": 0.6, "min": 0.15}
        },
        "target_cannabinoids": {
            "thc_percent": {"weight": 0.7, "preferred_range": (17, 25)}
        },
        "strain_type_preference": "Indica"
    },
    "Inflammation / Autoimmune": {
        "description": "Powerful anti-inflammatory effects",
        "target_terpenes": {
            "caryophyllene": {"weight": 1.0, "min": 0.20},
            "humulene": {"weight": 0.7, "min": 0.02},
            "myrcene": {"weight": 0.5, "min": 0.25}
        },
        "target_cannabinoids": {
            "cbd_percent": {"weight": 1.0, "min": 5.0},
            "thc_percent": {"weight": 0.3, "preferred_range": (5, 15)}
        },
        "strain_type_preference": "Hybrid"
    },
    "Seizures / Epilepsy": {
        "description": "High CBD for seizure control",
        "target_terpenes": {
            "linalool": {"weight": 0.8, "min": 0.08},
            "caryophyllene": {"weight": 0.7, "min": 0.20},
            "myrcene": {"weight": 0.5, "min": 0.25}
        },
        "target_cannabinoids": {
            "cbd_percent": {"weight": 1.0, "min": 8.0},
            "thc_percent": {"weight": -0.5, "preferred_range": (0, 10)}
        },
        "strain_type_preference": "Sativa"
    }
}

# Terpene information for educational display
TERPENE_INFO = {
    "myrcene": {
        "name": "Myrcene",
        "aroma": "Earthy, musky, herbal",
        "effects": "Sedating, muscle relaxant, anti-inflammatory",
        "color": "#8B4513"
    },
    "limonene": {
        "name": "Limonene", 
        "aroma": "Citrus, lemon, orange",
        "effects": "Mood elevation, stress relief, anti-anxiety",
        "color": "#FFA500"
    },
    "caryophyllene": {
        "name": "Caryophyllene",
        "aroma": "Spicy, peppery, woody",
        "effects": "Anti-inflammatory, pain relief, neuroprotective",
        "color": "#8B0000"
    },
    "linalool": {
        "name": "Linalool",
        "aroma": "Floral, lavender, sweet",
        "effects": "Calming, anti-anxiety, sedating",
        "color": "#9370DB"
    },
    "pinene": {
        "name": "Pinene",
        "aroma": "Pine, fresh, sharp",
        "effects": "Alertness, memory retention, anti-inflammatory",
        "color": "#228B22"
    },
    "humulene": {
        "name": "Humulene",
        "aroma": "Earthy, woody, hoppy",
        "effects": "Anti-inflammatory, appetite suppressant",
        "color": "#DAA520"
    },
    "terpinolene": {
        "name": "Terpinolene",
        "aroma": "Floral, herbal, piney",
        "effects": "Uplifting, antioxidant, sedating",
        "color": "#4682B4"
    }
}

@st.cache_data
def load_strain_data() -> pd.DataFrame:
    """Load the strain database - tries enhanced version first, falls back to standard"""
    # Try enhanced database first
    enhanced_path = 'strain_database_enhanced.csv'
    standard_path = 'strain_database.csv'
    
    if os.path.exists(enhanced_path):
        df = pd.read_csv(enhanced_path)
        st.session_state['using_enhanced'] = True
    elif os.path.exists(standard_path):
        df = pd.read_csv(standard_path)
        st.session_state['using_enhanced'] = False
        # Add data_source column if not present
        if 'data_source' not in df.columns:
            df['data_source'] = 'Curated Database'
    else:
        st.error("❌ Database file not found! Please ensure strain_database.csv or strain_database_enhanced.csv is in the same directory as app.py")
        st.stop()
    
    return df

def calculate_strain_score(strain: pd.Series, symptom_profile: Dict) -> Tuple[float, Dict]:
    """
    Calculate how well a strain matches the target profile
    Returns: (score, details_dict)
    """
    score = 0.0
    max_score = 0.0
    details = {}
    
    # Score terpenes
    for terp, criteria in symptom_profile.get('target_terpenes', {}).items():
        weight = criteria['weight']
        min_threshold = criteria['min']
        max_score += weight * 100
        
        strain_value = strain[terp]
        if strain_value >= min_threshold:
            # Full points if above threshold, bonus for higher values
            terp_score = weight * 100 * (strain_value / min_threshold)
            score += min(terp_score, weight * 150)  # Cap bonus at 150%
            details[terp] = "✓"
        else:
            # Partial points if close
            terp_score = weight * 100 * (strain_value / min_threshold)
            score += terp_score
            details[terp] = "~" if strain_value > min_threshold * 0.5 else "✗"
    
    # Score cannabinoids
    for cann, criteria in symptom_profile.get('target_cannabinoids', {}).items():
        weight = criteria['weight']
        max_score += abs(weight) * 100
        
        strain_value = strain[cann]
        
        if 'min' in criteria:
            # Minimum threshold scoring
            min_threshold = criteria['min']
            if strain_value >= min_threshold:
                cann_score = abs(weight) * 100
                score += cann_score
                details[cann] = "✓"
            else:
                cann_score = abs(weight) * 100 * (strain_value / min_threshold)
                score += cann_score
                details[cann] = "✗"
        
        elif 'preferred_range' in criteria:
            # Range-based scoring
            pref_min, pref_max = criteria['preferred_range']
            if pref_min <= strain_value <= pref_max:
                cann_score = abs(weight) * 100
                score += cann_score
                details[cann] = "✓"
            else:
                # Partial points based on distance from range
                if strain_value < pref_min:
                    distance = pref_min - strain_value
                else:
                    distance = strain_value - pref_max
                cann_score = abs(weight) * 100 * max(0, 1 - (distance / pref_max))
                score += cann_score
                details[cann] = "~"
    
    # Bonus for strain type preference
    strain_type_pref = symptom_profile.get('strain_type_preference', '')
    if strain_type_pref and strain['strain_type'] == strain_type_pref:
        score += 20
        max_score += 20
        details['type_match'] = True
    else:
        max_score += 20
        details['type_match'] = False
    
    # Normalize to 0-100 scale
    normalized_score = (score / max_score) * 100 if max_score > 0 else 0
    
    return normalized_score, details

def get_recommendations(symptom: str, df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """Get top strain recommendations for a symptom"""
    if symptom not in SYMPTOM_PROFILES:
        return pd.DataFrame()
    
    symptom_profile = SYMPTOM_PROFILES[symptom]
    
    # Calculate scores for all strains
    scores = []
    details_list = []
    for idx, strain in df.iterrows():
        score, details = calculate_strain_score(strain, symptom_profile)
        scores.append(score)
        details_list.append(details)
    
    df_copy = df.copy()
    df_copy['match_score'] = scores
    df_copy['match_details'] = details_list
    
    # Sort by score and return top N
    recommendations = df_copy.nlargest(top_n, 'match_score')
    
    return recommendations

def create_terpene_profile_chart(symptom_profile: Dict) -> alt.Chart:
    """Create a visual representation of the target terpene profile"""
    terpene_data = []
    
    for terp, criteria in symptom_profile.get('target_terpenes', {}).items():
        if terp in TERPENE_INFO:
            terpene_data.append({
                'Terpene': TERPENE_INFO[terp]['name'],
                'Importance': criteria['weight'] * 100,
                'Min Target': criteria['min'] * 100,
                'Color': TERPENE_INFO[terp]['color']
            })
    
    df_chart = pd.DataFrame(terpene_data)
    
    chart = alt.Chart(df_chart).mark_bar().encode(
        x=alt.X('Importance:Q', title='Importance Score', scale=alt.Scale(domain=[0, 100])),
        y=alt.Y('Terpene:N', title=None, sort='-x'),
        color=alt.Color('Color:N', scale=None, legend=None),
        tooltip=['Terpene', 'Importance', 'Min Target']
    ).properties(
        height=250,
        title='Target Terpene Profile'
    )
    
    return chart

def create_strain_terpene_chart(strain: pd.Series) -> alt.Chart:
    """Create a terpene profile chart for a specific strain"""
    terpene_cols = ['myrcene', 'limonene', 'caryophyllene', 'linalool', 'pinene', 'humulene', 'terpinolene']
    
    terpene_data = []
    for terp in terpene_cols:
        if terp in TERPENE_INFO and strain[terp] > 0.01:
            terpene_data.append({
                'Terpene': TERPENE_INFO[terp]['name'],
                'Percentage': strain[terp] * 100,
                'Color': TERPENE_INFO[terp]['color']
            })
    
    df_chart = pd.DataFrame(terpene_data)
    
    chart = alt.Chart(df_chart).mark_bar().encode(
        x=alt.X('Percentage:Q', title='Concentration (%)', scale=alt.Scale(domain=[0, 60])),
        y=alt.Y('Terpene:N', title=None, sort='-x'),
        color=alt.Color('Color:N', scale=None, legend=None),
        tooltip=['Terpene', alt.Tooltip('Percentage:Q', format='.2f')]
    ).properties(
        height=200
    )
    
    return chart

# Main App
def main():
    # Header
    st.title("🌿 Terpene Profile Recommender v1.3")
    st.markdown("### Science-Based Cannabis Strain Recommendations")
    st.caption("Data sources: Strain Data Project (2,400+ lab-tested strains) | Mendeley Cannabis Research Dataset | MaxValue Terpene Parser")
    st.markdown("---")
    
    # Load data
    df = load_strain_data()
    
    # Sidebar
    with st.sidebar:
        st.header("About This Tool")
        st.markdown("""
        This recommendation engine uses **chemical profiling** to match cannabis strains 
        to your specific needs.
        
        Unlike simple tag-based systems, we analyze:
        - **Terpene concentrations**
        - **Cannabinoid ratios**
        - **Strain genetics**
        
        to find the best biochemical match.
        """)
        
        st.markdown("---")
        st.markdown("**Data Sources**")
        
        # Show which database is being used
        if st.session_state.get('using_enhanced', False):
            st.success(f"✓ Using Enhanced Database ({len(df)} strains with source attribution)")
        else:
            st.info(f"ℹ️ Using Standard Database ({len(df)} strains)")
        
        st.markdown(f"""
        - [Strain Data Project](https://straindataproject.org/research) (2,400+ lab-tested samples)
        - [Mendeley Research Dataset](https://data.mendeley.com/datasets/6zwcgrttkp/1) (800+ strains)
        - [Terpene Profile Parser](https://github.com/MaxValue/Terpene-Profile-Parser-for-Cannabis-Strains)
        """)
        
        st.markdown("---")
        st.markdown("**Scientific References**")
        st.markdown("""
        - de la Fuente et al. (2019) - Terpene-effect correlations
        - Strain Data Project - GC-MS/FID terpene analysis
        - PubChem, NCBI databases
        
        See DATA_SOURCES.md for complete citations
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("## What are you looking to address?")
        
        selected_symptom = st.selectbox(
            "Select your primary concern:",
            options=list(SYMPTOM_PROFILES.keys()),
            index=0,
            help="Choose the symptom or condition you want to address"
        )
        
        if selected_symptom:
            symptom_info = SYMPTOM_PROFILES[selected_symptom]
            st.info(f"**Goal:** {symptom_info['description']}")
    
    with col2:
        st.markdown("## Quick Stats")
        
        # Display some database statistics
        total_strains = len(df)
        indica_count = len(df[df['strain_type'] == 'Indica'])
        sativa_count = len(df[df['strain_type'] == 'Sativa'])
        hybrid_count = len(df[df['strain_type'] == 'Hybrid'])
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Indica", indica_count)
        metric_col2.metric("Sativa", sativa_count)
        metric_col3.metric("Hybrid", hybrid_count)
    
    st.markdown("---")
    
    # Show the science section
    if selected_symptom:
        st.markdown("## 🔬 The Science Behind Your Match")
        
        symptom_profile = SYMPTOM_PROFILES[selected_symptom]
        
        # Target profile visualization
        col_chart1, col_chart2 = st.columns([3, 2])
        
        with col_chart1:
            chart = create_terpene_profile_chart(symptom_profile)
            st.altair_chart(chart, use_container_width=True)
        
        with col_chart2:
            st.markdown("### Key Terpenes")
            for terp, criteria in symptom_profile.get('target_terpenes', {}).items():
                if terp in TERPENE_INFO:
                    info = TERPENE_INFO[terp]
                    st.markdown(f"""
                    **{info['name']}**  
                    *{info['aroma']}*  
                    {info['effects']}
                    """)
                    st.markdown("---")
        
        # Get recommendations
        st.markdown("## 🎯 Top Strain Matches")
        
        recommendations = get_recommendations(selected_symptom, df, top_n=5)
        
        if not recommendations.empty:
            for idx, strain in recommendations.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="strain-card">
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Strain header
                    col_name, col_score, col_type = st.columns([3, 1, 1])
                    
                    with col_name:
                        st.markdown(f"### {strain['strain_name']}")
                        # Show data source if available
                        if 'data_source' in strain and pd.notna(strain['data_source']):
                            st.caption(f"Source: {strain['data_source']}")
                    
                    with col_score:
                        score_color = "#34c759" if strain['match_score'] >= 80 else "#ff9500" if strain['match_score'] >= 60 else "#ff3b30"
                        st.markdown(f"<h3 style='color: {score_color};'>{strain['match_score']:.0f}% Match</h3>", unsafe_allow_html=True)
                    
                    with col_type:
                        type_emoji = "🌙" if strain['strain_type'] == "Indica" else "☀️" if strain['strain_type'] == "Sativa" else "⚖️"
                        st.markdown(f"<h3>{type_emoji} {strain['strain_type']}</h3>", unsafe_allow_html=True)
                    
                    # Cannabinoid info
                    cann_col1, cann_col2, cann_col3 = st.columns(3)
                    cann_col1.metric("THC", f"{strain['thc_percent']:.1f}%")
                    cann_col2.metric("CBD", f"{strain['cbd_percent']:.1f}%")
                    cann_col3.metric("CBN", f"{strain['cbn_percent']:.1f}%")
                    
                    # Terpene profile chart
                    st.markdown("**Terpene Profile:**")
                    terp_chart = create_strain_terpene_chart(strain)
                    st.altair_chart(terp_chart, use_container_width=True)
                    
                    # Effects and uses
                    effect_col, use_col = st.columns(2)
                    
                    with effect_col:
                        st.markdown("**Primary Effects:**")
                        effects = strain['primary_effects'].split(',')
                        st.markdown(" • " + "  \n • ".join(effects))
                    
                    with use_col:
                        st.markdown("**Medical Uses:**")
                        uses = strain['medical_uses'].split(',')
                        st.markdown(" • " + "  \n • ".join(uses))
                    
                    st.markdown("---")
        else:
            st.warning("No strains found for this profile. Try a different symptom.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #86868b; font-size: 0.9em;'>
    <p><strong>Disclaimer:</strong> This tool is for educational purposes only. 
    Consult with a healthcare professional before using cannabis for medical purposes.</p>
    <p><strong>Data Sources:</strong> Strain Data Project (Iron Stem) | Mendeley Research Dataset (de la Fuente et al., 2019) | 
    Terpene Profile Parser (MaxValue) | PubChem Database</p>
    <p>Terpene Profile Recommender v1.3 | Built with science, designed for wellness</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
