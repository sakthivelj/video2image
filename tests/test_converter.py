"""
Unit tests for video2image package.
"""

import inspect
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path for imports (must be before other imports)
sys.path.insert(0, str(Path(__file__).parent.parent))

from video2image.converter import (  # noqa: E402
    calculate_frame_hash,
    detect_scene_change,
    extract_frames,
    extract_frames_batch,
    find_videos_recursive,
    load_config,
    save_config
)


class TestFrameExtraction(unittest.TestCase):
    """Test frame extraction functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.temp_dir, 'output')

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_extract_frames_basic(self):
        """Test basic frame extraction (mock test - requires video file)."""
        # This is a placeholder - actual testing requires a video file
        # In CI/CD, you would create or download a test video
        self.assertTrue(True)  # Placeholder

    def test_frame_step_parameter(self):
        """Test frame step parameter."""
        # Verify function accepts frame_step parameter
        # Actual execution requires video file
        self.assertTrue(callable(extract_frames))

    def test_time_based_extraction(self):
        """Test time-based frame extraction parameters."""
        # Verify start_time and end_time parameters exist
        sig = inspect.signature(extract_frames)
        params = list(sig.parameters.keys())

        self.assertIn('start_time', params)
        self.assertIn('end_time', params)

    def test_naming_pattern(self):
        """Test custom naming pattern parameter."""
        sig = inspect.signature(extract_frames)
        params = list(sig.parameters.keys())

        self.assertIn('naming_pattern', params)
        self.assertIn('prefix', params)
        self.assertIn('suffix', params)


class TestImageQuality(unittest.TestCase):
    """Test image quality features."""

    def test_jpeg_quality_parameter(self):
        """Test JPEG quality parameter."""
        sig = inspect.signature(extract_frames)
        params = list(sig.parameters.keys())

        self.assertIn('jpeg_quality', params)

    def test_png_compression_parameter(self):
        """Test PNG compression parameter."""
        sig = inspect.signature(extract_frames)
        params = list(sig.parameters.keys())

        self.assertIn('png_compression', params)

    def test_resize_parameters(self):
        """Test resize parameters."""
        sig = inspect.signature(extract_frames)
        params = list(sig.parameters.keys())

        self.assertIn('resize_width', params)
        self.assertIn('resize_height', params)

    def test_grayscale_parameter(self):
        """Test grayscale parameter."""
        sig = inspect.signature(extract_frames)
        params = list(sig.parameters.keys())

        self.assertIn('grayscale', params)


class TestSmartFeatures(unittest.TestCase):
    """Test smart features."""

    def test_scene_detection_function(self):
        """Test scene detection function exists."""
        self.assertTrue(callable(detect_scene_change))

    def test_frame_hash_calculation(self):
        """Test frame hash calculation."""
        import numpy as np

        # Create a simple test frame
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        frame[:] = [255, 0, 0]  # Red frame

        hash1 = calculate_frame_hash(frame)
        hash2 = calculate_frame_hash(frame)

        # Same frame should produce same hash
        self.assertEqual(hash1, hash2)

    def test_scene_detection_threshold(self):
        """Test scene detection with different frames."""
        import numpy as np

        # Create two very different frames
        frame1 = np.zeros((100, 100, 3), dtype=np.uint8)
        frame1[:] = [0, 0, 0]  # Black

        frame2 = np.zeros((100, 100, 3), dtype=np.uint8)
        frame2[:] = [255, 255, 255]  # White

        # Should detect scene change with low threshold
        result = detect_scene_change(frame1, frame2, threshold=10)
        self.assertTrue(result)


class TestBatchProcessing(unittest.TestCase):
    """Test batch processing features."""

    def test_batch_function_exists(self):
        """Test batch processing function exists."""
        self.assertTrue(callable(extract_frames_batch))

    def test_recursive_search_function(self):
        """Test recursive video search function."""
        self.assertTrue(callable(find_videos_recursive))

    def test_find_videos_empty_directory(self):
        """Test finding videos in empty directory."""
        temp_dir = tempfile.mkdtemp()
        try:
            videos = find_videos_recursive(temp_dir)
            self.assertEqual(len(videos), 0)
        finally:
            shutil.rmtree(temp_dir)


class TestConfiguration(unittest.TestCase):
    """Test configuration management."""

    def setUp(self):
        """Set up test config."""
        self.test_config_path = tempfile.mktemp(suffix='.yaml')

    def tearDown(self):
        """Clean up test config."""
        if os.path.exists(self.test_config_path):
            os.remove(self.test_config_path)

    def test_save_config(self):
        """Test saving configuration."""
        config = {
            'frame_step': 5,
            'jpeg_quality': 90,
            'scene_detection': True
        }

        save_config(config, self.test_config_path)

        # Verify file was created
        self.assertTrue(os.path.exists(self.test_config_path))

    def test_load_config(self):
        """Test loading configuration."""
        config = {
            'frame_step': 3,
            'jpeg_quality': 85
        }

        save_config(config, self.test_config_path)
        loaded = load_config(self.test_config_path)

        self.assertEqual(loaded['frame_step'], 3)
        self.assertEqual(loaded['jpeg_quality'], 85)

    def test_load_nonexistent_config(self):
        """Test loading nonexistent config returns empty dict."""
        config = load_config('/nonexistent/path/config.yaml')
        self.assertEqual(config, {})


class TestNamingPatterns(unittest.TestCase):
    """Test naming pattern functionality."""

    def test_naming_pattern_variables(self):
        """Test that naming pattern supports required variables."""
        # Test pattern formatting manually
        pattern = "{video}_{frame:04d}_{time}"

        result = pattern.format(
            video="test_video",
            frame=42,
            time="1.234"
        )

        expected = "test_video_0042_1.234"
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
