"""Intentional bad test discovery: direct functions, not unittest TestCase."""
def validate_age(value):
    return type(value) is int and 0 <= value <= 130

def reserve_before_action(predicted_cost, hard_cap):
    return predicted_cost <= hard_cap

def test_age_bool_guard():
    assert validate_age(25)
    assert not validate_age(True)

def test_budget_precheck():
    assert reserve_before_action(150, 150)
    assert not reserve_before_action(216, 150)

if __name__ == '__main__':
    for check in (test_age_bool_guard, test_budget_precheck):
        check()
        print('PASS', check.__name__)
    print('DIRECT_CHECKS_EXECUTED=2')
