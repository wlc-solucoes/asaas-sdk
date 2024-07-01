
def remove_none_and_empty_values(data: dict) -> dict:
    return {k: v for k, v in data.items() if v is not None and v != ''}
