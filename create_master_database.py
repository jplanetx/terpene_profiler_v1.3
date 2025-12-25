"""
Create master hybrid database combining lab-verified and manual data
Tracks provenance of every data point for full transparency
"""

import pandas as pd
import numpy as np

print("="*70)
print("CREATING MASTER HYBRID DATABASE")
print("="*70)

# Load both databases
lab_df = pd.read_csv(r'C:\Projects\terpene_profiler_v1.3\strain_database_lab_verified_enhanced.csv')
manual_df = pd.read_csv(r'C:\Projects\terpene_profiler_v1.3\strain_database_manual.csv')

print(f"\nLoaded:")
print(f"  Lab-verified: {len(lab_df)} strains")
print(f"  Manual: {len(manual_df)} strains")

# Standardize column names
# Lab data already has correct format
# Manual data needs sample_count and lab_sources columns

# Add tracking columns to manual data
manual_df['sample_count'] = 1  # Manual = single curated source
manual_df['lab_sources'] = 'Manual Curation'

# Create provenance tracking columns
def create_hybrid_row(lab_row=None, manual_row=None, strain_name=None):
    """Combine lab and manual data with full provenance tracking"""
    
    if lab_row is not None and manual_row is not None:
        # OVERLAP - Both sources have this strain
        # Use lab terpenes (more accurate), manual THC (more realistic)
        
        return {
            'strain_name': strain_name,
            
            # Cannabinoids - prefer manual (more realistic modern values)
            'thc_percent': manual_row['thc_percent'],
            'cbd_percent': manual_row['cbd_percent'],
            'cbn_percent': manual_row['cbn_percent'],
            'cannabinoid_source': f"Manual ({manual_row['data_source']})",
            
            # Terpenes - prefer lab (measured, not estimated)
            'myrcene': lab_row['myrcene'],
            'limonene': lab_row['limonene'],
            'caryophyllene': lab_row['caryophyllene'],
            'linalool': lab_row['linalool'],
            'pinene': lab_row['pinene'],
            'humulene': lab_row['humulene'],
            'terpinolene': lab_row['terpinolene'],
            'ocimene': lab_row['ocimene'],
            'terpene_source': f"Lab-Verified ({lab_row['sample_count']} samples from {lab_row['lab_sources']})",
            
            # Effects/Uses - prefer manual (better curated)
            'primary_effects': manual_row['primary_effects'],
            'medical_uses': manual_row['medical_uses'],
            'effects_source': f"Manual ({manual_row['data_source']})",
            
            # Strain type - prefer manual (genetics-based)
            'strain_type': manual_row['strain_type'],
            'type_source': f"Manual ({manual_row['data_source']})",
            
            # Tracking
            'data_quality': 'Hybrid - Lab terpenes + Manual metadata',
            'sample_count': lab_row['sample_count'],
            'lab_sources': lab_row['lab_sources'],
            'manual_source': manual_row['data_source']
        }
    
    elif lab_row is not None:
        # LAB ONLY - Use all lab data
        return {
            'strain_name': strain_name,
            
            'thc_percent': lab_row['thc_percent'],
            'cbd_percent': lab_row['cbd_percent'],
            'cbn_percent': lab_row['cbn_percent'],
            'cannabinoid_source': f"Lab-Verified ({lab_row['sample_count']} samples)",
            
            'myrcene': lab_row['myrcene'],
            'limonene': lab_row['limonene'],
            'caryophyllene': lab_row['caryophyllene'],
            'linalool': lab_row['linalool'],
            'pinene': lab_row['pinene'],
            'humulene': lab_row['humulene'],
            'terpinolene': lab_row['terpinolene'],
            'ocimene': lab_row['ocimene'],
            'terpene_source': f"Lab-Verified ({lab_row['sample_count']} samples from {lab_row['lab_sources']})",
            
            'primary_effects': lab_row['primary_effects'],
            'medical_uses': lab_row['medical_uses'],
            'effects_source': f"Auto-generated from terpene profile",
            
            'strain_type': lab_row['strain_type'],
            'type_source': f"Auto-classified from terpene profile",
            
            'data_quality': 'Lab-Only - All data from laboratory testing',
            'sample_count': lab_row['sample_count'],
            'lab_sources': lab_row['lab_sources'],
            'manual_source': 'None'
        }
    
    else:
        # MANUAL ONLY
        return {
            'strain_name': strain_name,
            
            'thc_percent': manual_row['thc_percent'],
            'cbd_percent': manual_row['cbd_percent'],
            'cbn_percent': manual_row['cbn_percent'],
            'cannabinoid_source': f"Manual ({manual_row['data_source']})",
            
            'myrcene': manual_row['myrcene'],
            'limonene': manual_row['limonene'],
            'caryophyllene': manual_row['caryophyllene'],
            'linalool': manual_row['linalool'],
            'pinene': manual_row['pinene'],
            'humulene': manual_row['humulene'],
            'terpinolene': manual_row['terpinolene'],
            'ocimene': manual_row['ocimene'],
            'terpene_source': f"Manual ({manual_row['data_source']})",
            
            'primary_effects': manual_row['primary_effects'],
            'medical_uses': manual_row['medical_uses'],
            'effects_source': f"Manual ({manual_row['data_source']})",
            
            'strain_type': manual_row['strain_type'],
            'type_source': f"Manual ({manual_row['data_source']})",
            
            'data_quality': 'Manual-Only - Curated from research sources',
            'sample_count': 1,
            'lab_sources': 'None',
            'manual_source': manual_row['data_source']
        }

# Get all unique strain names from both sources
all_strains = set(lab_df['strain_name'].str.lower()) | set(manual_df['strain_name'].str.lower())

print(f"\n{len(all_strains)} total unique strains across both sources")

# Create hybrid rows
hybrid_rows = []
overlap_count = 0
lab_only_count = 0
manual_only_count = 0

for strain in sorted(all_strains):
    # Find in lab data
    lab_match = lab_df[lab_df['strain_name'].str.lower() == strain]
    manual_match = manual_df[manual_df['strain_name'].str.lower() == strain]
    
    lab_row = lab_match.iloc[0] if len(lab_match) > 0 else None
    manual_row = manual_match.iloc[0] if len(manual_match) > 0 else None
    
    # Get proper case name
    if lab_row is not None:
        proper_name = lab_row['strain_name']
    else:
        proper_name = manual_row['strain_name']
    
    # Create hybrid row
    hybrid_row = create_hybrid_row(lab_row, manual_row, proper_name)
    hybrid_rows.append(hybrid_row)
    
    # Track statistics
    if lab_row is not None and manual_row is not None:
        overlap_count += 1
    elif lab_row is not None:
        lab_only_count += 1
    else:
        manual_only_count += 1

# Create final DataFrame
master_df = pd.DataFrame(hybrid_rows)

print("\n" + "="*70)
print("DATA SOURCE BREAKDOWN")
print("="*70)
print(f"Hybrid (both sources):  {overlap_count} strains")
print(f"Lab-only:              {lab_only_count} strains")
print(f"Manual-only:           {manual_only_count} strains")
print(f"TOTAL:                 {len(master_df)} strains")

# Sort by sample count (most validated first), then name
master_df = master_df.sort_values(['sample_count', 'strain_name'], ascending=[False, True])

# Save master database with full provenance
output_path = r'C:\Projects\terpene_profiler_v1.3\strain_database_master.csv'
master_df.to_csv(output_path, index=False)

print(f"\nOK Saved master database to:")
print(f"  {output_path}")

# Also create a simplified version for the app (without all the source columns)
app_df = master_df[[
    'strain_name', 'thc_percent', 'cbd_percent', 'cbn_percent',
    'myrcene', 'limonene', 'caryophyllene', 'linalool', 'pinene',
    'humulene', 'terpinolene', 'ocimene',
    'primary_effects', 'medical_uses', 'strain_type',
    'data_quality', 'sample_count'
]].copy()

# Add simplified data_source column for app display
app_df['data_source'] = master_df.apply(lambda row: 
    f"Hybrid: Lab terpenes ({row['sample_count']} samples) + Manual metadata" 
    if row['data_quality'].startswith('Hybrid') 
    else f"Lab-Verified: {row['sample_count']} samples from {row['lab_sources']}" 
    if row['data_quality'].startswith('Lab') 
    else f"Manual: {row['manual_source']}",
    axis=1
)

app_path = r'C:\Projects\terpene_profiler_v1.3\strain_database_enhanced.csv'
app_df.to_csv(app_path, index=False)

print(f"OK Saved app-ready database to:")
print(f"  {app_path}")

# Show statistics
print("\n" + "="*70)
print("SAMPLE STRAINS (Showing data source strategy)")
print("="*70)

# Show hybrid example
hybrid_examples = master_df[master_df['data_quality'].str.contains('Hybrid')].head(2)
for idx, row in hybrid_examples.iterrows():
    print(f"\n{row['strain_name']} ({row['data_quality']})")
    print(f"  THC: {row['thc_percent']:.1f}% - Source: {row['cannabinoid_source']}")
    print(f"  Terpenes - Source: {row['terpene_source']}")
    print(f"  Effects: {row['primary_effects']} - Source: {row['effects_source']}")
    print(f"  Type: {row['strain_type']} - Source: {row['type_source']}")

# Show lab-only example  
lab_only_examples = master_df[master_df['data_quality'].str.contains('Lab-Only')].head(1)
if len(lab_only_examples) > 0:
    for idx, row in lab_only_examples.iterrows():
        print(f"\n{row['strain_name']} ({row['data_quality']})")
        print(f"  THC: {row['thc_percent']:.1f}% - Source: {row['cannabinoid_source']}")
        print(f"  All data from {row['sample_count']} lab samples")

# Show manual-only example
manual_only_examples = master_df[master_df['data_quality'].str.contains('Manual-Only')].head(1)
if len(manual_only_examples) > 0:
    for idx, row in manual_only_examples.iterrows():
        print(f"\n{row['strain_name']} ({row['data_quality']})")
        print(f"  THC: {row['thc_percent']:.1f}% - Source: {row['cannabinoid_source']}")
        print(f"  All data from manual curation")

print("\n" + "="*70)
print("DATABASE STATISTICS")
print("="*70)
print(f"Total strains: {len(master_df)}")
print(f"Average lab samples (when available): {master_df[master_df['sample_count'] > 1]['sample_count'].mean():.1f}")
print(f"Strains with 100+ lab samples: {len(master_df[master_df['sample_count'] >= 100])}")
print(f"Strains with manual curation: {len(master_df[master_df['manual_source'] != 'None'])}")

print("\n" + "="*70)
print("DONE - Master database created with full provenance tracking!")
print("="*70)
print("\nTwo files created:")
print("1. strain_database_master.csv - Full provenance (all source columns)")
print("2. strain_database_enhanced.csv - App-ready (simplified)")
