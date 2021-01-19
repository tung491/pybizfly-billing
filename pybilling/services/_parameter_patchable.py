from abc import ABC

from ._segregation import Patchable


class ParameterPatchable(Patchable, ABC):
    def update(self, _id: str, *args, **kwargs) -> dict:
        self._add_sub_endpoint(_id)
        return super(ParameterPatchable, self).update(*args, **kwargs)
