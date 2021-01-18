from bulker import ImageBulker
from sklearn.model_selection import train_test_split
import numpy as np
import os
import argparse


def collect_class_images(label, dest_folder='', verbose=True):
    try:

        if verbose:
            print('Collecting:', label)

        image_bulker = ImageBulker()
        urls = image_bulker.get_thumbnail_urls(label.replace(' ', '+'), args.samples_per_class)
        nb_found_images = len(urls)

        if verbose:
            print('Found', nb_found_images, 'images')

        if nb_found_images == 0:
            err_msg = 'cannot find any image for label ' + label
            raise Exception(err_msg)

        class_name = label.replace(' ', '_')

        if args.as_dataset:
            train_urls, test_urls = train_test_split(urls, train_size=0.8)
            image_bulker.download_thumbnails_from_urls(train_urls, dest_folder=os.path.join(dest_folder, 'train/' + class_name), verbose=verbose)
            image_bulker.download_thumbnails_from_urls(test_urls, dest_folder=os.path.join(dest_folder, 'test/' + class_name), verbose=verbose)
        else:
            image_bulker.download_thumbnails_from_urls(urls, dest_folder=os.path.join(dest_folder, class_name), verbose=verbose)

    except Exception as e:
        print('Cannot collect', label, 'because', e)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--samples_per_class', type=int, default=100)
    parser.add_argument('--output_path', type=str, default='data')
    parser.add_argument('--as_dataset', action='store_true')
    parser.add_argument('--verbose', action="store_true")
    parser.add_argument('--jobs', type=int, default=1)
    args = parser.parse_args()

    assert args.samples_per_class > 0 and args.jobs > 0

    class_labels = np.loadtxt(open('class_labels.txt'), dtype=object, delimiter='\n')

    if args.jobs == 1:

        for label in class_labels:
            collect_class_images(label, dest_folder=args.output_path, verbose=args.verbose)

    else:

        from joblib import Parallel, delayed
        import multiprocessing as mlp

        nb_cores = mlp.cpu_count()
        nb_jobs = np.minimum(args.jobs, nb_cores)
        _ = Parallel(n_jobs=nb_jobs)(delayed(collect_class_images)(label, args.output_path, args.verbose) for label in class_labels)
