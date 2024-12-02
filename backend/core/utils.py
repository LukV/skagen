import ulid

def generate_id(prefix: str) -> str:
    """
    Generates a unique ID with the given prefix.

    Args:
        prefix (str): A single character representing the entity type.

    Returns:
        str: The generated unique ID.
    """
    if len(prefix) != 1 or not prefix.isalpha() or not prefix.isupper():
        raise ValueError("Prefix must be a single uppercase letter.")
    return f"{prefix}{ulid.new()}"
