"""Command to validate a Python package."""
from pathlib import Path
from typing import List, Type

from ..core.validator import Validator
from ..validators.pyproject_validator import PyProjectValidator
from ..validators.readme_validator import ReadmeValidator


def get_validators() -> List[Type[Validator]]:
    """Get list of all available validators."""
    return [
        PyProjectValidator,
        ReadmeValidator,
        # Add more validators here
    ]


def validate(project_path: str = ".") -> bool:
    """Run all validators on the project.
    
    Args:
        project_path: Path to the project directory
        
    Returns:
        bool: True if all validations pass, False otherwise
    """
    path = Path(project_path).resolve()
    validators = get_validators()
    all_passed = True
    
    print(f"\nValidating project: {path}\n")
    
    for validator_cls in validators:
        validator = validator_cls(path)
        result = validator.validate()
        
        print(f"Running {validator.name}...")
        if result.passed:
            print("✓ Passed")
        else:
            all_passed = False
            print("✗ Failed")
            for msg in result.messages:
                print(f"  - {msg}")
        print()
    
    return all_passed


def main():
    """Entry point for the validate command."""
    success = validate()
    if not success:
        exit(1)


if __name__ == "__main__":
    main() 