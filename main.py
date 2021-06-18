import argparse
import configparser
import os
from functools import partial
from multiprocessing import Pool

import psutil

from crawler.crawl_authors import crawl_author_with_publications, crawl_author_info_by_name, crawl_author_info_by_id
from crawler.crawl_pubs import crawl as pubs_crawler
from crawler.utils import read_table


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
        '--authors',
        nargs="*",
        default=[],
        help='Entity type to download')
    parser.add_argument(
        '--author_by_name',
        nargs="*",
        default=[],
        help='Entity type to download')
    parser.add_argument(
        '--author_by_id',
        nargs="*",
        default=[],
        help='Entity type to download')
    args = parser.parse_args()
    return args


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    args = vars(parse_args())
    print(args)
    path = config["storage"]["path"]
    CHECK_FOLDER = os.path.isdir(path)

    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(path)
        print("created folder : ", path)
    else:
        print(path, "Folder exists proceeding as is...")
    num_cpus = psutil.cpu_count(logical=False)
    if len(args["funder"]) > 0:
        print("Crawling publications for the given funding reference numbers")
        with Pool(num_cpus) as p:
            func = partial(pubs_crawler, path)
            p.map(func, args["funder"])
    elif len(args["authors"]) > 0:
        if "db" in args["authors"]:
            print("Crawling publications for the ELLIS Fellows")
            # authors_crawler(path, authors_list)
            authors_list = read_table(config["mongo"]["uri"])
            with Pool(num_cpus) as p:
                func = partial(crawl_author_with_publications, path)
                p.map(func, authors_list)
        elif "file" in args["authors"]:
            with open("authors.txt") as f:
                authors_list = f.read().splitlines()
            print("Crawling publications for the given list Authors")
            with Pool(num_cpus) as p:
                func = partial(crawl_author_with_publications, path)
                p.map(func, authors_list)
    elif len(args["author_by_name"]) > 0:
        if "file" in args["author_by_name"]:
            with open("authors_names.txt") as f:
                authors_list = f.read().splitlines()
            print("Crawling author information for the given list Authors")
            with Pool(num_cpus) as p:
                func = partial(crawl_author_info_by_name, path)
                p.map(func, authors_list)
    elif len(args["author_by_id"]) > 0:
        if "file" in args["author_by_id"]:
            with open("author_ids.txt") as f:
                authors_list = f.read().splitlines()
            print("Crawling author information for the given list Authors")
            with Pool(num_cpus) as p:
                func = partial(crawl_author_info_by_id, path)
                p.map(func, authors_list)
    else:
        print("Please pass funding reference numbers or authors list to crawl")


if __name__ == "__main__":
    main()
