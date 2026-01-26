"""
JSON cleanup script for Olympic Underdogs project
- Identifies redundant files
- Minifies JSON where appropriate
- Reports file sizes before and after
"""
import json
import os
from pathlib import Path

def get_file_size_kb(filepath):
    """Get file size in KB"""
    return os.path.getsize(filepath) / 1024

def minify_json(input_path, output_path=None):
    """Minify a JSON file by removing whitespace"""
    if output_path is None:
        output_path = input_path
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'), ensure_ascii=False)
    
    return data

def prettify_json(input_path, output_path=None, indent=2):
    """Prettify a JSON file with consistent formatting"""
    if output_path is None:
        output_path = input_path
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    
    return data

def analyze_json_files():
    """Analyze all JSON files in the data directory"""
    data_dir = Path('data')
    
    print("=" * 80)
    print("JSON FILES ANALYSIS")
    print("=" * 80)
    
    json_files = sorted(data_dir.glob('*.json'), key=lambda x: x.stat().st_size, reverse=True)
    
    total_size = 0
    files_info = []
    
    for json_file in json_files:
        size_kb = get_file_size_kb(json_file)
        total_size += size_kb
        
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read()
            data = json.loads(content)
        
        # Calculate potential savings
        minified = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        minified_size_kb = len(minified.encode('utf-8')) / 1024
        savings = size_kb - minified_size_kb
        savings_pct = (savings / size_kb * 100) if size_kb > 0 else 0
        
        files_info.append({
            'name': json_file.name,
            'size': size_kb,
            'minified_size': minified_size_kb,
            'savings': savings,
            'savings_pct': savings_pct
        })
    
    print(f"\n{'File':<50} {'Current':<12} {'Minified':<12} {'Savings':<12} {'%':<8}")
    print("-" * 94)
    
    for info in files_info:
        print(f"{info['name']:<50} {info['size']:>8.2f} KB  {info['minified_size']:>8.2f} KB  "
              f"{info['savings']:>8.2f} KB  {info['savings_pct']:>6.1f}%")
    
    print("-" * 94)
    print(f"{'TOTAL':<50} {total_size:>8.2f} KB")
    
    # Check for redundant files
    print("\n" + "=" * 80)
    print("REDUNDANCY CHECK")
    print("=" * 80)
    
    if (data_dir / 'nation_sports_participation_2026.json').exists() and \
       (data_dir / 'nation_sports_participation_2026_complete.json').exists():
        print("\n⚠️  Found redundant files:")
        print("   - nation_sports_participation_2026.json (85 nations)")
        print("   - nation_sports_participation_2026_complete.json (88 nations)")
        print("   Recommendation: Use _complete version, delete the other")
    
    return files_info

def clean_json_files(minify_large_files=True, threshold_kb=50):
    """Clean up JSON files"""
    print("\n" + "=" * 80)
    print("CLEANING JSON FILES")
    print("=" * 80)
    
    data_dir = Path('data')
    json_files = list(data_dir.glob('*.json'))
    
    cleaned = []
    
    for json_file in json_files:
        size_kb = get_file_size_kb(json_file)
        
        # Minify large files
        if minify_large_files and size_kb > threshold_kb:
            print(f"\n✓ Minifying {json_file.name} ({size_kb:.2f} KB)...")
            minify_json(json_file)
            new_size = get_file_size_kb(json_file)
            saved = size_kb - new_size
            print(f"  → {new_size:.2f} KB (saved {saved:.2f} KB, {saved/size_kb*100:.1f}%)")
            cleaned.append(json_file.name)
    
    print(f"\n✓ Cleaned {len(cleaned)} files")
    return cleaned

if __name__ == '__main__':
    # Analyze files
    analyze_json_files()
    
    # Ask user if they want to clean
    print("\n" + "=" * 80)
    response = input("\nClean JSON files? (minify files > 50KB) [y/N]: ").strip().lower()
    
    if response == 'y':
        clean_json_files()
        print("\n✅ Cleanup complete!")
    else:
        print("\n❌ Cleanup cancelled")
