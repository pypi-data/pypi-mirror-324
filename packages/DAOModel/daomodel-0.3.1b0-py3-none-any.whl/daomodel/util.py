from typing import Iterable, Any, OrderedDict

from sqlalchemy import Column, ColumnElement
from sqlmodel import or_, and_


class MissingInput(Exception):
    """Indicates that required information was not provided."""
    def __init__(self, detail: str):
        self.detail = detail


def reference_of(column: Column) -> str:
    """
    Prepares a str reference of a column.

    :param column: The column to convert
    :return: The 'table.column' notation of the Column
    """
    return f"{column.table.name}.{column.name}"


def names_of(properties: Iterable[Column]) -> list[str]:
    """
    Reduces Columns to just their names.

    :param properties: A group of Columns
    :return: A list of names matching the order of the Columns provided
    """
    return [p.name for p in properties]


def values_from_dict(*keys, **values) -> tuple[Any, ...]:
    """
    Pulls specific values from a dictionary.

    :param keys: The keys to read from the dict
    :param values: The dictionary containing the values
    :return: A tuple of values read from the dict, in the same order as keys
    """
    result = []
    for key in keys:
        if key in values:
            result.append(values[key])
        else:
            raise MissingInput(f"Requested key {key} not found in dictionary")
    return tuple(result)


def filter_dict(*keys, **values) -> dict[str, Any]:
    """
    Filters a dictionary to specified keys.

    :param keys: The target keys for the new dict
    :param values: The dictionary to filter down
    :return: The filter down values as a new dict
    """
    return {key: values[key] for key in keys}


def ensure_iter(elements):
    """
    Ensures that the provided argument is iterable.
    Single, non-Iterable items are converted to a single-item list.
    In this context, a str is not considered to be Iterable.

    :param elements: The input that may or may not be Iterable
    :return: The provided Iterable or a single item list
    """
    if not isinstance(elements, Iterable) or type(elements) is str:
        elements = [elements]
    return elements


def dedupe(original: list) -> list:
    """
    Creates a filtered copy of a list that does not include duplicates.

    :param original: The list to filter
    :return: a new list that maintains order but is guaranteed to have no duplicates
    """
    return list(OrderedDict.fromkeys(original))


def next_id() -> None:
    """Indicates to the model that an id should be auto incremented"""
    return None


class ConditionOperator:
    """A utility class to easily generate common expressions"""
    def __init__(self, *values: Any):
        self.values = values

    def get_expression(self, column: ColumnElement) -> ColumnElement:
        """Builds and returns the appropriate expression.

        :param column: The column on which to evaluate
        :return: the expression
        """
        raise NotImplementedError("Must implement `get_expression` in subclass")


class GreaterThan(ConditionOperator):
    def get_expression(self, column: ColumnElement) -> ColumnElement:
        return column > self.values[0]


class GreaterThanEqualTo(ConditionOperator):
    def get_expression(self, column: ColumnElement) -> ColumnElement:
        return column >= self.values[0]


class LessThan(ConditionOperator):
    def get_expression(self, column: ColumnElement) -> ColumnElement:
        return column < self.values[0]


class LessThanEqualTo(ConditionOperator):
    def get_expression(self, column: ColumnElement) -> ColumnElement:
        return column <= self.values[0]


class Between(ConditionOperator):
    def get_expression(self, column: ColumnElement) -> ColumnElement:
        lower_bound, upper_bound = self.values
        return and_(column >= lower_bound, column <= upper_bound)


class AnyOf(ConditionOperator):
    def get_expression(self, column: ColumnElement) -> ColumnElement:
        return or_(*[column == value for value in self.values])


class NoneOf(ConditionOperator):
    def get_expression(self, column: ColumnElement) -> ColumnElement:
        return and_(*[column != value for value in self.values])
