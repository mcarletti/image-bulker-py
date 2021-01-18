# Image bulker

Python script providing a simple way to download bulk of thumbnail images from Google.

### Features
* enable parallel download by setting number of jobs (ie. threads);
* organize images in a dataset, organizing downloaded data in two subfolders: train and test.

### Limitations
* it downloads only thumbnails;
* invalid urls are skipped and not substituted.


## Getting started

Download a copy of the project repository.
```bash
git clone https://github.com/mcarletti/image-bulker-py
cd image-bulker-py
```

Install Python requirements.
```bash
pip install -r requirements.txt
```

Set the classes `class_labels.txt` file according to your needs.
Each line of this file relates to a class and is used as a search query passed to the Google search engine.
Multiple words per query are allowed.

To run the image bulker, simply run the following command:
```bash
python main.py
```

### Options
* `samples_per_class` : number of images per class;
* `as_dataset` : enable dataset folders organization;
* `verbose` : enable verbosity;
* `jobs` : number of parallel jobs.

## Disclaimer
This program lets you download tons of images from Google.
Please do not download or use any image that violates its copyright terms.

## Licence
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)