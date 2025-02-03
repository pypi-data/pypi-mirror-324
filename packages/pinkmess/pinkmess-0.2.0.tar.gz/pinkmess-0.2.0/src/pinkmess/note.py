from __future__ import annotations

from datetime import datetime
from pathlib import Path

import frontmatter
from pydantic import BaseModel, ConfigDict


class Note(BaseModel):
    """
    A representation of a note.
    """

    path: Path
    """Path to the note file."""

    content: str | None = None
    """Content of the note."""

    metadata: frontmatter.Post | None = None
    """Metadata related to the note."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def create_empty(cls, dir_path: Path, file_name_format: str) -> Note:
        """
        Initializes an empty note given a directory.
        """
        now = datetime.now().strftime(file_name_format)
        note_path = dir_path / f"{now}.md"
        note_path.touch()
        return cls(path=note_path)

    @classmethod
    def from_path(cls, path: Path) -> Note:
        """
        Initializes a note from a file path.
        """
        note = cls(path=path)
        note.load()
        return note

    def load(self) -> None:
        """
        Loads the note content and metadata.
        """
        text = self.path.read_text()
        self.content = text
        self.metadata = frontmatter.loads(text)

    def save(self) -> None:
        """
        Saves the note content and metadata.
        """
        if self.metadata is None:
            self.path.write_text(self.content or "")
        else:
            self.path.write_text(frontmatter.dumps(self.metadata))
