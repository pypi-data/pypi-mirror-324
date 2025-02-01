
from typing import List
from pydantic import BaseModel, Field, field_validator
from cpelib.utils.common import REFERENCE_TAGS


class Reference(BaseModel):
    href: str
    text: str
    tags: List[str] = Field(default_factory=list)

    @staticmethod
    def _extract_tags_from_text(text: str) -> List[str]:
        # TODO: it should also include the reference link, as it can provide more context
        if not text:
            return []

        # TODO: cleaning should be done in a standard way
        clean_text = (text.strip().replace("-", " ").replace("/", " ")
                      .replace("_", " "))
        clean_text = "".join(char for char in clean_text if not char.isdigit())

        terms = set(clean_text.lower().split())
        tags = []

        for tag, keywords in REFERENCE_TAGS.items():
            if tag in tags:
                continue
            if terms.intersection(keywords):
                tags.append(tag)

        return tags

    def model_post_init(self, __context):
        """
        Automatically extract tags from `text` after initialization.
        This runs after the model's fields have been initialized.
        """
        if not self.tags:  # Only populate tags if they were not manually provided
            self.tags = self._extract_tags_from_text(self.text)
