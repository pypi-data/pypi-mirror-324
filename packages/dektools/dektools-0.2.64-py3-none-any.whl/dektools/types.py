from collections import OrderedDict
from .str import to_var_format


class TypeBase:
    _typed_cls_suffix = None
    _typed_name = None

    def __init__(self, manager):
        self.manager = manager

    @classmethod
    def get_typed_name(cls):
        if cls._typed_name:
            return cls._typed_name
        return cls.__name__[:-len(cls._typed_cls_suffix)]

    @classmethod
    def on_typed_registered(cls, types):
        pass


class TypesBase:
    label_mode = False

    def __init__(self):
        self._maps = OrderedDict()

    def __getitem__(self, item):
        try:
            return self._maps[item]
        except KeyError as e:
            if self.label_mode:
                return self._maps[self.to_label(item)]
            raise e from None

    def keys(self):
        return self._maps.keys()

    def items(self):
        return self._maps.items()

    def get(self, typed):
        ret = self._maps.get(typed)
        if ret is None and self.label_mode:
            return self._maps.get(self.to_label(typed))
        return ret

    def register(self, cls):
        self._maps[cls.get_typed_name()] = cls
        cls.on_typed_registered(self)
        return cls

    @staticmethod
    def to_label(s):
        return '-'.join(to_var_format(s))


class ManagerBase:
    types: TypesBase = None
