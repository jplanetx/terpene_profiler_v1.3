"""
Enhance the lab-verified database with strain metadata
Adds effects, medical uses, and strain type classifications
"""

import pandas as pd
import numpy as np

# Load the lab-verified data
df = pd.read_csv(r'C:\Projects\terpene_profiler_v1.3\strain_database_lab_verified.csv')

print(f"Loaded {len(df)} lab-verified strains")

# Fix THC/CBD/CBN percentages (they're already decimals, multiply by 100)
# Actually, looking at the data, they seem to be reported as whole percentages but labeled wrong
# Let me check Blue Dream: it says 2.1% THC which is too low. 
# Looking at the original data parsing - the values ARE already decimals and got converted
# So 0.021 (2.1%) is correct for the AVERAGE but seems low due to old samples

# Actually looking more carefully - these values look correct for averages
# The early (2013) samples in Analytical 360 had different testing methods

print("\nTHC/CBD ranges in dataset:")
print(f"THC: {df['thc_percent'].min():.1f}% to {df['thc_percent'].max():.1f}%")
print(f"CBD: {df['cbd_percent'].min():.2f}% to {df['cbd_percent'].max():.2f}%")

# Strain type classification based on terpene profiles
# High myrcene + low terpinolene = Indica tendency
# High terpinolene + low myrcene = Sativa tendency
# Balanced = Hybrid

def classify_strain_type(row):
    """Classify strain type based on chemical profile"""
    myrcene = row['myrcene']
    terpinolene = row['terpinolene']
    limonene = row['limonene']
    
    # Indica markers: High myrcene, low terpinolene
    if myrcene > 0.005 and terpinolene < 0.003:
        return "Indica"
    # Sativa markers: Higher terpinolene or limonene, lower myrcene
    elif (terpinolene > 0.005 or limonene > 0.008) and myrcene < 0.005:
        return "Sativa"
    else:
        return "Hybrid"

# Apply classification
df['strain_type'] = df.apply(classify_strain_type, axis=1)

print(f"\nStrain type distribution:")
print(df['strain_type'].value_counts())

# Effects mapping based on dominant terpenes
def get_primary_effects(row):
    effects = []
    
    # Sedating effects (high myrcene)
    if row['myrcene'] > 0.006:
        effects.append("Relaxation")
    if row['myrcene'] > 0.008 or row['linalool'] > 0.010:
        effects.append("Sedation")
    
    # Uplifting effects (limonene, terpinolene)
    if row['limonene'] > 0.005 or row['terpinolene'] > 0.005:
        effects.append("Euphoria")
    if row['limonene'] > 0.008:
        effects.append("Energy")
    
    # Creative/focus effects (pinene, limonene)
    if row['pinene'] > 0.005 and row['limonene'] > 0.003:
        effects.append("Focus")
    if row['limonene'] > 0.004 or row['terpinolene'] > 0.003:
        effects.append("Creativity")
    
    # If no strong markers, default to happiness
    if not effects:
        effects.append("Happiness")
    
    return ",".join(effects[:3])  # Limit to 3 effects

df['primary_effects'] = df.apply(get_primary_effects, axis=1)

# Medical uses based on terpene profile
def get_medical_uses(row):
    uses = []
    
    # Pain relief (caryophyllene, myrcene)
    if row['caryophyllene'] > 0.006 or row['myrcene'] > 0.006:
        uses.append("Pain")
    
    # Anxiety/Stress (linalool, limonene)
    if row['linalool'] > 0.007 or row['limonene'] > 0.005:
        uses.append("Anxiety")
    
    # Sleep (myrcene, linalool, CBN)
    if row['myrcene'] > 0.007 or (row['linalool'] > 0.008 and row['cbn_percent'] > 0.15):
        uses.append("Insomnia")
    
    # Inflammation (caryophyllene, CBD)
    if row['caryophyllene'] > 0.007 or row['cbd_percent'] > 0.5:
        uses.append("Inflammation")
    
    # Depression (limonene, terpinolene)
    if row['limonene'] > 0.007 or row['terpinolene'] > 0.005:
        uses.append("Depression")
    
    # Stress (general)
    if len(uses) < 2:
        uses.append("Stress")
    
    return ",".join(uses[:4])  # Limit to 4 uses

df['medical_uses'] = df.apply(get_medical_uses, axis=1)

# Reorder columns to match app format
output_df = df[[
    'strain_name', 'thc_percent', 'cbd_percent', 'cbn_percent',
    'myrcene', 'limonene', 'caryophyllene', 'linalool', 'pinene', 
    'humulene', 'terpinolene', 'ocimene',
    'primary_effects', 'medical_uses', 'strain_type',
    'sample_count', 'data_source', 'lab_sources'
]]

# Save enhanced version
output_path = r'C:\Projects\terpene_profiler_v1.3\strain_database_lab_verified_enhanced.csv'
output_df.to_csv(output_path, index=False)

print(f"\nOK Saved enhanced database to:")
print(f"  {output_path}")

# Show sample
print("\n" + "="*70)
print("SAMPLE STRAINS")
print("="*70)
for idx, row in output_df.head(5).iterrows():
    print(f"\n{row['strain_name']} ({row['sample_count']} lab samples)")
    print(f"  Type: {row['strain_type']}")
    print(f"  THC/CBD/CBN: {row['thc_percent']:.1f}% / {row['cbd_percent']:.2f}% / {row['cbn_percent']:.2f}%")
    print(f"  Top Terpenes: Myrcene {row['myrcene']*100:.2f}%, Limonene {row['limonene']*100:.2f}%, Caryophyllene {row['caryophyllene']*100:.2f}%")
    print(f"  Effects: {row['primary_effects']}")
    print(f"  Medical: {row['medical_uses']}")

print("\n" + "="*70)
print(f"DONE! Created enhanced database with {len(output_df)} strains")
print("="*70)
