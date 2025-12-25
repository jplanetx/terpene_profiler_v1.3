"""
Extract Minor Cannabinoids from Lab Data
========================================
Extracts CBG, THCV, CBC, CBDV from raw lab results and adds them to strain database.

Priority 1 Enhancement for StrainMatch Pro v2.0
Author: JPXL Labs
"""

import pandas as pd
import numpy as np
from pathlib import Path

# File paths
RAW_DATA = Path(r"C:\Projects\Terpene-Profile-Parser-for-Cannabis-Strains-master\Terpene-Profile-Parser-for-Cannabis-Strains-master\results.csv")
CURRENT_DB = Path(r"C:\Projects\terpene_profiler_v1.3\strain_database_enhanced.csv")
OUTPUT_DB = Path(r"C:\Projects\terpene_profiler_v1.3\strain_database_enhanced_v2.csv")

def load_raw_data():
    """Load the raw lab results"""
    print("[*] Loading raw lab data...")
    df = pd.read_csv(RAW_DATA, low_memory=False)
    print(f"[+] Loaded {len(df):,} test results")
    return df

def extract_cannabinoids_for_strain(raw_df, strain_name):
    """Extract average minor cannabinoid values for a specific strain"""
    # Normalize strain name for matching
    strain_name_clean = strain_name.lower().strip()
    
    # Filter rows for this strain (case-insensitive)
    strain_data = raw_df[raw_df['Sample Name'].str.lower().str.contains(strain_name_clean, na=False)]
    
    if len(strain_data) == 0:
        return {
            'cbg_percent': 0.0,
            'thcv_percent': 0.0,
            'cbc_percent': 0.0,
            'cbdv_percent': 0.0,
            'sample_count': 0
        }
    
    # Extract cannabinoid values (convert to numeric, treating empty as 0)
    cbg_values = pd.to_numeric(strain_data['delta-9 CBG'], errors='coerce').fillna(0)
    thcv_values = pd.to_numeric(strain_data['THCV'], errors='coerce').fillna(0)
    cbc_values = pd.to_numeric(strain_data['CBC'], errors='coerce').fillna(0)
    cbdv_values = pd.to_numeric(strain_data['CBDV'], errors='coerce').fillna(0)
    
    # Calculate averages (only from non-zero values if they exist)
    def safe_average(values):
        non_zero = values[values > 0]
        return non_zero.mean() if len(non_zero) > 0 else 0.0
    
    return {
        'cbg_percent': safe_average(cbg_values),
        'thcv_percent': safe_average(thcv_values),
        'cbc_percent': safe_average(cbc_values),
        'cbdv_percent': safe_average(cbdv_values),
        'sample_count': len(strain_data)
    }

def enhance_database():
    """Main enhancement function"""
    print("\n[*] StrainMatch Pro v2.0 - Minor Cannabinoid Extraction")
    print("=" * 60)
    
    # Load data
    raw_df = load_raw_data()
    current_db = pd.read_csv(CURRENT_DB)
    
    print(f"\n[*] Current database: {len(current_db)} strains")
    
    # Add new columns
    print("\n[*] Extracting minor cannabinoids...")
    
    cannabinoid_data = []
    for idx, row in current_db.iterrows():
        strain_name = row['strain_name']
        print(f"  Processing: {strain_name}...", end=" ")
        
        results = extract_cannabinoids_for_strain(raw_df, strain_name)
        cannabinoid_data.append(results)
        
        # Show what was found
        if results['sample_count'] > 0:
            print(f"[+] ({results['sample_count']} samples)")
        else:
            print("[!] No lab data found")
    
    # Convert to DataFrame and merge
    cannabinoid_df = pd.DataFrame(cannabinoid_data)
    enhanced_db = pd.concat([current_db, cannabinoid_df], axis=1)
    
    # Save enhanced database
    enhanced_db.to_csv(OUTPUT_DB, index=False)
    print(f"\n[+] Enhanced database saved: {OUTPUT_DB}")
    
    # Generate statistics report
    print("\n[*] Enhancement Statistics:")
    print("-" * 60)
    
    for cannabinoid in ['cbg_percent', 'thcv_percent', 'cbc_percent', 'cbdv_percent']:
        non_zero = (enhanced_db[cannabinoid] > 0).sum()
        if non_zero > 0:
            avg_value = enhanced_db[enhanced_db[cannabinoid] > 0][cannabinoid].mean()
            max_value = enhanced_db[cannabinoid].max()
            print(f"{cannabinoid.upper()[:4]}: {non_zero}/{len(enhanced_db)} strains have data")
            print(f"      Avg: {avg_value:.3f}% | Max: {max_value:.3f}%")
        else:
            print(f"{cannabinoid.upper()[:4]}: No data found")
    
    print("\n" + "=" * 60)
    print("[*] Next Step: Update app_v2.py to use the new database")
    print(f"    Change: load_strain_data() -> read '{OUTPUT_DB.name}'")

if __name__ == "__main__":
    enhance_database()
