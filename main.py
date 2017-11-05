from bulker import ImageBulker
from sklearn.model_selection import train_test_split
import os


parent_folder = './data'
dataset_name = 'africa'
class_labels = ['lion', 'giraffe', 'elephant', 'gorilla', 'parrot']
nb_samples_per_class = 100

dataset_path = os.path.join(parent_folder, dataset_name)
use_single_cpu = True

bulk = ImageBulker()


def collect_class_images(label, dest_folder='', verbose=True):
    if verbose:
        print('Collecting:', label)
    urls = bulk.get_thumbnail_urls(label.replace(' ', '+'), nb_samples_per_class)
    if verbose:
        print('Found', len(urls), 'images')
    train_urls, test_urls = train_test_split(urls, train_size=0.8)
    class_name = label.replace(' ', '_')
    bulk.download_thumbnails_from_urls(train_urls, dest_folder=os.path.join(dest_folder, 'train/' + class_name), verbose=False)
    bulk.download_thumbnails_from_urls(test_urls, dest_folder=os.path.join(dest_folder, 'test/' + class_name), verbose=False)


if use_single_cpu:

    for label in class_labels:
        collect_class_images(label, dest_folder=dataset_path, verbose=True)

else:

    from joblib import Parallel, delayed
    import multiprocessing as mlp

    nb_cores = mlp.cpu_count()
    _ = Parallel(n_jobs=nb_cores)(delayed(collect_class_images)(label, dataset_path) for label in class_labels)
