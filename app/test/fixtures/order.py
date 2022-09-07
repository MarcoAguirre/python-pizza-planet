import pytest


from ..utils.functions import (shuffle_list, get_random_sequence,
                               get_random_string)


def client_data_mock() -> dict:
    return {
        'client_address': get_random_string(),
        'client_dni': get_random_sequence(),
        'client_name': get_random_string(),
        'client_phone': get_random_sequence()
    }


@pytest.fixture
def order_uri():
    return '/order'


@pytest.fixture
def client_data():
    return client_data_mock()


def order(create_ingredients, create_size, client_data) -> dict:
    ingredients = [ingredient.get('_id') for ingredient in create_ingredients]
    size_id = create_size.json.get('_id')
    return {
        **client_data_mock(),
        'ingredients': ingredients,
        'size_id': size_id
    }


@pytest.fixture
def create_order(client, order_uri, create_ingredients, create_size, client_data) -> dict:
    response = client.post(order_uri, json=order(
        create_ingredients, create_size, client_data))
    return response


@pytest.fixture
def create_order_detail(create_ingredients, create_size):
    ingredient_ids = [ingredient.get('_id')
                      for ingredient in create_ingredients]
    ingredient_names = [ingredient.get('name')
                        for ingredient in create_ingredients]
    size_id = create_size.json.get('_id')
    return {
        'ingredients_ids': ingredient_ids,
        'ingredients_names': ingredient_names,
        'size_id': size_id
    }


@pytest.fixture
def create_orders(client, order_uri, create_ingredients, create_sizes) -> list:
    ingredients = [ingredient.get('_id') for ingredient in create_ingredients]
    sizes = [size.get('_id') for size in create_sizes]
    orders = []
    for _ in range(10):
        new_order = client.post(order_uri, json={
            **client_data_mock(),
            'ingredients': shuffle_list(ingredients)[:5],
            'size_id': shuffle_list(sizes)[0]
        })
        orders.append(new_order)
    return orders
