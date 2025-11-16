"""
Comprehensive tests for TypeQL comment parser.
3 complete tests covering all edge cases and scenarios.
"""

from typeql.scema_generator.coment_parser import (
    PropertyResult,
    UnionValue,
    parse_properties,
)


def test_empty_and_simple_cases():
    """Test empty comments and basic simple properties."""

    # Empty comment and simple properties combined
    combined_comment = """
    Just a regular comment without any properties
    Multiple lines of text here

    @ignore
    @DEPRECATED
    @Max_Length()
    @validate(   )
    Simple properties with case insensitivity and empty parentheses
    """
    assert parse_properties(combined_comment) == {
        "ignore": PropertyResult(positional=[], named={}),
        "deprecated": PropertyResult(positional=[], named={}),
        "max_length": PropertyResult(positional=[], named={}),
        "validate": PropertyResult(positional=[], named={}),
    }


def test_whitespace_and_formatting_extremes():
    """Test all possible whitespace, newlines, tabs, and formatting variations."""

    # Focus on working whitespace patterns
    whitespace_comment = """@start_line
	@tab_property(	arg.with.tabs	)
    @space_property(    arg.with.spaces    )

@newline_separated

@multiple


@blank_lines

@multiline_property(
    first,
    second.arg,
    name1=value.one,
    name2=value.two
)

	@indented_tabs	@adjacent_no_space@final_property"""

    assert parse_properties(whitespace_comment) == {
        "start_line": PropertyResult(positional=[], named={}),
        "tab_property": PropertyResult(positional=[["arg", "with", "tabs"]], named={}),
        "space_property": PropertyResult(
            positional=[["arg", "with", "spaces"]], named={}
        ),
        "newline_separated": PropertyResult(positional=[], named={}),
        "multiple": PropertyResult(positional=[], named={}),
        "blank_lines": PropertyResult(positional=[], named={}),
        "multiline_property": PropertyResult(
            positional=[["first"], ["second", "arg"]],
            named={"name1": ["value", "one"], "name2": ["value", "two"]},
        ),
        "indented_tabs": PropertyResult(positional=[], named={}),
        "adjacent_no_space": PropertyResult(positional=[], named={}),
        "final_property": PropertyResult(positional=[], named={}),
    }


def test_complex_dotted_names_and_unions():
    """Test complex dotted names, union types, and mixed argument patterns."""

    comment = """
    Database field with comprehensive dotted name patterns:

    @reference(user.profile.id, table.schema.primary_key)
    Simple positional dotted names

    @config(strategy=delete.cascade, timing=immediate.now, fallback=default.behavior)
    Only named dotted names

    @link(orders.items, products.catalog, status=active.pending, cascade=soft.delete)
    Mixed positional and named dotted names

    @type(string.utf8|number.decimal|boolean.strict)
    Union with dotted names

    @validate(entity, required=true, nullable=false, strategy=validation.strict)
    Mixed simple names and dotted names

    @index(primary.key, secondary.index, unique=constraint.unique | kuku, sparse=index.sparse)
    Complex mixed scenario
    """

    assert parse_properties(comment) == {
        "reference": PropertyResult(
            positional=[["user", "profile", "id"], ["table", "schema", "primary_key"]],
            named={},
        ),
        "config": PropertyResult(
            positional=[],
            named={
                "strategy": ["delete", "cascade"],
                "timing": ["immediate", "now"],
                "fallback": ["default", "behavior"],
            },
        ),
        "link": PropertyResult(
            positional=[["orders", "items"], ["products", "catalog"]],
            named={"status": ["active", "pending"], "cascade": ["soft", "delete"]},
        ),
        "type": PropertyResult(
            positional=[
                UnionValue(
                    values=[
                        ["string", "utf8"],
                        ["number", "decimal"],
                        ["boolean", "strict"],
                    ]
                )
            ],
            named={},
        ),
        "validate": PropertyResult(
            positional=[["entity"]],
            named={
                "required": ["true"],
                "nullable": ["false"],
                "strategy": ["validation", "strict"],
            },
        ),
        "index": PropertyResult(
            positional=[["primary", "key"], ["secondary", "index"]],
            named={
                "unique": UnionValue(values=[["constraint", "unique"], ["kuku"]]),
                "sparse": ["index", "sparse"],
            },
        ),
    }


# Run all tests
if __name__ == "__main__":
    test_empty_and_simple_cases()
    test_whitespace_and_formatting_extremes()
    test_complex_dotted_names_and_unions()

    print("✅ All 3 comprehensive tests passed!")
