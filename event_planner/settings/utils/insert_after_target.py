from typing import TypeVar

# Define a type variable to use in the insert_after_target function.
# This is needed to ensure that the sequence is a list of elements of the same type
# as the target and new_element.
_EL = TypeVar("_EL")


def insert_after_target(
    sequence: list[_EL],
    target: _EL,
    new_element: _EL,
) -> list[_EL]:
    """
    Insert a new element after a target element in a sequence.

    Args:
        sequence: The sequence to insert the new element into.
        target: The element to insert the new element after.
        new_element: The new element to insert.

    Returns:
        The sequence with the new element inserted after the target element.

    Raises:
        ValueError: If the target element is not in the sequence.

    """
    index = sequence.index(target)

    new_sequence = sequence.copy()
    new_sequence.insert(index + 1, new_element)

    return new_sequence
