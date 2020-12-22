import os
from fp.fp import FreeProxy
import pandas as pd
from scholarly import scholarly, ProxyGenerator

from crawler.logger import get_logger

logger = get_logger(__name__)


def crawl(path, funding_num):
    logger.info(f"crawling funding number {funding_num}")
    pg = ProxyGenerator()
    #pg.Tor_Internal(tor_cmd="tor")
    pg.Tor_External(tor_sock_port=9050, tor_control_port=9051, tor_password="scholarly_password")
    scholarly.use_proxy(pg)
    #pg = ProxyGenerator()
    #proxy = FreeProxy(rand=True, timeout=2, country_id=['DE', 'BE', 'BG']).get()
    #pg.SingleProxy(http=proxy, https=proxy)
    #scholarly.use_proxy(pg)

    publications = scholarly.search_pubs(funding_num)
    df = pd.DataFrame(columns=['title', 'year', 'citations', 'authors', 'venue', 'link'])
    for index, publication in enumerate(publications):
        publication = scholarly.fill(publication)
        pub_dict = {"title": publication["bib"]["title"],
                    "year": publication["bib"]["pub_year"],
                    "citations": publication["num_citations"],
                    "authors": publication["bib"]["author"],
                    "venue": publication["bib"]["venue"] if 'venue' in publication["bib"] else None,
                    "link": publication["pub_url"]
                   }
        df = df.append(pub_dict, ignore_index=True)
    file_name = f"{funding_num}.json"
    file_path = os.path.join(path, file_name)
    df.to_json(file_path, orient="records")
    logger.info(f"Finished crawling for funder {funding_num}")