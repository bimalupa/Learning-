#!/usr/bin/env python
"""
Smart Requirements Verification System
Checks if all dependencies are installed before running pip install
Prevents unnecessary re-installations and saves time
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple
import json
from datetime import datetime

class RequirementsVerifier:
    def __init__(self, requirements_file: str = "requirements.txt"):
        self.requirements_file = Path(requirements_file)
        self.cache_file = Path(".requirements_cache.json")
        self.installed_packages = {}
        self.missing_packages = []

    def get_installed_packages(self) -> dict:
        """Get all installed packages and versions"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--format", "json"],
                capture_output=True,
                text=True,
                check=True
            )
            packages = json.loads(result.stdout)
            return {pkg["name"].lower(): pkg["version"] for pkg in packages}
        except Exception as e:
            print(f"❌ Error getting installed packages: {e}")
            return {}

    def parse_requirements(self) -> List[Tuple[str, str]]:
        """Parse requirements.txt file"""
        requirements = []

        if not self.requirements_file.exists():
            print(f"❌ {self.requirements_file} not found!")
            return requirements

        with open(self.requirements_file, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue

                # Parse package and version
                for op in ['>=', '<=', '==', '~=', '>', '<']:
                    if op in line:
                        pkg_name, version = line.split(op, 1)
                        requirements.append((pkg_name.strip(), version.strip()))
                        break
                else:
                    # No version specified
                    requirements.append((line, None))

        return requirements

    def verify_requirements(self) -> bool:
        """Check if all requirements are installed"""
        print("🔍 Verifying requirements...")
        print("-" * 50)

        self.installed_packages = self.get_installed_packages()
        requirements = self.parse_requirements()

        all_satisfied = True

        for pkg_name, required_version in requirements:
            pkg_lower = pkg_name.lower()

            if pkg_lower not in self.installed_packages:
                print(f"❌ Missing: {pkg_name}")
                self.missing_packages.append(pkg_name)
                all_satisfied = False
            else:
                installed_version = self.installed_packages[pkg_lower]
                status = "✅"
                print(f"{status} {pkg_name}: {installed_version}")

        print("-" * 50)

        if all_satisfied:
            print("✅ All requirements are satisfied!")
            self.save_cache()
            return True
        else:
            print(f"\n⚠️  {len(self.missing_packages)} package(s) missing")
            return False

    def save_cache(self):
        """Save verification timestamp and package list"""
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "requirements_file": str(self.requirements_file),
            "packages": self.installed_packages,
            "verified": True
        }

        try:
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
            print(f"✅ Cache saved: {self.cache_file}")
        except Exception as e:
            print(f"⚠️  Could not save cache: {e}")

    def get_last_verification(self) -> dict:
        """Get last verification details"""
        if not self.cache_file.exists():
            return None

        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except Exception:
            return None

    def show_status(self):
        """Show current status"""
        last_check = self.get_last_verification()

        print("\n📊 Requirements Status")
        print("=" * 50)

        if last_check:
            print(f"Last Verified: {last_check['timestamp']}")
            print(f"Total Packages: {len(last_check['packages'])}")
        else:
            print("Never verified yet")

        print("=" * 50)

    def install_missing(self) -> bool:
        """Install only missing packages"""
        if not self.missing_packages:
            print("✅ All packages already installed!")
            return True

        print(f"\n🔧 Installing {len(self.missing_packages)} missing package(s)...")
        print("-" * 50)

        # Install via pip
        try:
            # Use requirements.txt directly but pip will only install missing
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(self.requirements_file)],
                check=True
            )
            print("\n✅ Installation completed!")
            self.save_cache()
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Installation failed: {e}")
            return False


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Verify and manage Python requirements without unnecessary re-installations"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only verify, don't install"
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="Install missing packages"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show verification status"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force full reinstallation"
    )
    parser.add_argument(
        "--requirements",
        default="requirements.txt",
        help="Path to requirements.txt file"
    )

    args = parser.parse_args()

    verifier = RequirementsVerifier(args.requirements)

    # Show status
    verifier.show_status()

    # Handle --status flag
    if args.status:
        return 0

    # Handle --force flag
    if args.force:
        print("\n⚠️  Force reinstalling all packages...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", args.requirements, "--force-reinstall"],
                check=True
            )
            verifier.save_cache()
            print("✅ Force reinstallation completed!")
            return 0
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation failed: {e}")
            return 1

    # Verify requirements
    all_satisfied = verifier.verify_requirements()

    # Install if needed and requested
    if args.install or (not all_satisfied and not args.check):
        if not all_satisfied:
            print("\n🔧 Installing missing packages...")
            success = verifier.install_missing()
            return 0 if success else 1
        else:
            print("✅ All requirements already satisfied!")
            return 0

    return 0 if all_satisfied else 1


if __name__ == "__main__":
    sys.exit(main())
