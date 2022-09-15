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


class DbSeeder(Seeder):
    def generate_ingredients_or_beverages(self, model, order_component: list):
        fake_items = Faker(cls=model, init={
            "_id": generator.Sequence(end=total_orders),
            "name": random.choice(order_component),
            "price": generator.Integer(start=1, end=13)
        })

        return fake_items

    def save_data_in_corresponding_db(self, data):
        for db_register in data:
            self.db.session.add(db_register)

    def run(self):
        ingredients = [ingredient for ingredient in self.generate_ingredients_or_beverages(
            Ingredient, ingredient_list).create(len(ingredient_list))]

        beverages = [beverage for beverage in self.generate_ingredients_or_beverages(
            Beverage, beverage_list).create(len(beverage_list))]

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
