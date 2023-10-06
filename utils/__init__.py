__all__ = ["is_numeric"]


def is_numeric(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
