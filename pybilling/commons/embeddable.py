from typing import List

from pybilling.utils import ExcludeValueException


class Embeddable:
    def embeddable(self) -> List[str]:
        return []

    def validate_embedded(self, embedded: str):
        embeddable = self.embeddable()
        if embedded not in embeddable:
            raise ExcludeValueException(embedded, embeddable)
