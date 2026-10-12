import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "incident-card.schema.json").read_text(encoding="utf-8"))
PROFILE_EXAMPLE = ROOT / "profiles" / "aviation" / "examples" / "aviation-maintenance-synthetic.json"
EXAMPLE = json.loads(PROFILE_EXAMPLE.read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())


class AviationProfileTests(unittest.TestCase):
    def test_schema_is_valid(self):
        Draft202012Validator.check_schema(SCHEMA)

    def test_all_examples_validate(self):
        for path in [*(ROOT / "examples").glob("*.json"), PROFILE_EXAMPLE]:
            with self.subTest(path=path.name):
                document = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual([], list(VALIDATOR.iter_errors(document)))

    def test_invalid_adrep_reference_fails(self):
        document = copy.deepcopy(EXAMPLE)
        document["aviation_profile"]["adrep_category_refs"] = [
            {"code": "lowercase", "mapping_status": "publisher_asserted_unverified"}
        ]
        self.assertNotEqual([], list(VALIDATOR.iter_errors(document)))

    def test_unverified_mapping_status_is_required(self):
        document = copy.deepcopy(EXAMPLE)
        document["aviation_profile"]["adrep_category_refs"] = [{"code": "SCF-NP", "mapping_status": "verified"}]
        self.assertNotEqual([], list(VALIDATOR.iter_errors(document)))

    def test_unknown_aviation_fields_fail(self):
        document = copy.deepcopy(EXAMPLE)
        document["aviation_profile"]["certified_airworthy"] = True
        self.assertNotEqual([], list(VALIDATOR.iter_errors(document)))


if __name__ == "__main__":
    unittest.main()
