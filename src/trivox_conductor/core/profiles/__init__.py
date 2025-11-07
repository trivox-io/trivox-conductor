from pathlib import Path
from .profile_manager import ProfileManager


_PROFILES_PATH = Path(__file__).resolve().parents[2] / "profiles.yml"
profile_manager = ProfileManager.from_yaml(_PROFILES_PATH)
