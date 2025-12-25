"""
Extract and aggregate real lab data from Terpene Profile Parser repository
Creates enhanced strain database with statistical validation
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Load the massive lab dataset
print("Loading 43,000+ lab samples...")
df = pd.read_csv(
    r'C:\Projects\Terpene-Profile-Parser-for-Cannabis-Strains-master\Terpene-Profile-Parser-for-Cannabis-Strains-master\results.csv',
    low_memory=False
)

print(f"OK Loaded {len(df):,} samples from {df['Database Name'].nunique()} labs")
print(f"OK {df['Sample Name'].nunique():,} unique strain names")

# Key terpene columns (standardized names)
terpene_map = {
    'beta-Myrcene': 'myrcene',
    'delta-Limonene': 'limonene', 
    'beta-Caryophyllene': 'caryophyllene',
    'Linalool': 'linalool',
    'alpha-Pinene': 'alpha_pinene',
    'beta-Pinene': 'beta_pinene',
    'alpha-Humulene': 'humulene',
    'Terpinolene': 'terpinolene',
    'Ocimene': 'ocimene'
}

cannabinoid_map = {
    'delta-9 THC': 'thc',
    'CBD': 'cbd',
    'CBN': 'cbn'
}

# Convert percentages to decimals and handle NaN
for col in list(terpene_map.keys()) + list(cannabinoid_map.keys()):
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce') / 100  # Convert to decimal

print("\n" + "="*60)
print("AGGREGATING BY STRAIN NAME")
print("="*60)

# Group by strain name and calculate statistics
strain_data = []

for strain_name, group in df.groupby('Sample Name'):
    # Need at least 3 samples for statistical validity
    if len(group) < 3:
        continue
    
    # Skip if strain name is too generic or unclear
    if len(strain_name) < 3 or strain_name.lower() in ['trim', 'shake', 'mix', 'blend']:
        continue
    
    # Calculate means for terpenes
    terp_means = {}
    for orig_col, std_col in terpene_map.items():
        if orig_col in group.columns:
            values = group[orig_col].dropna()
            if len(values) >= 2:  # Need at least 2 valid readings
                terp_means[std_col] = values.mean()
    
    # Calculate means for cannabinoids
    cann_means = {}
    for orig_col, std_col in cannabinoid_map.items():
        if orig_col in group.columns:
            values = group[orig_col].dropna()
            if len(values) >= 2:
                cann_means[std_col] = values.mean()
    
    # Only include if we have good terpene data
    if len(terp_means) >= 4:  # At least 4 terpenes measured
        strain_info = {
            'strain_name': strain_name,
            'sample_count': len(group),
            'lab_sources': ', '.join(group['Database Name'].unique()),
            **terp_means,
            **cann_means
        }
        strain_data.append(strain_info)

# Create DataFrame
result_df = pd.DataFrame(strain_data)

print(f"\nOK Aggregated {len(result_df)} strains with sufficient data")
print(f"  (from {len(result_df[result_df['sample_count'] >= 5])} with 5+ samples)")

# Fill missing values with 0
terpene_cols = list(terpene_map.values())
cannabinoid_cols = list(cannabinoid_map.values())

for col in terpene_cols + cannabinoid_cols:
    if col in result_df.columns:
        result_df[col] = result_df[col].fillna(0)
    else:
        result_df[col] = 0

# Sort by sample count (most tested strains first)
result_df = result_df.sort_values('sample_count', ascending=False)

# Save top 100 strains
top_strains = result_df.head(100)

print("\n" + "="*60)
print("TOP 10 MOST-TESTED STRAINS")
print("="*60)
for idx, row in top_strains.head(10).iterrows():
    print(f"{row['strain_name']}: {row['sample_count']} samples from {row['lab_sources']}")

# Calculate combined pinene (alpha + beta)
if 'alpha_pinene' in top_strains.columns and 'beta_pinene' in top_strains.columns:
    top_strains['pinene'] = top_strains['alpha_pinene'] + top_strains['beta_pinene']
else:
    top_strains['pinene'] = 0

# Prepare final output format matching your app
output_df = pd.DataFrame({
    'strain_name': top_strains['strain_name'],
    'thc_percent': (top_strains['thc'] * 100).round(1),
    'cbd_percent': (top_strains['cbd'] * 100).round(2),
    'cbn_percent': (top_strains['cbn'] * 100).round(2),
    'myrcene': top_strains['myrcene'].round(4),
    'limonene': top_strains['limonene'].round(4),
    'caryophyllene': top_strains['caryophyllene'].round(4),
    'linalool': top_strains['linalool'].round(4),
    'pinene': top_strains['pinene'].round(4),
    'humulene': top_strains['humulene'].round(4),
    'terpinolene': top_strains['terpinolene'].round(4),
    'ocimene': top_strains['ocimene'].round(4),
    'sample_count': top_strains['sample_count'],
    'data_source': 'Lab-Aggregated (' + top_strains['sample_count'].astype(str) + ' samples)',
    'lab_sources': top_strains['lab_sources']
})

# Save to CSV
output_path = r'C:\Projects\terpene_profiler_v1.3\strain_database_lab_verified.csv'
output_df.to_csv(output_path, index=False)

print(f"\nOK Saved {len(output_df)} lab-verified strains to:")
print(f"  {output_path}")

# Show sample data
print("\n" + "="*60)
print("SAMPLE OUTPUT (First 3 Strains)")
print("="*60)
print(output_df.head(3).to_string())

print("\n" + "="*60)
print("STATISTICS")
print("="*60)
print(f"Average samples per strain: {output_df['sample_count'].mean():.1f}")
print(f"Median samples per strain: {output_df['sample_count'].median():.0f}")
print(f"Max samples for one strain: {output_df['sample_count'].max()}")
print(f"Strains with 10+ samples: {len(output_df[output_df['sample_count'] >= 10])}")
print(f"Strains with 20+ samples: {len(output_df[output_df['sample_count'] >= 20])}")

print("\nDONE - EXTRACTION COMPLETE!")
