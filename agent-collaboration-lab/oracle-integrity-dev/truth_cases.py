"""Hand-specified cases and expected outputs, separate from candidate implementations.

These are public DEV labels, not unseen confirmation truth.
"""
CASES = {
    'interval': [
        ('partial overlap', ((1, 6), (4, 9)), True),
        ('touching endpoints', ((1, 4), (4, 9)), False),
        ('disjoint', ((1, 3), (5, 8)), False),
        ('nested', ((1, 10), (2, 6)), True),
        ('identical', ((2, 6), (2, 6)), True),
        ('zero length first', ((3, 3), (1, 5)), False),
        ('zero length second', ((1, 5), (3, 3)), False),
        ('reverse partial', ((4, 9), (1, 6)), True),
    ],
    'first_seen': [
        ('empty', ([],), []),
        ('single', ([('z', 5)],), [('z', 5)]),
        ('two in order', ([('z', 5), ('a', 8)],), [('z', 5), ('a', 8)]),
        ('adjacent duplicate', ([('z', 5), ('z', 9)],), [('z', 5)]),
        ('nonadjacent duplicate', ([('z', 5), ('a', 8), ('z', 9)],), [('z', 5), ('a', 8)]),
        ('repeated all', ([('b', 3), ('a', 2), ('b', 4), ('a', 6)],), [('b', 3), ('a', 2)]),
        ('not sorted', ([('c', 1), ('a', 2), ('b', 3)],), [('c', 1), ('a', 2), ('b', 3)]),
        ('two-key second appearance', ([('y', 7), ('x', 0), ('x', 1)],), [('y', 7), ('x', 0)]),
    ],
}
