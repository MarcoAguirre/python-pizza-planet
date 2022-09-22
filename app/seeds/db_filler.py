from app.repositories.models import IngredientDetail, Size, Ingredient, Beverage, Order
from flask_seeder import Seeder, Faker, generator
from datetime import datetime, timezone, timedelta
import random

size_list = [
    {'name': 'slice', 'price': 1.25},
    {'name': 'personal', 'price': 1.25},
    {'name': 'medium', 'price': 1.25},
    {'name': 'big', 'price': 1.25},
]

beverage_list = ['Coca-cola', 'Fanta', 'Sprite', 'Fiora', 'Gallito']

ingredient_list = ['Chicken', 'Cheese', 'Tomato', 'Pepper', 'Salami',
                   'Jam', 'Mushrooms', 'Pinaple', 'Onion', 'Sauce']

total_orders = 100

name_list_path = "./app/seeds/data/names/names.txt"


def read_txt_file_with_names_line_by_line(path):
    with open(path) as name:
        return name.read().splitlines()


class SequenceList(generator.Sequence):
    def __init__(self, list: list):
        super().__init__(start=0, end=len(list))
        self._list = list

    def generate(self):
        value = self._next
        self._next += 1

        return self._list[value]


class CustomNameGenerator(generator.Generator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._lines = None

    def generate(self):
        if self._lines is None:
            self._lines = read_txt_file_with_names_line_by_line(
                name_list_path)

        result = self.rnd.choice(self._lines)

        return result


class DateGenerator(generator.Generator):

    def __init__(self, start_date: datetime, **kwargs):
        super().__init__(**kwargs)
        self._start_date = start_date

    def generate(self):
        days_to_generate_dates = timedelta(days=8)
        end_date = datetime.now(timezone.utc)
        random_date = self._start_date + \
            random.randrange((end_date - self._start_date) //
                             days_to_generate_dates + 1) * days_to_generate_dates

        return random_date


class DbSeeder(Seeder):
    def generate_ingredients_or_beverages(self, model, order_component: list):
        fake_items = Faker(cls=model, init={
            "_id": generator.Sequence(end=total_orders),
            "name": SequenceList(order_component),
            "price": generator.Integer(start=1, end=13)
        })

        return fake_items

    def generate_sizes(self):
        size_names = [size['name'] for size in size_list]
        size_prices = [size['price'] for size in size_list]

        fake_sizes = Faker(cls=Size, init={
            "_id": generator.Sequence(end=total_orders),
            "name": SequenceList(size_names),
            "price": SequenceList(size_prices)
        })

        return fake_sizes

    def generate_orders(self):
        fake_order = Faker(cls=Order, init={
            "_id": generator.Sequence(end=total_orders),
            "client_name": CustomNameGenerator(),
            "client_dni": 'client',  # This DNI will have the client name too in order to be unique
            "client_address": generator.String('[a-m]'),
            "client_phone": generator.String('[0-9]'),
            "date": DateGenerator(start_date=datetime(1997, 6, 22, tzinfo=timezone.utc)),
            "total_price": 1,
            "size_id": generator.Integer(start=1, end=len(size_list))
        })

        fake_ingredient_detail = Faker(cls=IngredientDetail, init={
            "_id": generator.Sequence(end=total_orders),
            "ingredient_price": 1,
            "order_id": generator.Integer(start=1, end=total_orders),
            "ingredient_id": generator.Integer(start=1, end=len(ingredient_list))
        })

        fake_order_list = [order for order in fake_order.create(total_orders)]
        fake_ingredient_detail_list = [
            ingredient_detail for ingredient_detail in fake_ingredient_detail.create(total_orders)]

        return fake_order_list, fake_ingredient_detail_list

    def save_data_in_corresponding_db(self, data):
        for db_register in data:
            self.db.session.add(db_register)

    def calculate_ingredient_total_price(self, ingredients: list, ingredients_detailed: list):
        for ingredient_in_detail in ingredients_detailed:
            ingredient_in_detail.ingredient_price = sum(
                [ingredient.price for ingredient in ingredients
                 if ingredient._id == ingredient_in_detail.ingredient_id])

    def calculate_order_total_price(self, orders: list, sizes: list, orders_ingredients: list):
        for order in orders:
            '''
            Here it is necessary to generate a unique DNI for client due to the String generator was assigning random DNIs
            that means that if a repeated client exists, they both will have different DNIs
            '''
            order.client_dni += f'-{order.client_name}'
            total_ingredients = sum([
                ingredient_detail.ingredient_price for ingredient_detail in orders_ingredients
                if ingredient_detail.order_id == order._id])

            size_total_price = sum(
                [size.price for size in sizes if size._id == order.size_id])

            order.total_price = total_ingredients + size_total_price

    def run(self):
        ingredients = [ingredient for ingredient in self.generate_ingredients_or_beverages(
            Ingredient, ingredient_list).create(len(ingredient_list))]

        beverages = [beverage for beverage in self.generate_ingredients_or_beverages(
            Beverage, beverage_list).create(len(beverage_list))]

        sizes = [size for size in self.generate_sizes().create(len(size_list))]

        orders, ingredient_details = self.generate_orders()

        self.calculate_ingredient_total_price(ingredients, ingredient_details)
        self.calculate_order_total_price(orders, sizes, ingredient_details)

        self.save_data_in_corresponding_db(sizes)
        self.save_data_in_corresponding_db(ingredients)
        self.save_data_in_corresponding_db(ingredient_details)
        self.save_data_in_corresponding_db(beverages)
        self.save_data_in_corresponding_db(orders)
