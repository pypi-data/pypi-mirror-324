def error(code: int, text: str) -> None:
    """"Prints an error text and exits."""
    print(f"Error {code}: {text}.")
    exit(code)
