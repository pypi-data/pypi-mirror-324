import unittest
import os
from ossbomer_schema.validator import SBOMSchemaValidator

class TestSBOMValidation(unittest.TestCase):
    def setUp(self):
        self.validator = SBOMSchemaValidator()
        self.test_dir = os.path.dirname(__file__)  # Get the directory of the test file

    def test_valid_spdx_json(self):
        result = self.validator.validate_spdx_json(os.path.join(self.test_dir, "test_sbom.spdx.json"))
        self.assertEqual(result, "Valid")

    def test_invalid_spdx_json(self): # Example invalid test
        # Create a broken SBOM or modify a test one for this example
        pass

    def test_valid_spdx_xml(self):
        result = self.validator.validate_spdx_xml(os.path.join(self.test_dir, "test_sbom.spdx.xml"))
        self.assertEqual(result, "Valid")

    def test_valid_cyclonedx_json(self):
        result = self.validator.validate_cyclonedx_json(os.path.join(self.test_dir, "test_sbom.cyclonedx.1.4.json"))
        self.assertEqual(result, "Valid")

    def test_valid_cyclonedx_xml(self):
        result = self.validator.validate_cyclonedx_xml(os.path.join(self.test_dir, "test_sbom.cyclonedx.1.4.xml"))
        self.assertEqual(result, "Valid")

    # Add more test cases for invalid SBOMs and edge cases

if __name__ == "__main__":
    unittest.main()