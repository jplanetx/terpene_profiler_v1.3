# StrainMatch Pro v2.1 🧬

**Science-Based Cannabis Recommendation Engine**  
Powered by 43,000+ lab tests | Built for dispensary budtenders

---

## Quick Start

### Launch the App
```bash
cd C:\Projects\terpene_profiler_v1.3
streamlit run app_v2.py
```

The app will open at: `http://localhost:8503` or `http://localhost:8504`

---

## What's New in v2.1

### Minor Cannabinoids
Now tracks **6 cannabinoids** instead of 3:
- THC (psychoactive)
- CBD (therapeutic)
- CBN (sedative)
- **CBG** ✨ (mother cannabinoid)
- **THCV** ✨ (energetic)
- **CBC** ✨ (anti-inflammatory)

### Entourage Effect Scoring
Recommendations now award bonus points for scientifically-proven synergies:
- THC + CBD = anxiety modulation
- CBD + Caryophyllene = anti-inflammatory power
- THC + Myrcene = enhanced sedation
- And 4 more synergies...

---

## Files Overview

### Core Application
- **app_v2.py** - Main Streamlit app
- **strain_database_enhanced_v2.csv** - Enhanced database (113 strains)

### Scripts
- **scripts/extract_minor_cannabinoids.py** - Data extraction tool

### Documentation
- **RESEARCH_ENHANCEMENT_REPORT.md** - Scientific foundation
- **ENHANCEMENT_SUMMARY.md** - Latest changes summary
- **CHANGELOG.md** - Version history

---

## Data Source

**Raw Lab Data:**
- Path: `C:\Projects\Terpene-Profile-Parser-for-Cannabis-Strains-master\results.csv`
- Tests: 43,018 certified lab results
- Labs: Analytical 360, SC Labs, PSI Labs (state-certified)
- Coverage: 113 strains with 6 cannabinoids + 8 terpenes

**Extraction Statistics:**
- CBG: 99% strain coverage
- THCV: 85% strain coverage
- CBC: 99% strain coverage
- CBDV: 22% strain coverage (rare)

---

## Re-Generating the Database

If the raw lab data is updated, regenerate the enhanced database:

```bash
python scripts/extract_minor_cannabinoids.py
```

This will:
1. Parse 43,018 lab test results
2. Calculate average cannabinoid values per strain
3. Output: `strain_database_enhanced_v2.csv`
4. Runtime: ~40 seconds

---

## App Architecture

### Symptom Profiles (`SYMPTOM_PROFILES`)
Defines target terpene/cannabinoid profiles for 9 conditions:
- Sleep & Relaxation
- Anxiety & Stress Relief
- Energy & Focus
- Creativity & Euphoria
- Pain Management
- Mood & Depression
- Nausea & Appetite
- Inflammation & Autoimmune
- Seizures & Neurological

### Scoring Algorithm (`calculate_strain_score`)
1. **Terpene Matching** - Awards points for target terpenes
2. **Cannabinoid Matching** - Awards points for target cannabinoids
3. **Penalty System** - Deducts points for conflicting terpenes
4. **Strain Type Bonus** - Extra points for Indica/Sativa preference
5. **Entourage Bonuses** - 7 synergy bonuses (NEW in v2.1)
6. **Normalization** - Final score capped at 100%

### UI Components
- **Find By Need** - Symptom-based recommendation
- **Browse All Strains** - Search and filter library
- **Learn The Science** - Educational content

---

## For Budtenders

### Using the Tool
1. Click symptom category (e.g., "Sleep & Relaxation")
2. Read the "Tell Your Customer" script
3. Review top 6 matched strains
4. Explain why using the science notes
5. Show strain cards with cannabinoid breakdown

### Key Talking Points
- **Entourage Effect** - Whole plant > isolated compounds
- **Terpene Profiles** - Shape the experience more than THC%
- **Minor Cannabinoids** - CBG, THCV, CBC add unique effects
- **Quality Indicators** - High terpene content = premium flower

---

## For Developers

### Tech Stack
- **Python 3.10+**
- **Streamlit 1.52.2**
- **Pandas** (data processing)
- **Altair** (visualizations)
- **NumPy** (calculations)

### Key Functions
```python
load_strain_data()              # Cached database loader
calculate_strain_score()        # Matching algorithm
get_recommendations()           # Top N strains
render_strain_card()            # UI component
create_terpene_radar()          # Terpene visualization
```

### Adding a New Symptom Category
1. Add entry to `SYMPTOM_PROFILES` dict
2. Define target terpenes and cannabinoids
3. Write customer pitch and science note
4. Test recommendations

### Modifying Entourage Bonuses
Edit `calculate_strain_score()` function:
```python
# Example: Add new synergy
if strain.get('cbg_percent', 0) > 0.4 and strain.get('thcv_percent', 0) > 0.15:
    score += 6
    max_score += 6
    details["bonuses"].append("✓ CBG+THCV (energetic focus)")
else:
    max_score += 6
```

---

## Production Deployment

### Requirements
- Python 3.10+
- 2GB RAM minimum
- Modern web browser (Chrome, Firefox, Safari)
- Internet connection (for Google Fonts)

### Recommended Setup
- **POS Tablet:** iPad Pro 12.9" or Surface Pro
- **Display:** Dark mode optimized
- **Network:** Local WiFi for fast loading

### Security Notes
- No user authentication required (standalone tool)
- No data collection or tracking
- No external API calls (except fonts)
- All processing client-side

---

## Troubleshooting

### App Won't Start
```bash
# Check Python version
python --version  # Should be 3.10+

# Install dependencies
pip install streamlit pandas numpy altair

# Run with verbose output
streamlit run app_v2.py --logger.level=debug
```

### Database Not Found
Ensure `strain_database_enhanced_v2.csv` exists in the project root.
If missing, run the extraction script:
```bash
python scripts/extract_minor_cannabinoids.py
```

### Port Already In Use
Streamlit auto-increments ports. If 8501 is taken, it tries 8502, 8503, etc.
Check the terminal output for the actual URL.

---

## Future Enhancements

### Planned Features
- [ ] Strain comparison tool (side-by-side)
- [ ] Natural language search ("something for pain that won't make me sleepy")
- [ ] Patient outcome data integration (Releaf studies)
- [ ] Print-friendly strain info cards
- [ ] Purchase history tracking
- [ ] Personalized recommendations (learning from sales data)

### Data Expansion
- [ ] Integrate Leafly effects database (4,762 strains)
- [ ] Add real patient outcome data
- [ ] Include genetic lineage information
- [ ] Add flavor profile ratings

---

## License & Attribution

**Project:** StrainMatch Pro v2.1  
**Developer:** JPXL Labs  
**AI Assistance:** Claude AI (Anthropic)  
**Data Sources:**
- Terpene-Profile-Parser-for-Cannabis-Strains (GitHub)
- Analytical 360, SC Labs, PSI Labs (certified testing facilities)
- PubMed Cannabis Research
- Frontiers in Pharmacology
- Journal of Cannabis Research

**Disclaimer:** This tool is for educational purposes only. Always consult healthcare professionals for medical advice. Not intended to diagnose, treat, cure, or prevent any disease.

---

## Contact & Support

**Project Owner:** JP @ JPXL Labs  
**GitHub:** _(if public)_  
**Documentation:** See `RESEARCH_ENHANCEMENT_REPORT.md` for scientific references

---

**Last Updated:** December 24, 2024  
**Version:** 2.1.0  
**Status:** Production Ready ✅