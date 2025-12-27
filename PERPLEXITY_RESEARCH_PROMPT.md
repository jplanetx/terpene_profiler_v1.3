# PERPLEXITY RESEARCH PROMPT: Cannabis Terpene & Cannabinoid Data Validation & Expansion

## OBJECTIVE
You are researching data quality and expansion opportunities for StrainMatch Pro, a cannabis recommendation engine used by dispensary budtenders. The app currently uses 113 strains with 6,460+ lab test samples. Your mission: validate current data sources, identify gaps, and find additional high-quality datasets to expand coverage and accuracy.

---

## CONTEXT (Review Attached Files First)
I've attached three documents that provide complete context:
1. **DATA_SUMMARY_FOR_RESEARCH.md** - Current dataset structure, sample sizes, and known gaps
2. **PROVENANCE.md** - Complete source attribution for all 113 strains
3. **RESEARCH_ENHANCEMENT_REPORT.md** - Research methodology and data efficacy analysis

Please review these thoroughly before proceeding with research.

---

## RESEARCH TASKS

### PART 1: Validate Current Data Sources (High Priority)

**Task 1A: Verify Laboratory Credibility**
Research the three labs currently used:
- **Analytical 360** (Washington State)
- **SC Labs** (California)  
- **PSI Labs** (Michigan)

Questions to answer:
1. Are these labs still operating and state-certified in 2024-2025?
2. What are their current testing methodologies (GC-MS, HPLC, LC-MS)?
3. Are there any controversies, license suspensions, or quality issues?
4. How do they compare to other top-tier cannabis testing labs?
5. Do they publish their testing protocols/standards publicly?

**Task 1B: Assess Research Dataset Validity**
Evaluate the academic sources:
- **Mendeley Cannabis Research Dataset** (de la Fuente et al., 2019) - data.mendeley.com/datasets/6zwcgrttkp/1
- **Terpene Profile Parser** repository

Questions to answer:
1. Has this research been cited in subsequent studies? (Check Google Scholar)
2. Are there any corrections, retractions, or critiques?
3. What is the current citation count and academic impact?
4. Have newer versions or updates been published since 2019?

**Task 1C: Evaluate Data Age & Relevance**
Our lab data is from 2013-2019, manual data from 2019-2022.

Questions to answer:
1. How much have cannabis genetics/potency changed since 2019?
2. Are 2013-2019 terpene profiles still representative of modern strains?
3. What is the typical shelf-life of cannabis strain data validity?
4. Should we deprecate any data due to age?

---

### PART 2: Identify Data Gaps & Prioritize Expansion (High Priority)

**Task 2A: Coverage Gap Analysis**
Identify the most important missing strains:

Questions to answer:
1. What are the top 20 most popular cannabis strains in 2024-2025? (Check Leafly, Weedmaps rankings)
2. Which of these top strains are MISSING from our database?
3. Are there important therapeutic strains (high-CBD, high-CBG) we're missing?
4. What are the most popular new strains (2020-2024) that don't exist in our data?

**Task 2B: Chemical Analysis Gap Assessment**
Our database tracks 7 major cannabinoids and 8 terpenes.

Questions to answer:
1. What other cannabinoids should we track? (e.g., CBDA, CBGA, Delta-8 THC, CBT)
2. What other terpenes are clinically significant? (e.g., bisabolol, nerolidol, guaiol, geraniol)
3. Should we track flavonoids? If so, which ones?
4. Are there emerging biomarkers or compounds worth tracking?

**Task 2C: Metadata Enhancement Opportunities**
Questions to answer:
1. What metadata would make recommendations more accurate?
   - Growing conditions (indoor/outdoor/greenhouse)?
   - Phenotype variations?
   - Genetic lineage/parent strains?
   - Harvest season/age?
2. Are there standardized ways to capture this metadata in industry databases?

---

### PART 3: Find New High-Quality Data Sources (Critical Priority)

**Task 3A: Laboratory Data Sources**
Find additional state-certified cannabis testing labs with public data:

Requirements:
- Must be state-certified/licensed
- Must publish testing data (even if paywalled)
- Must use validated methodologies (GC-MS, HPLC, LC-MS)
- Prefer labs with >1000 sample repository

Questions to answer:
1. Which top-tier labs publish their data? (e.g., Steep Hill, CannaSafe, ACS Laboratory)
2. Are there lab data aggregators or APIs available?
3. Do any labs offer bulk data downloads or research partnerships?
4. What is the cost (if any) to access this data?

**Task 3B: Academic & Research Databases**
Find peer-reviewed cannabis research with chemical profile data:

Search for:
- PubMed/PubMed Central cannabis terpene studies (2020-2025)
- Research datasets on Mendeley, Figshare, Dryad, Zenodo
- University cannabis research programs with public data
- Clinical trial registries with strain-specific data

Questions to answer:
1. Are there newer datasets than the 2019 Mendeley dataset?
2. Which universities are publishing cannabis chemical profile data?
3. Are there any large-scale strain characterization studies (>100 strains)?
4. Do any studies include both lab data AND patient outcomes?

**Task 3C: Industry Data Sources**
Identify reputable commercial/industry databases:

Potential sources:
- Leafly API / dataset
- Weedmaps data
- Phylos Bioscience (genetic data)
- Cannabis Genomic Research Initiative
- Medicinal Genomics
- Confident Cannabis platform

Questions to answer:
1. Do these platforms offer data licensing or API access?
2. What is their data validation methodology?
3. How large are their datasets?
4. Are there any free/open-source industry datasets?
5. What partnerships or collaborations exist for research access?

**Task 3D: International Data Sources**
Our current data is US-focused.

Questions to answer:
1. Are there Canadian cannabis databases (legal since 2018)?
2. What about European medical cannabis databases?
3. Israeli medical cannabis research (world leaders in cannabis medicine)?
4. Are there WHO or international cannabis databases?

---

### PART 4: Emerging Research & Future-Proofing (Medium Priority)

**Task 4A: Terpene-Effect Correlation Research**
Questions to answer:
1. What is the latest research on the "entourage effect"?
2. Are there validated terpene→effect correlations? (e.g., myrcene→sedation)
3. Which terpene ratios predict specific medical outcomes?
4. Any studies debunking common assumptions about terpenes?

**Task 4B: Cannabinoid Ratio Research**
Questions to answer:
1. What THC:CBD ratios are optimal for specific conditions?
2. Is there research on minor cannabinoid synergies (CBC+CBG, THCV+CBDV)?
3. What cannabinoid profiles work best for pediatric/geriatric patients?

**Task 4C: Personalized Cannabis Medicine**
Questions to answer:
1. Are there pharmacogenomic studies (genetic factors affecting cannabis response)?
2. Research on dosage optimization based on terpene profiles?
3. Any clinical trials linking specific strains to medical outcomes?

---

### PART 5: Data Quality & Standardization Issues (High Priority)

**Task 5A: Industry Testing Standards**
Questions to answer:
1. Are there standardized testing protocols across states/countries?
2. What are the known issues with cannabis lab testing accuracy?
3. Have there been lab scandals or data manipulation cases we should know about?
4. What is the margin of error for typical terpene/cannabinoid tests?

**Task 5B: Data Normalization Challenges**
Questions to answer:
1. How do different labs handle detection limits for trace terpenes?
2. Are there standardized naming conventions for terpenes/cannabinoids?
3. How do labs account for degradation (THC→CBN over time)?
4. What are best practices for averaging multiple lab results?

**Task 5C: Regulatory Landscape**
Questions to answer:
1. Are there upcoming changes to cannabis testing regulations?
2. Which states have the strictest/most reliable testing requirements?
3. Are there federal initiatives for cannabis data standardization?

---

## OUTPUT FORMAT

Please structure your research findings as follows:

### 1. EXECUTIVE SUMMARY
- Key findings (2-3 paragraphs)
- Biggest opportunities identified
- Critical risks or data quality concerns
- Recommended immediate next steps

### 2. CURRENT DATA VALIDATION
For each current source (Analytical 360, SC Labs, PSI Labs, Mendeley dataset):
- **Status:** Active/Inactive, Credible/Questionable
- **Reliability Score:** 1-10 with justification
- **Recommendations:** Keep/Deprecate/Supplement

### 3. HIGH-PRIORITY DATA SOURCES (Top 5)
For each recommended new source:
- **Source Name & URL**
- **Data Type:** Lab data / Research dataset / Industry database
- **Coverage:** # of strains, sample sizes
- **Access:** Free / Paid / Partnership required
- **Reliability:** Assessment and validation
- **Integration Effort:** Easy / Medium / Hard
- **Priority Ranking:** 1-5 with justification

### 4. GAP ANALYSIS
- **Missing Strains:** Top 20 popular strains we don't have
- **Missing Compounds:** Cannabinoids/terpenes we should add
- **Missing Metadata:** Additional data fields worth collecting

### 5. EMERGING RESEARCH HIGHLIGHTS
- Latest studies on terpene-effect correlations
- New findings on cannabinoid synergies
- Relevant clinical trial results (2020-2025)

### 6. RISKS & CONCERNS
- Data quality issues identified
- Methodological problems with current sources
- Regulatory or legal concerns
- Potential bias in data sources

### 7. IMPLEMENTATION ROADMAP
**Phase 1 (Immediate - 0-30 days):**
- Validate/deprecate current sources
- Add top 3 new data sources

**Phase 2 (Short-term - 1-3 months):**
- Expand strain coverage to top 200 strains
- Add missing compounds (cannabinoids/terpenes)

**Phase 3 (Long-term - 3-12 months):**
- Integrate clinical outcome data
- Build pharmacogenomic recommendations

---

## SUCCESS CRITERIA

Your research will be considered successful if it provides:
1. ✅ Clear validation or concerns about our 3 current lab sources
2. ✅ At least 3-5 high-quality new data sources with access paths
3. ✅ Prioritized list of missing strains to add (top 20+)
4. ✅ Evidence-based recommendations on new compounds to track
5. ✅ Actionable roadmap for expanding from 113 to 200+ strains
6. ✅ Risk assessment of any data quality issues
7. ✅ Latest research findings on terpene/cannabinoid effects (2020-2025)

---

## ADDITIONAL CONTEXT

**App Use Case:**
Dispensary budtenders use this tool to recommend strains based on customer needs:
- "I need help sleeping" → Match to sedative terpene profiles
- "Chronic pain management" → High-CBD or specific cannabinoid ratios
- "Focus for ADHD" → Pinene/limonene-dominant profiles
- "Appetite stimulation" → THCV-low, myrcene-high strains

**Target User:**
Medical cannabis patients and recreational users seeking evidence-based recommendations rather than "bro science."

**Competitive Landscape:**
We're competing with Leafly, Weedmaps, and budtender intuition. Our advantage is statistical validation and transparent data sourcing.

**Budget:**
We can invest in data licensing if ROI is clear, but prefer open-source or research partnership models.

---

## BEGIN RESEARCH

Please proceed with comprehensive research on all tasks above. Prioritize:
1. Validation of current sources (Part 1)
2. Finding new high-quality data sources (Part 3)
3. Gap analysis for missing strains (Part 2A)

Take your time and be thorough - this research will determine the roadmap for expanding StrainMatch Pro from 113 strains to a comprehensive industry-leading dataset.
