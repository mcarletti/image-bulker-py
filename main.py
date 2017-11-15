from bulker import ImageBulker
from sklearn.model_selection import train_test_split
import numpy as np
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--samples_per_class', type=int, required=True)
parser.add_argument('--jobs', type=int, default=1)
args = parser.parse_args()

assert args.samples_per_class > 0 and args.jobs > 0

dataset_path = './data'
class_labels = np.loadtxt(open('class_labels.txt'), dtype=object, delimiter='\n')

use_single_cpu = False

bulk = ImageBulker()


def collect_class_images(label, dest_folder='', verbose=True):
    try:
        if verbose:
            print('Collecting:', label)
        urls = bulk.get_thumbnail_urls(label.replace(' ', '+'), args.samples_per_class)
        nb_found_images = len(urls)
        if verbose:
            print('Found', nb_found_images, 'images')
        if nb_found_images == 0:
            err_msg = 'cannot find any image for label ' + label
            raise Exception(err_msg)
        train_urls, test_urls = train_test_split(urls, train_size=0.8)
        class_name = label.replace(' ', '_')
        bulk.download_thumbnails_from_urls(train_urls, dest_folder=os.path.join(dest_folder, 'train/' + class_name), verbose=False)
        bulk.download_thumbnails_from_urls(test_urls, dest_folder=os.path.join(dest_folder, 'test/' + class_name), verbose=False)
    except Exception as e:
        print('Cannot collect', label, 'because', e)


if args.jobs == 1:

    for label in class_labels:
        collect_class_images(label, dest_folder=dataset_path, verbose=True)

else:

    from joblib import Parallel, delayed
    import multiprocessing as mlp

    nb_cores = mlp.cpu_count()
    nb_jobs = np.minimum(args.jobs, nb_cores)
    _ = Parallel(n_jobs=nb_jobs)(delayed(collect_class_images)(label, dataset_path) for label in class_labels)
