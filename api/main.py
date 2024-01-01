from configurations import Configuration
from generator import Generator
from storage import Storage
from visualizer import Visualizer


d = [2.36, 4.75, 9.50, 12.70]

print('defining storage')
storage = Storage()
print('initiating configurations')
config = Configuration(
    d,
    0.45,
    0.5,
    3,
    n_min=8.0,
    n_max=17,
    x_min=0,
    x_max=100,
    y_min=0,
    y_max=100,
    z_min=0,
    z_max=100
)
print('initiating generator')
generator = Generator(config, storage)
print('generating')
generator.wrapper()
print('initiating visualizer')
visualizer = Visualizer(storage.polyhedrons)
print('visualizing')
visualizer.visualize()
print('exporting to csv')
storage.export_to_csv()
print('done')
print(f'total aggregates generated: {len(storage.polyhedrons)}')
