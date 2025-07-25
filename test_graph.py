from dataclasses import dataclass
from typing import final, Union, Optional, override


class Q:
    def __getattr__(self, name):
        return f"Virtual attr: {name}"

    @override
    def __dir__(self):
        return ['foo', 'bar']

q = Q()
print(q.foo)

@dataclass
class Node:
    """Базовый класс узла графа"""
    pass


@final
@dataclass
class A(Node):
    def to_parent[T: "A | B"](self, parent: T):
        """A может иметь родителей B или C"""
        return (self, parent)

    def to_child(self, child: Union["B", "C"]):
        """A может иметь детей B или C"""
        if isinstance(child, (B, C)):
            return (self, child)
        return None


@final
@dataclass
class B(Node):
    def to_parent(self, parent: Union["A", "C"]):
        """B может иметь родителей A или C"""
        if isinstance(parent, (A, C)):
            return (self, parent)
        return None

    def to_child(self, child: Union["A", "C"]):
        """B может иметь детей A или C"""
        if isinstance(child, (A, C)):
            return (self, child)
        return None


@final
@dataclass
class C(Node):
    def to_parent(self, parent: Union[A, B]):
        """C может иметь родителей A или B"""
        if isinstance(parent, (A, B)):
            return (self, parent)
        return None

    def to_child(self, child: Union[A, B]):
        """C может иметь детей A или B"""
        if isinstance(child, (A, B)):
            return (self, child)
        return None


# Использование
a = A()
b = B()
c = C()

# Создание связей с проверкой типов:
parent_relation = a.to_parent()  # Optional[tuple[A, Union[B, C]]]
if parent_relation:
    child_node, parent_node = parent_relation  # (A, B)

child_relation = a.to_child(c)    # Optional[tuple[A, Union[B, C]]]
if child_relation:
    parent_node, child_node = child_relation  # (A, C)

# Неправильные связи вернут None:
invalid = a.to_parent(a)  # None - A не может быть родителем A

# IDE знает точные типы в tuple:
# parent_relation[0]  # A
# parent_relation[1]  # Union[B, C]
