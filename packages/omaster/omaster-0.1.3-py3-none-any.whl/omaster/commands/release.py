"""Command to release a Python package."""
import subprocess
import shutil
from pathlib import Path
from typing import Optional
import tomli
import tomli_w

from .validate import validate
from ..utils.version import bump_version


def run_command(cmd: str, cwd: Optional[Path] = None) -> bool:
    """Run a shell command."""
    try:
        subprocess.run(cmd.split(), check=True, cwd=cwd)
        return True
    except subprocess.CalledProcessError:
        return False


def clean_dist(project_path: Path) -> bool:
    """Clean up old build files."""
    try:
        dist_path = project_path / "dist"
        if dist_path.exists():
            shutil.rmtree(dist_path)
        dist_path.mkdir(exist_ok=True)
        return True
    except Exception as e:
        print(f"Error cleaning dist directory: {str(e)}")
        return False


def release(project_path: str = ".") -> bool:
    """Release the package.
    
    Steps:
    1. Validate
    2. Bump version
    3. Clean dist
    4. Build
    5. Publish
    
    Args:
        project_path: Path to the project directory
        
    Returns:
        bool: True if release successful, False otherwise
    """
    path = Path(project_path).resolve()
    print(f"\nReleasing project: {path}\n")
    
    # Step 1: Validate
    print("Step 1: Validating project...")
    if not validate(project_path):
        print("✗ Validation failed")
        return False
    print("✓ Validation passed\n")
    
    # Step 2: Bump version
    print("Step 2: Bumping version...")
    if not bump_version(path):
        print("✗ Version bump failed")
        return False
    print("✓ Version bumped\n")
    
    # Step 3: Clean dist
    print("Step 3: Cleaning build files...")
    if not clean_dist(path):
        print("✗ Clean failed")
        return False
    print("✓ Clean successful\n")
    
    # Step 4: Build
    print("Step 4: Building package...")
    if not run_command("uv build", cwd=path):
        print("✗ Build failed")
        return False
    print("✓ Build successful\n")
    
    # Step 5: Publish
    print("Step 5: Publishing package...")
    if not run_command("uv publish", cwd=path):
        print("✗ Publish failed")
        return False
    print("✓ Publish successful\n")
    
    print("Release completed successfully!")
    return True


def main():
    """Entry point for the release command."""
    success = release()
    if not success:
        exit(1)


if __name__ == "__main__":
    main() 