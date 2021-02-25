class Pizza:
    def __init__(self, pizza_id: int, num_ingredients: int, ingredients: list[str]):
        self.id = pizza_id
        self.num_ingredients = num_ingredients
        self.ingredients = ingredients


class Order:
    def __init__(self, num_pizzas: int, teams: list[int], pizzas: list[Pizza]):
        self.num_pizzas = num_pizzas
        self.teams = teams
        self.pizzas = pizzas


class Delivery:
    def __init__(self, team_members: int, pizzas: list):
        self.team_members = team_members
        self.pizzas = pizzas

    def __repr__(self):
        return f'{self.team_members} {" ".join(str(pizza.id) for pizza in self.pizzas)}'
