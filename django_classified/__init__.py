VERSION = (1, 2, 0)


def get_version():
    """Return the version as a human-format string."""
    version = f"{VERSION[0]}.{VERSION[1]}"
    # Append 3rd symbol if it's not zero
    if VERSION[2]:
        version = f"{version}.{VERSION[2]}"

    return version
