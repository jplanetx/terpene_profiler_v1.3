# StrainMatch Pro - Current Data Summary

## Dataset Overview
- **Total Strains:** 113 unique cannabis strains
- **Total Lab Samples Represented:** 6,460+ individual tests
- **Data Sources:** Multi-lab aggregation + peer-reviewed research

## Data Structure (25 columns)

### Cannabinoids
- THC % (primary psychoactive)
- CBD % (therapeutic, non-psychoactive)
- CBN % (sedative effects)
- CBG % (anti-inflammatory)
- THCV % (appetite suppressant)
- CBC % (anti-inflammatory)
- CBDV % (anti-convulsant)

### Terpenes (% by weight)
- Myrcene (sedative, muscle relaxant)
- Limonene (mood elevation, stress relief)
- Caryophyllene (anti-inflammatory, pain relief)
- Linalool (anxiety relief, sleep aid)
- Pinene (alertness, memory)
- Humulene (appetite suppressant)
- Terpinolene (sedative, antioxidant)
- Ocimene (antifungal, decongestant)

### Metadata
- Strain name
- Primary effects (e.g., "Relaxation,Euphoria,Creativity")
- Medical uses (e.g., "Pain,Depression,Insomnia")
- Strain type (Indica/Sativa/Hybrid)
- Data quality tier (Hybrid/Lab-Only/Manual-Only)
- Sample count (10-425 lab tests per strain)
- Data source attribution

## Data Quality Breakdown

### Tier 1: Hybrid Sources (28 strains - HIGHEST QUALITY)
- Terpenes: 10-425 lab samples (GC-MS/FID tested)
- Cannabinoids: Research-based modern values
- Effects: Manually curated from studies
- Examples: Blue Dream (425 samples), Girl Scout Cookies (166 samples)

### Tier 2: Lab-Only (72 strains - HIGH STATISTICAL VALIDITY)
- All data: 10-273 lab samples
- Multi-lab cross-validation
- Examples: Dutch Treat (273 samples), Grape Ape (120 samples)

### Tier 3: Manual-Only (13 strains - RESEARCH-BASED)
- Curated from peer-reviewed sources
- Includes therapeutic high-CBD strains
- Examples: Granddaddy Purple, Northern Lights, ACDC

## Current Laboratory Sources
1. **Analytical 360** (Washington State - Licensed)
2. **SC Labs** (California - State Certified)
3. **PSI Labs** (Michigan - State Certified)

## Current Research Sources
1. **Strain Data Project** (straindataproject.org)
2. **Mendeley Cannabis Research Dataset** (de la Fuente et al., 2019)
3. **Terpene Profile Parser** (43,018 lab samples)

## Sample Data (First 5 Strains)

**Blue Dream** (Hybrid - 425 lab samples)
- THC: 17.0% | CBD: 0.1% | CBN: 0.0%
- Myrcene: 0.72% | Limonene: 0.10% | Caryophyllene: 0.58%
- Effects: Relaxation, Euphoria, Creativity
- Medical: Pain, Depression, Nausea, Insomnia

**Dutch Treat** (Sativa - 273 lab samples)
- THC: 1.4% | CBD: 0.15% | CBN: 0.1%
- Myrcene: 0.37% | Limonene: 1.44% | Linalool: 1.55%
- Effects: Sedation, Euphoria, Energy
- Medical: Anxiety, Depression

**Harlequin** (Sativa - 188 lab samples - HIGH CBD)
- THC: 9.0% | CBD: 9.0% | CBN: 0.0%
- Linalool: 0.92% | Pinene: 0.31%
- Effects: Relaxation, Focus, Clarity
- Medical: Pain, Anxiety, Inflammation, Seizures

**Girl Scout Cookies** (Hybrid - 166 lab samples)
- THC: 18.0% | CBD: 0.1% | CBN: 0.1%
- Caryophyllene: 0.91% | Linalool: 0.67% | Humulene: 1.04%
- Effects: Euphoria, Relaxation, Happiness
- Medical: Pain, Nausea, Appetite, Stress

**Sour Diesel** (Sativa - 137 lab samples)
- THC: 20.0% | CBD: 0.1% | CBN: 0.0%
- Caryophyllene: 0.90% | Humulene: 1.23%
- Effects: Energy, Euphoria, Creativity
- Medical: Depression, Fatigue, Stress, Focus

## Known Data Gaps

### Coverage Gaps
- Limited representation of rare/exotic strains
- Few landrace strains (pure genetics)
- Limited autoflower strain data
- Missing many new hybrid strains (2020-2024)

### Chemical Analysis Gaps
- Minor cannabinoids (CBG, CBC, THCV) inconsistently reported
- Rare terpenes (bisabolol, nerolidol, guaiol) not tracked
- Flavonoid data completely absent
- No degradation pathway data (THC→CBN over time)

### Metadata Gaps
- Growing conditions not tracked (indoor/outdoor/greenhouse)
- No phenotype variation data (same strain, different growers)
- Limited lineage/genetics information
- No harvest date/age data

### Medical Data Gaps
- Dosage information absent
- No contraindications/side effects data
- Limited pediatric therapeutic strain data
- No drug interaction warnings

## Data Reliability Assessment

**Strengths:**
✅ Multi-lab cross-validation for terpene profiles
✅ Large sample sizes (10-425 tests per strain)
✅ State-certified laboratory testing
✅ Full provenance attribution
✅ Peer-reviewed research integration

**Limitations:**
⚠️ Lab data from 2013-2019 (some cannabinoid values outdated)
⚠️ No post-2020 strain coverage
⚠️ Limited minor cannabinoid data
⚠️ Effects/medical uses are subjective/user-reported
⚠️ No clinical trial data

## Use Case
This dataset powers a budtender recommendation tool that matches customer needs (sleep, pain relief, focus, etc.) to strains based on:
1. Terpene profile similarity
2. Cannabinoid ratios
3. Documented effects/medical uses
4. Statistical validation from lab testing
