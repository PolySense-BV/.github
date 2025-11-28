"""
Image storage interface and implementations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from .models import ImageMetadata


class BaseImageStorage(ABC):
    """Base class for image storage backends."""

    @abstractmethod
    def get_images(
        self,
        start_time: datetime,
        end_time: datetime,
        production_line_id: Optional[str] = None,
    ) -> List[ImageMetadata]:
        """
        Retrieve images within a time range.

        Args:
            start_time: Start of time range
            end_time: End of time range
            production_line_id: Optional filter by production line

        Returns:
            List of image metadata
        """
        pass


class MockImageStorage(BaseImageStorage):
    """Mock image storage for testing."""

    def __init__(self):
        """Initialize mock storage with sample data."""
        self.mock_images: List[ImageMetadata] = []

    def get_images(
        self,
        start_time: datetime,
        end_time: datetime,
        production_line_id: Optional[str] = None,
    ) -> List[ImageMetadata]:
        """Return mock images within time range."""
        filtered = [
            img
            for img in self.mock_images
            if start_time <= img.timestamp <= end_time
            and (
                production_line_id is None
                or img.production_line_id == production_line_id
            )
        ]
        return filtered

    def add_mock_image(self, image: ImageMetadata):
        """Add a mock image for testing."""
        self.mock_images.append(image)


class FileSystemImageStorage(BaseImageStorage):
    """File system based image storage."""

    def __init__(self, base_path: str):
        """
        Initialize file system storage.

        Args:
            base_path: Base directory path for images
        """
        import os
        self.base_path = base_path
        if not os.path.exists(base_path):
            os.makedirs(base_path, exist_ok=True)

    def get_images(
        self,
        start_time: datetime,
        end_time: datetime,
        production_line_id: Optional[str] = None,
    ) -> List[ImageMetadata]:
        """Retrieve images from file system."""
        import os
        from pathlib import Path

        images = []
        base = Path(self.base_path)

        # Search for images in subdirectories
        for image_file in base.rglob("*.jpg"):
            # Try to extract timestamp from filename or path
            # This is a simplified implementation
            # In production, you'd have a proper index/metadata database
            try:
                # Assume filename contains timestamp
                timestamp_str = image_file.stem
                timestamp = datetime.fromisoformat(timestamp_str)
            except:
                # Use file modification time as fallback
                timestamp = datetime.fromtimestamp(
                    image_file.stat().st_mtime
                )

            if start_time <= timestamp <= end_time:
                line_id = image_file.parent.name
                if production_line_id is None or line_id == production_line_id:
                    images.append(
                        ImageMetadata(
                            timestamp=timestamp,
                            production_line_id=line_id,
                            image_path=str(image_file),
                        )
                    )

        return images
