import pytest


def test_create_order_service(create_order):
    created_order = create_order
    pytest.assume(created_order.status.startswith('308'))


def test_check_order_values(detail_created_order):
    current_order_detail = detail_created_order
    pytest.assume(type(current_order_detail['client_data']) == dict)
    pytest.assume(type(current_order_detail['size_id']) == int)
    returned_order_ids = current_order_detail['ingredients_ids']
    for ingredient_id in returned_order_ids:
        pytest.assume(type(ingredient_id) == int)
    returned_order_names = current_order_detail['ingredients_names']
    for ingredient_name in returned_order_names:
        pytest.assume(type(ingredient_name) == str)
