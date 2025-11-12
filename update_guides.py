#!/usr/bin/env python3
"""
Script to update all faction guides with the new "Bonus Game Elements" section.
Replaces "Key Game Elements" with "Bonus Game Elements" in all faction guides.
"""

import os
import re
from pathlib import Path

# Base directory containing all faction guides
BASE_DIR = Path(r"C:\Users\Hampu\Downloads\TI4_Faction_Guides")

# List of all 30 factions
FACTIONS = [
    "Arborec",
    "Argent_Flight",
    "Barony_of_Letnev",
    "Clan_of_Saar",
    "Council_Keleres",
    "Crimson_Rebellion",
    "Deepwrought_Scholarate",
    "Embers_of_Muaat",
    "Emirates_of_Hacan",
    "Empyrean",
    "Federation_of_Sol",
    "Firmament_Obsidian",
    "Ghosts_of_Creuss",
    "L1Z1X_Mindnet",
    "Last_Bastion",
    "Mahact_Gene_Sorcerers",
    "Mentak_Coalition",
    "Naalu_Collective",
    "Naaz-Rokha_Alliance",
    "Nekro_Virus",
    "Nomad",
    "Ral_Nel_Consortium",
    "Sardakk_Norr",
    "Titans_of_Ul",
    "Universities_of_Jol-Nar",
    "Vuilraith_Cabal",
    "Winnu",
    "Xxcha_Kingdom",
    "Yin_Brotherhood",
    "Yssaril_Tribes"
]

# New section content template
NEW_SECTION_TEMPLATE = """## {section_num}. Bonus Game Elements

This section highlights specific action cards, relics, and agendas that have exceptional synergy with your faction abilities or present particular threats/opportunities you should be aware of.

*Action cards that synergize particularly well with your faction's strengths or mitigate your weaknesses.*

*Relics that offer exceptional value for your faction's strategy and abilities.*

*Agendas to pursue that benefit your position, and agendas to watch out for that could hurt you.*

### A. High-Value Action Cards

### B. Relic Priorities

### C. Agenda Awareness"""

def update_faction_guide(faction_name):
    """Update a single faction guide."""
    guide_path = BASE_DIR / faction_name / f"{faction_name}.md"

    if not guide_path.exists():
        print(f"❌ {faction_name}: File not found at {guide_path}")
        return None

    # Read the file
    with open(guide_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the "Key Game Elements" section and extract section number
    pattern = r'^## ([IVXL]+)\. Key Game Elements.*?(?=^## [IVXL]+\.|$)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)

    if not match:
        print(f"⚠️  {faction_name}: 'Key Game Elements' section not found")
        return None

    section_num = match.group(1)

    # Create the new section with the correct section number
    new_section = NEW_SECTION_TEMPLATE.format(section_num=section_num)

    # Replace the old section with the new one
    new_content = re.sub(
        pattern,
        new_section + "\n\n",
        content,
        flags=re.MULTILINE | re.DOTALL
    )

    # Write back to file
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ {faction_name}: Updated section {section_num} (Key Game Elements → Bonus Game Elements)")
    return section_num

def main():
    """Process all faction guides."""
    print("Starting faction guide updates...\n")

    results = {}

    for faction in FACTIONS:
        section_num = update_faction_guide(faction)
        if section_num:
            results[faction] = section_num

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\nSuccessfully updated {len(results)} out of {len(FACTIONS)} guides:\n")

    for faction, section_num in sorted(results.items()):
        print(f"  • {faction:30} → Section {section_num}")

    if len(results) < len(FACTIONS):
        failed = set(FACTIONS) - set(results.keys())
        print(f"\n⚠️  Failed to update {len(failed)} guides:")
        for faction in sorted(failed):
            print(f"  • {faction}")

if __name__ == "__main__":
    main()
