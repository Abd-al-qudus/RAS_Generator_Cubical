from configurations import Configuration
from generator import Generator
from storage import Storage
from visualizer import Visualizer


# d = [4.75, 9.50, 12.70, 19.00]
# d = [4.75, 7.125, 9.50, 11.10, 12.70, 15.85, 19.00]
d = [2.36, 4.75, 9.50, 12.70]
# d = [4.00, 6.00, 8.00, 10.00]
# p = [0, 26, 77, 100]

# p = [1.4, 10, 61, 97, 100]
# d = [4.75, 7.125, 9.50, 11.10]

print('defining storage')
storage = Storage()

print('initiating configurations')
config = Configuration(
    d,
    0.35,
    0.5,
    0.005,
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
visualizer = Visualizer(storage.ellipsoids);

print('visualizing')
visualizer.visualize()
# print(storage.hull)
# print(storage.polyhedrons)

print('exporting to csv')
storage.export_to_csv()

print('done')
print(f'total aggregates generated: {len(storage.ellipsoids)}')
# import pandas as pd
# df = pd.read_csv('../coordinates.csv')
# df.to_excel('coordinates.xlsx', index=False)
