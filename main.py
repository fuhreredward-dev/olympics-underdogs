"""
Olympic Underdogs Watchlist - Main Application
Generates daily watchlists of underdog nations competing in Winter Olympics 2026.
"""

import argparse
from datetime import datetime
from pathlib import Path

from src.data_loader import DataLoader
from src.underdog_checker import UnderdogChecker
from src.medals_per_capita import MedalsPerCapitaCalculator
from src.watchlist_generator import WatchlistGenerator
from src.utils import load_config, format_date


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description='Generate Olympic Underdogs Watchlist'
    )
    parser.add_argument(
        '--date',
        type=str,
        help='Date to generate watchlist for (YYYY-MM-DD). Defaults to today.'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Generate watchlists for all dates in the Olympics'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    print("Loading configuration...")
    config = load_config(args.config)
    
    # Initialize components
    print("Initializing data loader...")
    data_loader = DataLoader(config)
    data_loader.load_all()
    
    underdog_checker = UnderdogChecker(data_loader, config)
    medals_calculator = MedalsPerCapitaCalculator(data_loader)
    watchlist_generator = WatchlistGenerator(
        data_loader, underdog_checker, medals_calculator, config
    )
    
    # Generate watchlist(s)
    if args.all:
        print("\nGenerating watchlists for all Olympic dates...")
        generated_files = watchlist_generator.generate_all_dates()
        print(f"\n✓ Generated {len(generated_files)} watchlists")
        print(f"  from {generated_files[0]} to {generated_files[-1]}")
    else:
        # Determine target date
        if args.date:
            target_date = args.date
        else:
            target_date = format_date(datetime.now())
        
        print(f"\nGenerating watchlist for {target_date}...")
        content = watchlist_generator.generate_for_date(target_date)
        
        # Save to file
        watchlist_generator.save_watchlist(target_date, content)
        
        # Also print to console
        print("\n" + "="*60)
        print(content)
        print("="*60)
    
    print("\n✓ Done!")


if __name__ == '__main__':
    main()
