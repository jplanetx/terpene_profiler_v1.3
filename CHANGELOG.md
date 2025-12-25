# Changelog - StrainMatch Pro

All notable changes to this project will be documented in this file.

## [2.1.0] - 2024-12-24

### Added
- **Minor Cannabinoid Support**: CBG, THCV, CBC, CBDV extraction and integration
- **Entourage Effect Scoring**: 7 new scientifically-backed synergy bonuses
  * THC + CBD (anxiety modulation)
  * THC + Myrcene (enhanced sedation)
  * CBD + Caryophyllene (anti-inflammatory power)
  * Limonene + Linalool (calm + uplift)
  * CBG + CBC (brain health)
  * THC + Pinene (memory protection)
  * High terpene content bonus
- **Enhanced Database**: `strain_database_enhanced_v2.csv` with 4 new cannabinoid columns
- **Extraction Script**: `scripts/extract_minor_cannabinoids.py` for data processing
- **CBDV Information**: Added to cannabinoid encyclopedia
- **Expanded UI**: Strain cards now display 6 cannabinoids (was 4)

### Changed
- Database source: `strain_database_enhanced.csv` → `strain_database_enhanced_v2.csv`
- Scoring algorithm: Now includes entourage effect bonuses (up to 48 additional points)
- Symptom profiles: 7 categories enhanced with minor cannabinoid targeting
  * Sleep & Relaxation (added CBC)
  * Anxiety & Stress Relief (added CBC)
  * Energy & Focus (added CBG)
  * Pain Management (added CBC)
  * Nausea & Appetite (added CBC)
  * Inflammation & Autoimmune (added CBC, CBG)
  * Seizures & Neurological (added CBDV)

### Fixed
- None - no bugs found during enhancement

### Data
- **Lab Coverage**: 112/113 strains have CBG data (99%)
- **Lab Coverage**: 96/113 strains have THCV data (85%)
- **Lab Coverage**: 112/113 strains have CBC data (99%)
- **Lab Coverage**: 25/113 strains have CBDV data (22%)
- **Source**: 43,018 certified lab test results

---

## [2.0.0] - 2024-12-23 (Previous Version)

### Added
- Complete UI/UX redesign with dark mode
- Research-backed symptom categories
- Terpene encyclopedia with consumer-friendly language
- Cannabinoid information system
- Enhanced database with lab-verified data
- Customer pitch scripts for budtenders
- Science notes for educational purposes

### Changed
- Database: Migrated from `strain_database.csv` to `strain_database_enhanced.csv`
- UI: Modern glassmorphism design with gradient accents
- Fonts: Plus Jakarta Sans + JetBrains Mono
- Color scheme: Cannabis industry professional standards

---

## [1.3.0] - Original Version

### Features
- Basic strain recommendation by symptom
- Terpene profile visualization
- Simple database of lab-tested strains
- Basic UI with Streamlit defaults

---

**Maintained by:** JPXL Labs  
**App:** StrainMatch Pro (formerly Terpene Profile Recommender)  
**Tech Stack:** Python, Streamlit, Pandas, Altair