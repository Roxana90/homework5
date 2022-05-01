from collections import defaultdict
from helpers.data_types import AvailableFileTypes
from .file_workers import CSVWorker, JSONWorker


class Stats:
    def __init__(self, input_type, output_type):
        available_types_lower = [item.lower() for item in AvailableFileTypes.get_available_types()]
        if input_type not in available_types_lower:
            raise TypeError(f'{input_type} is not an available type.')

        if output_type not in available_types_lower:
            raise TypeError(f'{output_type} is not an available type.')

        self.input_type = input_type
        self.output_type = output_type
        self.input_file_worker = None
        self.out_file_worker = None

        if self.input_type == 'csv':
            self.input_file_worker = CSVWorker()
        elif self.input_type == 'json':
            self.input_file_worker = JSONWorker()

        if self.output_type == 'csv':
            self.output_file_worker = CSVWorker()
        elif self.output_type == 'json':
            self.output_file_worker = JSONWorker()

    def run(self):
        # Step 1. Read from input file
        products = self.input_file_worker.read()
        print('products', products)

        # Step 2. Do some magic
        products_by_colour = defaultdict(list)
        for product in products:
            products_by_colour[product['colour']].append(product)

        products_by_gender = defaultdict(list)
        for product in products:
            products_by_gender[product['gender']].append(product)

        most_sold_products = defaultdict(list)
        for product in products:
            most_sold_products[product['sales']].append(product)


        # Step 3. Write to output file
        for colour, products in products_by_colour.items():
            self.output_file_worker.write(colour, products)

        for gender, products in products_by_gender.items():
            self.output_file_worker.write(gender, products)

        for sales, products in most_sold_products.items():
            self.output_file_worker.write(sales, products)
