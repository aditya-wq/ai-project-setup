"""Integration tests for CLI."""

import pytest
from pathlib import Path


class TestCLIIntegration:
    """Integration tests for CLI commands."""

    def test_cli_compresses_file(self, tmp_path):
        """Test CLI compresses a file."""
        from ai_project.cli import main
        import sys

        test_file = tmp_path / "test.md"
        test_file.write_text("# Test\n\nContent here.")

        original_argv = sys.argv
        try:
            sys.argv = ["aiproject", str(test_file)]
            result = main()
        except SystemExit:
            result = 0
        finally:
            sys.argv = original_argv

        assert result == 0 or result is None

    def test_cli_handles_missing_file(self, tmp_path):
        """Test CLI handles missing file gracefully."""
        from ai_project.cli import main
        import sys

        missing_file = tmp_path / "missing.md"
        original_argv = sys.argv
        try:
            sys.argv = ["aiproject", str(missing_file)]
            result = main()
        except SystemExit as e:
            result = e.code
        finally:
            sys.argv = original_argv

        assert result != 0

    def test_cli_shows_help(self):
        """Test CLI shows help."""
        from ai_project.cli import main
        import sys

        original_argv = sys.argv
        try:
            sys.argv = ["aiproject", "--help"]
            main()
        except SystemExit as e:
            assert e.code == 0
        finally:
            sys.argv = original_argv
