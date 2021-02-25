import os
from random import shuffle
from tqdm import tqdm
from models import Pizza, Order, Delivery

FILE_NAMES = ['a_example', 'b_little_bit_of_everything', 'c_many_ingredients', 'd_many_pizzas', 'e_many_teams']


def read_order(file_name: str):
    with open(f'input_files/{file_name}.in') as f:
        num_pizzas, *teams = map(int, f.readline().split())
        pizzas: list[Pizza] = []

        for pizza_id, line in enumerate(f.readlines()):
            num_ingredients, *ingredients = line.split()
            pizzas.append(Pizza(pizza_id, int(num_ingredients), ingredients))

        # Shuffle the pizzas to help us get a random first pizza on each delivery.
        shuffle(pizzas)
        pizzas.sort(key=lambda x: x.num_ingredients, reverse=True)
    return Order(num_pizzas, teams, pizzas)


def write_deliveries(file_name: str, deliveries: list[Delivery]):
    with open(f'output_files/{file_name}.out', 'w+') as f:
        print(len(deliveries), file=f)
        for delivery in deliveries:
            print(delivery, file=f)


def score_delivery(delivery: Delivery) -> int:
    # This is based on the provided score method in the problem statement.
    return len(set(ingredient for pizza in delivery.pizzas for ingredient in pizza.ingredients)) ** 2


def score_deliveries(deliveries: list[Delivery]) -> int:
    return sum(score_delivery(delivery) for delivery in deliveries)


def score_pizza(current_ingredients: set[str], pizza: Pizza) -> int:
    unique_ingredients = len(current_ingredients.intersection(pizza.ingredients))
    total_ingredients = len(current_ingredients.union(pizza.ingredients))
    return total_ingredients - unique_ingredients


def get_delivery(members: int, available_pizzas: list[Pizza]) -> Delivery:
    pizzas: list[Pizza] = []
    current_ingredients = set()
    for _ in range(members):
        # Find the best pizza that matches our current ingredients based on our scoring function.
        pizza = max(available_pizzas, key=lambda x: score_pizza(current_ingredients, x))
        current_ingredients.update(pizza.ingredients)
        available_pizzas.remove(pizza)
        pizzas.append(pizza)
    return Delivery(members, pizzas)


def get_deliveries(order: Order, members: int, progress_bar: tqdm) -> list[Delivery]:
    deliveries: list[Delivery] = []
    teams_index = members - 2
    while order.num_pizzas >= members and order.teams[teams_index] > 0:
        delivery = get_delivery(members, order.pizzas)
        deliveries.append(delivery)
        progress_bar.update(members)
        order.num_pizzas -= members
        order.teams[teams_index] -= 1
    return deliveries


def solution(file_name: str):
    order = read_order(file_name)
    deliveries: list[Delivery] = []
    progress_bar = tqdm(total=order.num_pizzas, desc=f'{file_name}.in')

    # Change the order to experiment with solutions:
    # Starting with 4 members results in getting the highest score on most input files.
    deliveries.extend(get_deliveries(order, members=4, progress_bar=progress_bar))
    deliveries.extend(get_deliveries(order, members=3, progress_bar=progress_bar))
    deliveries.extend(get_deliveries(order, members=2, progress_bar=progress_bar))

    progress_bar.close()

    write_deliveries(file_name, deliveries)
    score = score_deliveries(deliveries)
    print(f'{file_name}.in score => {score}')


def main():
    if not os.path.exists('output_files'):
        os.makedirs('output_files')

    for file_name in FILE_NAMES:
        solution(file_name)


if __name__ == '__main__':
    main()
