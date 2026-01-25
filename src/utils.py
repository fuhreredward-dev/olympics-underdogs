"""
Utility functions for the Olympic Underdogs Watchlist.
"""

from datetime import datetime
from typing import Dict, List
import yaml


def load_config(config_path: str = "config.yaml") -> Dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def parse_date(date_str: str) -> datetime:
    """Parse date string to datetime object."""
    return datetime.strptime(date_str, "%Y-%m-%d")


def format_date(date_obj: datetime) -> str:
    """Format datetime object to string."""
    return date_obj.strftime("%Y-%m-%d")


def format_date_display(date_obj: datetime) -> str:
    """Format datetime object for display."""
    return date_obj.strftime("%B %d, %Y")


def get_ioc_code_name_map() -> Dict[str, str]:
    """
    Return a mapping of IOC codes to full nation names.
    This is a subset - expand as needed.
    """
    return {
        "USA": "United States",
        "CAN": "Canada",
        "GER": "Germany",
        "FRA": "France",
        "ITA": "Italy",
        "NOR": "Norway",
        "SWE": "Sweden",
        "FIN": "Finland",
        "AUT": "Austria",
        "SUI": "Switzerland",
        "JPN": "Japan",
        "CHN": "China",
        "KOR": "South Korea",
        "GBR": "Great Britain",
        "NED": "Netherlands",
        "RUS": "Russia",
        "CZE": "Czech Republic",
        "POL": "Poland",
        "SVK": "Slovakia",
        "SLO": "Slovenia",
        "CRO": "Croatia",
        "BLR": "Belarus",
        "UKR": "Ukraine",
        "KAZ": "Kazakhstan",
        "AUS": "Australia",
        "NZL": "New Zealand",
        "ESP": "Spain",
        "BEL": "Belgium",
        "LAT": "Latvia",
        "EST": "Estonia",
        "LTU": "Lithuania",
        "BUL": "Bulgaria",
        "ROM": "Romania",
        "HUN": "Hungary",
        # Add smaller/underdog nations
        "LIE": "Liechtenstein",
        "AND": "Andorra",
        "MON": "Monaco",
        "SMR": "San Marino",
        "ISL": "Iceland",
        "LUX": "Luxembourg",
        "MLT": "Malta",
        "CYP": "Cyprus",
        "GEO": "Georgia",
        "ARM": "Armenia",
        "MDA": "Moldova",
        "BIH": "Bosnia and Herzegovina",
        "MKD": "North Macedonia",
        "ALB": "Albania",
        "MNE": "Montenegro",
        "SRB": "Serbia",
        "KOS": "Kosovo",
        "JAM": "Jamaica",
        "MEX": "Mexico",
        "BRA": "Brazil",
        "ARG": "Argentina",
        "CHI": "Chile",
        "IND": "India",
        "PAK": "Pakistan",
        "THA": "Thailand",
        "MAS": "Malaysia",
        "SGP": "Singapore",
        "HKG": "Hong Kong",
        "TPE": "Chinese Taipei",
        "PHI": "Philippines",
        "IRI": "Iran",
        "ISR": "Israel",
        "TUR": "Turkey",
        "EGY": "Egypt",
        "MAR": "Morocco",
        "RSA": "South Africa",
        "KEN": "Kenya",
        "NGR": "Nigeria",
        "GHA": "Ghana",
        "TUN": "Tunisia",
        "ALG": "Algeria",
    }


def format_population(population: int) -> str:
    """Format population for display."""
    if population >= 1_000_000:
        return f"{population / 1_000_000:.2f}M"
    elif population >= 1_000:
        return f"{population / 1_000:.1f}K"
    else:
        return str(population)


def calculate_per_capita(medals: int, population: int) -> float:
    """Calculate medals per capita (per 1 million people)."""
    if population == 0:
        return 0.0
    return (medals / population) * 1_000_000
