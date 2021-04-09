import os
import pandas as pd
from scholarly import scholarly, ProxyGenerator

from crawler.utils import save_unsuccessful_author
from crawler.logger import get_logger

logger = get_logger(__name__)


def crawl(path, author):
    logger.info(f"crawling author {author}")
    df = pd.DataFrame(
        columns=[
            "author_id",
            "authors",
            "title",
            "year",
            "citations",
            "yearly_citations",
        ]
    )
    # pg = ProxyGenerator()
    # pg.Tor_Internal(tor_cmd="tor")
    # scholarly.use_proxy(pg)
    pg = ProxyGenerator()
    pg.Tor_External(
        tor_sock_port=9050, tor_control_port=9051,
        tor_password="scholarly_password"
    )
    scholarly.use_proxy(pg)
    try:
        author_obj = next(scholarly.search_author(author))
    except StopIteration:
        logger.exception(
            f"Author {author} does not match with any names in Google scholar"
        )
        save_unsuccessful_author(path, author)
        return

    publications = scholarly.fill(author_obj, sections=["publications"])
    logger.info(
        f"Number of publications for {author} is\
        {len(publications['publications'])}"
    )

    for index, publication in enumerate(publications["publications"]):
        try:
            pub = scholarly.fill(publication)
        except ValueError as e:
            logger.exception("Exception while parsing the paper")
            logger.exception(e)
            continue
        logger.info(f"processing {author} publication no {index}")
        pub_dict = {
            "author_id": author_obj["scholar_id"],
            "authors": pub["bib"]["author"] if "author" in pub["bib"] else None,
            "title": pub["bib"]["title"],
            "year": pub["bib"]["pub_year"] if "pub_year" in pub["bib"] else 0,
            "citations": pub["num_citations"],
            "yearly_citations": pub["cites_per_year"]
            if "cites_per_year" in pub
            else None,
        }
        df = df.append(pub_dict, ignore_index=True)
    file_name = f"{author_obj['name'].lower().replace(' ', '_')}.csv"
    file_path = os.path.join(path, file_name)
    df.to_csv(file_path, sep=";")
    logger.info(f"Finished crawling author {author}")


def crawl_author_info(path, author):
    logger.info("Crawling information for the author {}".format(author))
    df = pd.DataFrame(
        columns=[
            "author_id",
            "hindex",
            "hindex5y",
            "citedBy",
            "citedBy5y",
            "i10index",
            "i10index5y",
            "cite_counts",
        ]
    )
    pg = ProxyGenerator()
    pg.Tor_External(
        tor_sock_port=9050, tor_control_port=9051, tor_password="scholarly_password"
    )
    scholarly.use_proxy(pg)
    try:
        author_obj = next(scholarly.search_author(author))
    except StopIteration:
        logger.exception(
            f"Author {author} does not match with any names in Google scholar"
        )
        save_unsuccessful_author(path, author)
        return

    author_info = scholarly.fill(author_obj, sections=["basics", "indices", "counts"])
    print(author_info)
    author_dict = {
        "author_id": author_info["scholar_id"],
        "hindex": author_info["hindex"],
        "hindex5y": author_info["hindex5y"],
        "citedBy": author_info["citedby"],
        "citedBy5y": author_info["citedby5y"],
        "i10index": author_info["i10index"],
        "i10index5y": author_info["i10index5y"],
        "cite_counts": author_info["cites_per_year"]
    }
    df = df.append(author_dict, ignore_index=True)
    file_name = f"{author_info['name'].lower().replace(' ', '_')}.csv"
    file_path = os.path.join(path, file_name)
    df.to_csv(file_path, sep=";")
    logger.info("Finished crawling author {}".format(author))
