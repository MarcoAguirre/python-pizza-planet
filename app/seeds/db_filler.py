from tkinter.font import names
from flask_seeder import Seeder, Faker, generator
from app.repositories.models import Size, Ingredient, Beverage, Order

import random

# class Beverage(Beverage):
#     def generate_ingredients_or_beverages(self, _id=None, name=None, price=None):
#         self._id = _id
#         self.name = name
#         self.price = price

#     def __str__(self):
#         return "ID=%d, Name=%s, Price=%d" % (self._id, self.name, self.price)
size_list = [
    {'name': 'slice', 'price': 1.25},
    {'name': 'personal', 'price': 1.25},
    {'name': 'medium', 'price': 1.25},
    {'name': 'big', 'price': 1.25},
]

beverage_list = ['Coca-cola', 'Fanta', 'Sprite', 'Fiora', 'Gallito']

ingredient_list = ['Chicken', 'Cheese', 'Tomato',
                   'Pepper', 'Salami', 'Jam', 'Mushrooms']

total_orders = 100


class SequenceList(generator.Sequence):
    # def __init__(self, start=1, end=100, **kwargs): #???????????????????????????
    #     super().__init__(start, end, **kwargs)
    def __init__(self, list: list):
        super().__init__(start=0, end=len(list))
        self._list = list

    def generate(self):
        value = self._next
        self._next += 1

        return self._list[value]


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

    def save_data_in_corresponding_db(self, data):
        for db_register in data:
            self.db.session.add(db_register)

    def run(self):
        ingredients = [ingredient for ingredient in self.generate_ingredients_or_beverages(
            Ingredient, ingredient_list).create(len(ingredient_list))]

        beverages = [beverage for beverage in self.generate_ingredients_or_beverages(
            Beverage, beverage_list).create(len(beverage_list))]

        sizes = [size for size in self.generate_sizes().create(len(size_list))]

        self.save_data_in_corresponding_db(sizes)
        self.save_data_in_corresponding_db(ingredients)
        self.save_data_in_corresponding_db(beverages)
        # faker = Faker(
        #     cls=Beverage,
        #     init={
        #         "_id": generator.Sequence(),
        #         "name": generator.Name(),
        #         "price": generator.Integer(start=1, end=10)
        #     }
        # )

        # for user in faker.create(5):
        #     print("Adding user: %s" % user)
        #     self.db.session.add(user)
