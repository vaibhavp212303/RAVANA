import re
import json


class TestCaseParser:
    @staticmethod
    def extract(text: str):
        split_pattern = r"(?=\*\*?Test Case(?:\s+\d+|:))"
        chunks = re.split(split_pattern, text, flags=re.IGNORECASE)
        cases = []

        for chunk in chunks:
            chunk = chunk.strip()
            if not chunk.lower().startswith("**test case"):
                continue

            def section(title, multiline=True):
                pattern = rf"\*\*{title}:?\*\*(.*?)(?=\n\*\*|\Z)"
                match = re.search(pattern, chunk, re.DOTALL | re.IGNORECASE)
                if not match:
                    return [] if multiline else None
                content = match.group(1).strip()
                return [line.strip("-*+•\t ").strip() for line in content.split("\n") if line.strip()] \
                    if multiline else content

            case_data = {
                "test_case": section("Test Case", multiline=False),
                "objective": section("Objective", multiline=False),
                "test_steps": section("Test Steps"),
                "expected_results": section("Expected Results")
            }
            cases.append({k: v for k, v in case_data.items() if v})
        return cases or [{"raw_output": text}]

    @staticmethod
    def parse_json_or_text(output_text):
        try:
            structured_cases = json.loads(output_text)
            return structured_cases if isinstance(structured_cases, list) else [structured_cases]
        except json.JSONDecodeError:
            return TestCaseParser.extract(output_text)
