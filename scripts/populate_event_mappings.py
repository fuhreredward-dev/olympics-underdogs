#!/usr/bin/env python3
"""
Helper script to populate event underdog mappings.
Run this after manually identifying which underdogs compete in which events.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.event_underdog_mapper import EventUnderdogMapper


def main():
    """
    Populate event underdog mappings.
    
    Modify this script to add your manual mappings for each sport.
    Run: python scripts/populate_event_mappings.py
    """
    
    mapper = EventUnderdogMapper(data_dir="data")
    mapper.load_underdog_nations()
    mapper.load_schedule()
    
    print("=" * 80)
    print("POPULATING EVENT UNDERDOG MAPPINGS")
    print("=" * 80)
    print(f"\nTotal underdog nations loaded: {len(mapper.underdog_nations)}")
    print(f"Underdog nations: {', '.join(sorted(mapper.underdog_nations))}")
    print("\n" + "=" * 80)
    
    # ========================================================================
    # SKELETON - Add your mappings here
    # ========================================================================
    print("\nAdding Skeleton mappings...")
    
    # Men's Skeleton - Heat 1 (Feb 12)
    mapper.add_event_mapping(
        discipline="Skeleton",
        event="Men's Skeleton",
        date="2026-02-12",
        underdog_nations=["DEN", "ISR"],  # Denmark, Israel
        stage="Heat 1"
    )
    
    # Men's Skeleton - Heat 2 (Feb 12)
    mapper.add_event_mapping(
        discipline="Skeleton",
        event="Men's Skeleton",
        date="2026-02-12",
        underdog_nations=["DEN", "ISR"],
        stage="Heat 2"
    )
    
    # Men's Skeleton - Heat 3 Final (Feb 13)
    mapper.add_event_mapping(
        discipline="Skeleton",
        event="Men's Skeleton",
        date="2026-02-13",
        underdog_nations=["DEN", "ISR"],
        stage="Heat 3 - Final"
    )
    
    # Men's Skeleton - Heat 4 Final Classification (Feb 13)
    mapper.add_event_mapping(
        discipline="Skeleton",
        event="Men's Skeleton",
        date="2026-02-13",
        underdog_nations=["DEN", "ISR"],
        stage="Heat 4 / Final Classification"
    )
    
    # Women's Skeleton - Heat 1 (Feb 13)
    mapper.add_event_mapping(
        discipline="Skeleton",
        event="Women's Skeleton",
        date="2026-02-13",
        underdog_nations=["BRA", "DEN", "RSA"],  # Brazil, Denmark, South Africa
        stage="Heat 1"
    )
    
    # Women's Skeleton - Heat 2 (Feb 13)
    mapper.add_event_mapping(
        discipline="Skeleton",
        event="Women's Skeleton",
        date="2026-02-13",
        underdog_nations=["BRA", "DEN", "RSA"],
        stage="Heat 2"
    )
    
    # Women's Skeleton - Heat 3 Final (Feb 14)
    mapper.add_event_mapping(
        discipline="Skeleton",
        event="Women's Skeleton",
        date="2026-02-14",
        underdog_nations=["BRA", "DEN", "RSA"],
        stage="Heat 3 - Final"
    )
    
    # Women's Skeleton - Heat 4 Final Classification (Feb 14)
    mapper.add_event_mapping(
        discipline="Skeleton",
        event="Women's Skeleton",
        date="2026-02-14",
        underdog_nations=["BRA", "DEN", "RSA"],
        stage="Heat 4 / Final Classification"
    )
    
    # Mixed Team Skeleton (Feb 15) - If Denmark qualifies team
    mapper.add_event_mapping(
        discipline="Skeleton",
        event="Mixed Team Skeleton",
        date="2026-02-15",
        underdog_nations=["DEN"],  # Only if Denmark qualifies a team
        stage="Final"
    )
    
    print(f"✓ Added {len([m for m in mapper.event_mappings.values() if m['discipline'] == 'Skeleton'])} Skeleton event mappings")
    
    # ========================================================================
    # SKI JUMPING - Add your mappings here
    # ========================================================================
    print("\nAdding Ski Jumping mappings...")
    
    # Example: Turkey has 2 male athletes in individual events
    # Add mappings as you identify them
    
    # mapper.add_event_mapping(
    #     discipline="Ski Jumping",
    #     event="Men's Individual Normal Hill",
    #     date="2026-02-08",
    #     underdog_nations=["TUR"],
    #     stage="Qualification"
    # )
    
    # ========================================================================
    # SKI MOUNTAINEERING - Add your mappings here
    # ========================================================================
    print("\nAdding Ski Mountaineering mappings...")
    
    # Example: Australia has 1 male + 1 female in all events
    
    # mapper.add_event_mapping(
    #     discipline="Ski Mountaineering",
    #     event="Men's Individual",
    #     date="2026-02-21",
    #     underdog_nations=["AUS"],
    #     stage="Final"
    # )
    
    # ========================================================================
    # SPEED SKATING - Add your mappings here
    # ========================================================================
    print("\nAdding Speed Skating mappings...")
    
    # Example: Chinese Taipei, Denmark, Estonia, Portugal
    
    # ========================================================================
    # SNOWBOARD - Add your mappings here
    # ========================================================================
    print("\nAdding Snowboard mappings...")
    
    # Example: Australia, Brazil
    
    # ========================================================================
    # Add more sports as you manually map them...
    # ========================================================================
    
    # Save all mappings
    print("\n" + "=" * 80)
    output_file = mapper.save_mappings()
    
    # Show summary
    summary = mapper.get_discipline_summary()
    print("\n" + "=" * 80)
    print("DISCIPLINE SUMMARY")
    print("=" * 80)
    
    for discipline in sorted(summary.keys()):
        info = summary[discipline]
        print(f"\n{discipline}:")
        print(f"  Event instances: {info['event_count']}")
        print(f"  Competition dates: {', '.join(info['dates'])}")
        print(f"  Underdog nations ({len(info['underdogs'])}): {', '.join(info['underdogs'])}")
    
    print("\n" + "=" * 80)
    print(f"✓ Complete! Mappings saved to: {output_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()
