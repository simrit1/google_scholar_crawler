import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
import ast
from visualization.helpers import init, show_values_on_bars

# Set pallete and settings
sns.set_style("whitegrid", {'axes.grid': False})


def get_top_citeBy_researchers(config, last_five=False):
    """
    Obtains the top cited researchers.
    Args:
        config ([type]): [Is the configurations of the config.ini]
        last_five (bool, optional): [If only the last five year stat is required]. Defaults to False.
    """
    data = init(config)
    if len(data) > 15:
        data = data.iloc[:15, :]
    data = data.sort_values("citedBy", ascending=False)
    plt.figure(figsize=(12, 10))
    if last_five:
        sns.barplot(x="citedBy5y", y="name",
                    data=data, orient="h",
                    color="steelblue")
    else:
        sns.barplot(x="citedBy", y="name",
                    data=data, orient="h",
                    color="steelblue")
    path = os.path.dirname(os.path.abspath(__file__))
    save_location = os.path.join(path, "report/figures/")
    plt.savefig(save_location + "citeBy-top.pdf", bbox_inches='tight', dpi=300)


def get_top_hindex_researchers(config, last_five=False):
    """Get the top hindex researchers

    Args:
        config ([type]): [config.ini file configurations]
        last_five (bool, optional): [description]. Defaults to False.
    """
    data = init(config)
    if len(data) > 15:
        data = data.iloc[:15, :]
    data = data.sort_values("hindex", ascending=False)
    plt.figure(figsize=(12, 10))
    if last_five:
        sns.barplot(x="hindex5y", y="name",
                    data=data, orient="h",
                    color="steelblue")
    else:
        sns.barplot(x="hindex", y="name",
                    data=data, orient="h",
                    color="steelblue")
    path = os.path.dirname(os.path.abspath(__file__))
    save_location = os.path.join(path, "report/figures/")
    plt.savefig(save_location + "h-index-top.pdf", bbox_inches='tight', dpi=300)


def get_top_interests(config):
    """Obtain the top interests as keywords across the dataset.

    Args:
        config ([type]): [config.ini]
    """
    keywords_dict = {}

    def get_keywords_dict(x):
        x = ast.literal_eval(x)
        for item in x:
            if item == "NLP":
                item = "Natural Language Processing"
            elif item == "AI":
                item = "Artificial Intelligence"
            print(item)
            if item.lower() not in keywords_dict:
                keywords_dict[item.lower()] = 1
            else:
                keywords_dict[item.lower()] = keywords_dict[item.lower()] + 1

    data = init(config)
    data["interests"].apply(get_keywords_dict)
    keywords = pd.DataFrame(keywords_dict.items())
    keywords.columns = ["keyword", "Counts"]
    keywords = keywords.sort_values("Counts", ascending=False)
    plt.figure(figsize=(12, 8))
    plt.title("Top-20 interests the authors show")
    g = sns.barplot(x="Counts", y="keyword",
                    data=keywords.head(20), color="steelblue")
    # show_values_on_bars(g, h_v="h", space=0.2)
    path = os.path.dirname(os.path.abspath(__file__))
    save_location = os.path.join(path, "report/figures/")
    g.figure.savefig(save_location + "top-keywords.pdf", bbox_inches='tight', dpi=300)
