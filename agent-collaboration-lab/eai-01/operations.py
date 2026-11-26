"""DEV operations. The target contract supplies the oracle for every transformation."""
import unittest


def empty_evidence(entries):
    """Replace a list of evidence items with an empty list."""
    if not isinstance(entries, list):
        raise TypeError("expected a list")
    return []


def suppress_required_check(method):
    """Make one unittest method report skipped when the suite runs."""
    return unittest.skip("synthetic suppression")(method)


def duplicate_evidence(entries, source, destination):
    """Replace one distinct item by another, preserving collection length."""
    if entries[source] == entries[destination]:
        raise ValueError("expected two distinct starting items")
    changed = list(entries)
    changed[destination] = entries[source]
    return changed


def unexpected_type(fields, key, replacement):
    """Replace one member with a different Python type selected by the adapter."""
    if type(fields[key]) is type(replacement):
        raise ValueError("expected a type change")
    return {**fields, key: replacement}


def require_consistent_exit(verdict, returncode, contract):
    """Post-execution assertion. Caller supplies the independently specified map."""
    if verdict not in contract or contract[verdict] != returncode:
        raise AssertionError(f"verdict {verdict!r} disagrees with exit {returncode!r}")
