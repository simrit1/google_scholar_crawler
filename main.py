import argparse
import configparser
import os
from functools import partial
from multiprocessing import Pool
import psutil
from crawler.crawl_authors import (crawl_author_with_publications,
                                   crawl_author_info_by_name,
                                   crawl_author_info_by_id,
                                   crawl_keywords)
from crawler.crawl_pubs import crawl_publications
from crawler.merge_data import merge_authors
from visualization import visualize_authors, helpers

def parse_args():
    parser = argparse.ArgumentParser(prog='scholar-crawl',
                                     description='Google Scholar Crawler',
                                     argument_default=argparse.SUPPRESS)
    parser.add_argument(
        '--funder',
        nargs="+",
        default=[],
        help="Funding reference number"
    )
    parser.add_argument(
        '--authors-publications',
        action="store_true",
        help='Entity type to download')
    parser.add_argument(
        '--authors-by-name',
        action="store_true",
        help='Entity type to download')
    parser.add_argument(
        '--authors-by-id',
        action="store_true",
        help='Entity type to download')
    parser.add_argument(
        '--authors-by-keyword',
        nargs="*",
        help='Entity type to download')
    parser.add_argument(
        '--input-file',
        type=str,
        help='Path to input file')
    args = parser.parse_args()
    return args


def main(config, args):
    print(args)
    path = config["storage"]["path"]
    n_hits = config["nauthors"]["n_hits"]
    is_directory_exists = os.path.isdir(path)

    # If folder doesn't exist, then create it.
    if not is_directory_exists:
        os.makedirs(path)
        print(f"created directory : {path}")
    else:
        print(f"Directory {path} exists proceeding as is...")
    num_cpus = psutil.cpu_count(logical=False)
    if len(args["funder"]) > 0:
        print("Crawling publications for the given funding reference numbers")
        with Pool(num_cpus) as p:
            func = partial(crawl_publications, path)
            p.map(func, args["funder"])
    elif "authors_publications" in args:
        assert (args["input_file"] and os.path.isfile(args["input_file"])),\
            "Please provide the correct input file"
        input_file = args["input_file"]
        with open(input_file) as f:
            authors_list = f.read().splitlines()
        assert len(authors_list) > 0, "No Authors in the given input file, please add author names before running"
        print("Crawling publications for the given list Authors")
        with Pool(num_cpus) as p:
            func = partial(crawl_author_with_publications, path)
            p.map(func, authors_list)
    elif "authors_by_name" in args:
        assert (args["input_file"] and os.path.isfile(args["input_file"])),\
            "Please provide the correct input file"
        input_file = args["input_file"]
        with open(input_file) as f:
            authors_list = f.read().splitlines()
        assert len(authors_list) > 0, "No Authors in the given input file, please add author names before running"
        print("Crawling author information for the given list Author names")
        with Pool(num_cpus) as p:
            func = partial(crawl_author_info_by_name, path)
            p.map(func, authors_list)
    elif "authors_by_id" in args:
        assert (args["input_file"] and os.path.isfile(args["input_file"])),\
            "Please provide the correct input file"
        input_file = args["input_file"]
        with open(input_file) as f:
            authors_list = f.read().splitlines()
        assert len(authors_list) > 0, "No Google scholar id's in the given input file, please add scholar id's before running"
        print("Crawling author information for the given list Authors")
        with Pool(num_cpus) as p:
            func = partial(crawl_author_info_by_id, path)
            p.map(func, authors_list)
    elif "authors_by_keyword" in args:
        assert (args["input_file"] and os.path.isfile(args["input_file"])),\
            "Please provide the correct input file"
        input_file = args["input_file"]
        with open(input_file) as f:
            keyword_list = f.read().splitlines()
        assert len(keyword_list) > 0, "No keywords are provided in the input file, please them before running"
        print("Crawling author information for the given list of Keywords")
        with Pool(num_cpus) as p:
            func = partial(crawl_keywords, path, n_hits)
            p.map(func, keyword_list)
    else:
        print("Please pass funding reference numbers or authors list or\
            keywords to crawl information")


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    args = vars(parse_args())
    main(config, args)
    merge_authors(config)
    visualize_authors.get_top_citeBy_researchers(config)
    visualize_authors.get_top_hindex_researchers(config)
    visualize_authors.get_top_interests(config)
    helpers.generate_pdf(config)
