import json

from pizza import Pizza, PizzaOrder
from configparser import ConfigParser
from confluent_kafka import Producer, Consumer

config_parser = ConfigParser(interpolation=None)
config_file = open('config.properties', 'r')
config_parser.read_file(config_file)
producer_config = dict(config_parser['kafka_client'])
consumer_config = dict(config_parser['kafka_client'])
consumer_config.update(config_parser['consumer'])
pizza_producer = Producer(producer_config)

pizza_warmer = {}
pizza_topic = 'pizza'
completed_pizza_topic = 'pizza-with-veggies'


def order_pizzas(count):
    order = PizzaOrder(count)
    pizza_warmer[order.id] = order
    for i in range(count):
        new_pizza = Pizza()
        new_pizza.order_id = order.id
        pizza_producer.produce(pizza_topic, key=order.id, value=new_pizza.toJSON())
    pizza_producer.flush()
    return order.id

def get_order(order_id):
    load_orders()

    order = pizza_warmer[order_id]
    if order == None:
        return "No pizza found!"
    else:
        return order.toJSON()


def load_orders():
    pizza_consumer = Consumer(consumer_config)
    pizza_consumer.subscribe([completed_pizza_topic])
    for i in range(60):
        msg = pizza_consumer.poll(0.05)
        if msg is None:
            pass
        elif msg.error():
            print(f'Bummer - {msg.error()}')
        else:
            pizza = json.loads(msg.value())
            add_pizza(pizza['order_id'], pizza)
    pizza_consumer.close()

def add_pizza(order_id, pizza):
    if order_id in pizza_warmer.keys():
        order = pizza_warmer[order_id]
        order.add_pizza(pizza)
