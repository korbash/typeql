import re
from typing import Any, Dict, List, Union

from lark import Lark, Token, Transformer
from pydantic import BaseModel, ConfigDict, Field


class UnionValue(BaseModel):
    """Represents a union type value with pipe separator."""

    model_config = ConfigDict(frozen=True)

    values: List[List[str]] = Field(
        description="List of union type options as dotted names"
    )


class PropertyResult(BaseModel):
    """Result of parsing a single property with its arguments."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    positional: List[Union[List[str], UnionValue]] = Field(
        default_factory=list, description="Positional arguments in order"
    )
    named: Dict[str, Union[List[str], UnionValue]] = Field(
        default_factory=dict, description="Named arguments as key-value pairs"
    )


# Enhanced Lark grammar with positional args first, then named args
property_grammar = r"""
start: property

property: noarg_property
    | arg_property

noarg_property: "@" NAME

arg_property: "@" NAME "(" _WS* args? _WS* ")"

args: arg (_WS* "," _WS* arg)*

arg: positional_arg | named_arg

positional_arg: value
named_arg: NAME _WS* "=" _WS* value

value: union_value | dotted_name

union_value: dotted_name (_WS* "|" _WS* dotted_name)+

dotted_name: NAME ("." NAME)*

NAME: /[a-z_][a-z0-9_]*/  // Only lowercase

_WS: /[ \t\n\r]+/
"""


class PropertyTransformer(Transformer):
    def NAME(self, t: Token) -> str:
        return t.value.lower()  # Ensure lowercase

    def dotted_name(self, parts):
        # Handle dotted names like "a.b.c" - validate and return as list
        dotted_parts = []
        for part in parts:
            part_str = str(part).lower()
            if not re.match(r"^[a-z_][a-z0-9_]*$", part_str):
                raise ValueError(f"Invalid identifier in dotted name: '{part_str}'")
            dotted_parts.append(part_str)
        return dotted_parts

    def union_value(self, values):
        # Keep dotted names as List[str] for union values
        return UnionValue(values=values)

    def positional_arg(self, items):
        return items[0]

    def named_arg(self, items):
        name = items[0]
        value = items[1]
        return {"type": "named", "name": name, "value": value}

    def named_args(self, items):
        return items

    def arg(self, items):
        return items[0]

    def args(self, items):
        return items

    def arg_property(self, items):
        name = items[0]
        args = items[1] if len(items) > 1 else []
        return {"name": name, "args": args}

    def noarg_property(self, items):
        return {"name": items[0], "args": []}

    def property(self, items):
        return items[0]

    def start(self, items):
        return items[0]


# Enhanced regex for finding @properties in text
PROPERTY_RE = re.compile(
    r"(?P<full>@(?P<name>[a-z_][a-z0-9_]*)(?:\((?P<body>[^)]*(?:\([^)]*\)[^)]*)*)\))?)",
    flags=re.DOTALL | re.IGNORECASE,
)


def parse_properties_from_text(text: str) -> Dict[str, PropertyResult]:
    """
    Parse text for @property annotations and return structured data.

    Supports:
    - @ignore (no args)
    - @alias(new_name) (positional args first)
    - @link(a|b|c, nullable=true) (positional args, then named args)

    Args:
        text: Text containing @property annotations (will be converted to lowercase)

    Returns:
        Dict with property names as keys, PropertyResult as values
    """
    # Convert entire text to lowercase for parsing
    text_lower = text.lower()

    parser = Lark(property_grammar, parser="earley")
    transformer = PropertyTransformer()

    properties = {}

    for match in PROPERTY_RE.finditer(text_lower):
        try:
            tree = parser.parse(match.group("full"))
            property_data = transformer.transform(tree)

            property_name = property_data["name"]

            if property_name in properties:
                raise ValueError(f"Duplicate property: {property_name}")

            # Convert args to PropertyResult format
            processed_args = _process_args(property_data["args"])
            properties[property_name] = processed_args

        except Exception as e:
            # Log error but continue parsing other properties
            print(f"Failed to parse property {match.group('full')}: {e}")

    return properties


def _extract_simple_value(value) -> Union[List[str], UnionValue]:
    """
    Extract simple value from Lark Tree structure and convert to proper types.
    """
    from lark import Tree

    if isinstance(value, Tree):
        # If it's a Tree, extract the first child
        if value.children:
            return _extract_simple_value(value.children[0])
        # Return empty list for empty Tree instead of None
        return []
    else:
        # Simple value (already processed by transformer)
        return value


def _process_args(args: list[dict]) -> PropertyResult:
    """
    Convert parsed args to convenient PropertyResult format.
    Now allows mixed positional and named arguments.
    """
    result = PropertyResult(positional=[], named={})

    for arg in args:
        if isinstance(arg, dict) and arg.get("type") == "named":
            result.named[arg["name"]] = _extract_simple_value(arg["value"])
        else:
            # Positional argument (now just a simple value)
            result.positional.append(_extract_simple_value(arg))
    return result


# Legacy function for backward compatibility
def parse_properties(text: str) -> Dict[str, PropertyResult]:
    """
    Legacy API - returns simple args list.

    Args:
        text: Text to parse (will be converted to lowercase)

    Returns:
        Dict with property names as keys, PropertyResult as values
    """
    return parse_properties_from_text(text)
