=========
 askcomm
=========

Overview
========

A set of search patterns that query a corpus of event-based and community-detected social network (node-edge) data. The queries are great for content produced within the detected-community subgraph data.

It assumes you have:

- imported your corpus as a pandas DataFrame,
- included metadata information, such as a list of dates and list of groups to reorganize your corpus, and
- pre-processed your documents as community-detected data across periodic events.

Functions
=========

``query_controller``: Accepts corpus and hub user data and searches for content germane to the detected module community across a range of periods and communities. 

- ``find_mentions``: A function to conduct a cross-reference search within a period's data range with 2 options: ``mentions_only`` or ``user_and_mentions``. 
 - ``mentions_only`` searches a column with a List of mentions per tweet.
 - ``user_and_mentions`` cross references the author of a tweet with the list of mentions.
 - @returns a Dict of top result posts/content found during that period.

``
query_controller(
 hubs=df_hubs,#community-detected data
 hub_col_period='period',#column name for periods
 hub_col_module='info_module',# column name for community name
 hub_col_users='name',#column name for specific user
 period_range=[1,10],#range of desired periods
 module_range=[1,10],#range of desired communities/modules
 corpus=c_htg,#content corpus
 period_dates=period_dates,#List of lists with date ranges
 col_dates='dates'#column name for dates
)
``

`convert_to_df`: Converts the Dict output from query_controller into a Dataframe with top result per user. If no tweet found , appends as None.

`find_ht`: Queries subset of isolated mentioned or authored tweets with hashtag group list. It returns another subset as a dataframe.

`find_links`: Queries links in tweets with search string. It returns subset as a dataframe.

Other functions include: `find_mentions` and `print_subset`.

It functions only with Python 3.x and is not backwards-compatible.

**Warning**: askcomm performs little to no custom error-handling, so make sure your inputs are formatted properly. If you have questions, please let me know via email.

System requirements
===================

* pandas
* tqdm

Installation
============

1. Download this repo onto your computer.
2. Store the folder in a meaningful location.
3. Open a terminal.
4. In the terminal, navigate to the root of the folder.
5. In the terminal, run ```pip install .```

Known Issues or Limitations
===========================

Please contact me if you discover any issues.

Example notebooks
=================

- Coming ...
