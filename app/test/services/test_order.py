import pytest

from app.test.utils.functions import (shuffle_list, get_random_sequence,
                                      get_random_string)


def test_create_order_service(create_order):
    created_order = create_order
    pytest.assume(created_order.status.startswith('308'))


def test_check_order_values(create_order_detail):
    current_order = create_order_detail
    pytest.assume(type(current_order['size_id']) == int)
    returned_order_ids = current_order['ingredients_ids']
    for ingredient_id in returned_order_ids:
        pytest.assume(type(ingredient_id) == int)
    returned_order_names = current_order['ingredients_names']
    for ingredient_name in returned_order_names:
        pytest.assume(type(ingredient_name) == str)


def test_get_orders_service(client, create_orders, order_uri):
    response = client.get(order_uri)
    pytest.assume(response.status.startswith('200'))
    returned_orders = {
        order['_id']: order for order in response.json}
    for order in create_orders:
        pytest.assume(order['_id'] in returned_orders)
