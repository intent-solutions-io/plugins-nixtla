"""
Analyze codebase for TimeGPT-1 API usage patterns.

Usage:
    python analyze_codebase.py [base_directory]
"""
import os
import glob
import re
from typing import List, Tuple


def analyze_codebase(base_dir: str) -> List[Tuple[str, str]]:
    """
    Analyzes the codebase for TimeGPT-1 API usage patterns.

    Args:
        base_dir: The base directory of the codebase.

    Returns:
        A list of tuples, where each tuple contains the file path and the matched code snippet.
    """
    patterns = [
        r"timegpt\.forecast\(",
        r"timegpt\.create_model\(",
        r"timegpt\.load_data\(",
        r"timegpt\.train\("
    ]
    results: List[Tuple[str, str]] = []

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith((".py", ".ipynb")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        for pattern in patterns:
                            matches = re.findall(pattern, content)
                            for match in matches:
                                results.append((file_path, match))
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

    return results


def generate_analysis_report(analysis_results: List[Tuple[str, str]], output_file: str = "analysis_report.txt") -> None:
    """
    Generates a report summarizing the codebase analysis.

    Args:
        analysis_results: A list of tuples containing file paths and matched code snippets.
        output_file: The path to the output report file.
    """
    with open(output_file, "w") as f:
        f.write("Codebase Analysis Report\n")
        f.write("-------------------------\n\n")
        if not analysis_results:
            f.write("No TimeGPT-1 API usage found.\n")
        else:
            for file_path, match in analysis_results:
                f.write(f"File: {file_path}\n")
                f.write(f"Match: {match}\n")
                f.write("-------------------------\n")
            f.write(f"Found {len(analysis_results)} instances of TimeGPT-1 API usage.\n")


if __name__ == "__main__":
    import sys

    base_directory = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"Analyzing codebase in: {base_directory}")

    analysis_results = analyze_codebase(base_directory)
    generate_analysis_report(analysis_results)

    print(f"Codebase analysis complete. See analysis_report.txt for details.")
    print(f"Found {len(analysis_results)} instances of TimeGPT-1 API usage.")
