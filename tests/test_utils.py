from src.villa_availabitlity.utils import merge_villas


def test_merge_villas():
    data_1 = [
        {"name": "villa 1", "months": [{"month_name": "January", "percentage_blocked": 10}]},
        {"name": "villa 2", "months": [{"month_name": "January", "percentage_blocked": 20}]},
    ]
    data_2 = [
        {"name": "villa 1", "months": [{"month_name": "January", "percentage_blocked": 11}]},
        {"name": "villa 3", "months": [{"month_name": "January", "percentage_blocked": 30}]},
    ]
    merged = merge_villas(data_1, data_2)
    assert merged == [
        {"name": "villa 1", "months": [{"month_name": "January", "percentage_blocked": 11}]},
        {"name": "villa 2", "months": [{"month_name": "January", "percentage_blocked": 20}]},
        {"name": "villa 3", "months": [{"month_name": "January", "percentage_blocked": 30}]},
    ]
