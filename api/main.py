from configurations import Configuration
from generator import Generator
from storage import Storage
from visualizer import Visualizer


d = [2.36, 4.75, 9.50, 12.70, 19.00]
# d = [4.00, 7.00, 10.00, 13.00, 16.00, 19.00]
# d = [4.75, 7.40, 10.05, 12.70]
# p = [0, 26, 77, 100]

# p = [1.4, 10, 61, 97, 100]

print('defining storage')
storage = Storage()
print('initiating configurations')
config = Configuration(
    d,
    0.3,
    0.5,
    0.15,
    n_min=8,
    n_max=18,
    x_min=0,
    x_max=50,
    y_min=0,
    y_max=50,
    z_min=0,
    z_max=50
)
print('initiating generator')
generator = Generator(config, storage)
print('generating')
generator.wrapper()
print('initiating visualizer')
visualizer = Visualizer(storage.polyhedrons, storage.hull)
print('visualizing')
visualizer.visualize()
# print(storage.hull)
# print(storage.polyhedrons)
print('exporting to csv')
storage.export_to_csv()
print('done')
print(f'total aggregates generated: {len(storage.polyhedrons)}')
# import pandas as pd
# df = pd.read_csv('../coordinates.csv')
# df.to_excel('coordinates.xlsx', index=False)
