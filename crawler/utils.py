from pymongo import MongoClient
import os

def update_record():
    pass


def read_table(uri):
    client = MongoClient(uri)
    authors = client['groups']['group_author']
    authors = list(authors.find({}, projection=["author_name"]))
    author_names = set([author["author_name"] for author in authors])
    return author_names


def save_unsuccessful_author(path, author):
    with open(os.path.join(path, "fail.log"), "a") as f:
        f.write(author)
        f.write("\n")

