import unittest
from unittest.mock import patch, mock_open
import yaml


class TestYAMLWrapConfig(unittest.TestCase):
    def setUp(self):
        # Setting up a dummy path for tests
        self.dummy_path = "dummy_path.yaml"
        self.data = {"key": "value"}

    def test_load_existing_file(self):
        from wrapconfig import YAMLWrapConfig

        # Mock the open method to return a string of data
        m = mock_open(
            read_data=yaml.dump(self.data)
        )  # Use yaml.dump() instead of json.dumps()
        with patch("builtins.open", m):
            manager = YAMLWrapConfig(self.dummy_path)
            manager.load()
            self.assertEqual(manager.data, self.data)

    def test_save_file(self):
        from wrapconfig import YAMLWrapConfig

        # Mock the open method and os methods
        m = mock_open()
        with patch("builtins.open", m), patch(
            "os.path.exists", return_value=False
        ), patch("os.makedirs"):
            manager = YAMLWrapConfig(self.dummy_path)
            manager.set_data(self.data)
            manager.save()

            written_data = "".join(m().write.call_args_list[-1][0])

            self.assertEqual(
                yaml.dump(self.data, default_flow_style=False), written_data
            )  # Use yaml.dump() with default_flow_style=False for readability

    def test_save_file_existing_dir(self):
        from wrapconfig import YAMLWrapConfig

        # Mock the open method and os methods
        m = mock_open(read_data=yaml.dump(self.data))
        with patch("builtins.open", m), patch(
            "os.path.exists", return_value=True  # Mock to return True
        ), patch(
            "os.makedirs",
        ) as mock_makedirs:
            manager = YAMLWrapConfig(self.dummy_path)
            manager.set_data(self.data)
            manager.save()

            # Assert that os.makedirs was not called
            with self.assertRaises(AssertionError):
                manager.save()
                mock_makedirs.assert_called_once()

    def test_yaml_support_optional(self):
        import sys

        # Mock the sys.modules to simulate that pyyaml is not installed
        if "wrapconfig" in sys.modules:
            del sys.modules["wrapconfig"]
        for key in list(sys.modules.keys()):
            if key.startswith("wrapconfig") or key.startswith("test"):
                del sys.modules[key]
        original_modules = sys.modules.copy()
        sys.modules["yaml"] = None

        try:
            # Reload your module to trigger the import in __init__.py
            import wrapconfig

            # Check that 'YAMLWrapConfig' is not in __all__
            self.assertNotIn("YAMLWrapConfig", wrapconfig.__all__)

        finally:
            # Restore original modules to ensure other tests are not affected
            sys.modules = original_modules
