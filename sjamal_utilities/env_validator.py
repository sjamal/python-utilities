"""Environment variable validation utilities."""

from typing import List, Optional


class EnvValidator:
    """Validate that required environment variables are set and non-empty."""

    @staticmethod
    def check(required_vars: List[str], strict: bool = True) -> dict:
        """
        Check if required environment variables are set.

        Args:
            required_vars: List of environment variable names to check.
            strict: If True, raise ValueError if any are missing. If False, return a report.

        Returns:
            dict with keys 'missing', 'empty', 'valid'. All are lists of var names.

        Raises:
            ValueError: If strict=True and any required vars are missing or empty.
        """
        import os

        result = {"missing": [], "empty": [], "valid": []}

        for var in required_vars:
            if var not in os.environ:
                result["missing"].append(var)
            elif not os.environ[var].strip():
                result["empty"].append(var)
            else:
                result["valid"].append(var)

        if strict and (result["missing"] or result["empty"]):
            failed = result["missing"] + result["empty"]
            raise ValueError(
                f"Missing or empty environment variables: {', '.join(failed)}"
            )

        return result

    @staticmethod
    def print_report(required_vars: List[str]) -> bool:
        """
        Print a readable report of environment variable status.

        Args:
            required_vars: List of environment variable names to check.

        Returns:
            True if all are valid, False otherwise.
        """
        result = EnvValidator.check(required_vars, strict=False)
        all_valid = len(result["valid"]) == len(required_vars)

        if all_valid:
            print(f"✓ All {len(required_vars)} required environment variables are set.")
        else:
            if result["missing"]:
                print(f"✗ Missing: {', '.join(result['missing'])}")
            if result["empty"]:
                print(f"✗ Empty: {', '.join(result['empty'])}")

        return all_valid
