"""New synthetic examples, deliberately correct and incorrect. No AI inference."""


def overlapping_half_open_a(a, b):
    return max(a[0], b[0]) < min(a[1], b[1])


def overlapping_half_open_b(a, b):
    return a[0] < a[1] and b[0] < b[1] and a[0] < b[1] and b[0] < a[1]


def overlapping_touch_counts(a, b):
    return max(a[0], b[0]) <= min(a[1], b[1])


def overlapping_containment_only(a, b):
    return (a[0] <= b[0] and b[1] <= a[1]) or (b[0] <= a[0] and a[1] <= b[1])


def overlapping_inclusive_end(a, b):
    return a[0] <= b[1] and b[0] <= a[1]


def first_by_key_a(items):
    seen = set()
    result = []
    for key, payload in items:
        if key not in seen:
            seen.add(key)
            result.append((key, payload))
    return result


def first_by_key_b(items):
    result = dict(items[::-1])  # earliest wins after reverse insertion
    keys = list(dict.fromkeys(key for key, _ in items))
    return [(key, result[key]) for key in keys]


def last_by_key(items):
    values = dict(items)
    keys = list(dict.fromkeys(key for key, _ in items))
    return [(key, values[key]) for key in keys]


def sorted_first_by_key(items):
    first = dict(items[::-1])
    return sorted(first.items())


def adjacent_only(items):
    result = []
    for item in items:
        if not result or result[-1][0] != item[0]:
            result.append(item)
    return result


IMPLEMENTATIONS = {
    'interval': {
        'correct': {'max_min': overlapping_half_open_a, 'direct': overlapping_half_open_b},
        'incorrect': {'touch_counts': overlapping_touch_counts, 'containment_only': overlapping_containment_only, 'inclusive_end': overlapping_inclusive_end},
    },
    'first_seen': {
        'correct': {'set_append': first_by_key_a, 'reverse_dict': first_by_key_b},
        'incorrect': {'last_wins': last_by_key, 'sort_keys': sorted_first_by_key, 'adjacent_only': adjacent_only},
    },
}
