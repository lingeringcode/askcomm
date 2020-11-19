# -*- coding: utf-8 -*-
#!/usr/bin/python

# evekeys for Python 3
# by Chris Lindgren <chris.a.lindgren@gmail.com>
# Distributed under the BSD 3-clause license.
# See LICENSE.txt or http://opensource.org/licenses/BSD-3-Clause for details.

# WHAT IS IT?
# A set of search patterns that query a corpus of event-based and community-detected tweets,
# but it could be modified to query most social-network (node-edge) data.

# It assumes you have:
    # imported your corpus as a pandas DataFrame,
    # included metadata information, such as a list of dates and list of groups to reorganize your corpus, and
    # pre-processed your documents as community-detected data across periodic events.

# It functions only with Python 3.x and is not backwards-compatible.

# Warning: evekeys performs little to no custom error-handling, so make sure your inputs are formatted properly. If you have questions, please let me know via email.
import pandas as pd
import ast
import re
from tqdm import tqdm_notebook as tqdm

'''
    find_ht: Queries subset of isolated mentioned or authored tweets with hashtag group list.
        It returns another subset as a dataframe.
        
        Arguments:
            -dft= Dataframe. Subset of tweets.
            -un= String. Desired username of twitter user who authored tweet.
            -hashtags= List of Strings. Desired hashtags to search for in 'hashtags' column.
        Returns:
            -htg_df= Dataframe. Any tweets that meet above query's criteria.
'''
def find_ht(**kwargs):
    htg_tweets = []
    copy_query = kwargs['dft'].copy().reset_index(drop=True)
    copy_query = copy_query.to_dict('records')
    for row in tqdm(copy_query):
        # CHECK MENTIONS
        h = row['hashtags']
        if isinstance(h, str):
            h = ast.literal_eval(h)
            if type(h) == list:
                if len(h) > 0:
                    # Go through list of mentions
                    for ht_check in h:
                        for ht in kwargs['htg']:
                            #If match found, append tweet to list
                            if ht == ht_check:
                                htg_tweets.append(row)
    
    htg_df = pd.DataFrame(htg_tweets)
    
    if len(htg_df) == 0:
        print('No tweets found.')
        return htg_df
    
    # Sort by descending RT counts
    htg_df.sort_values('retweets_count', ascending=False)
        
    return htg_df

'''
    find_links: Queries links in tweets with search string.
        It returns subset as a dataframe.
        
        Arguments:
            -dft= Dataframe. Subset of tweets.
            -url= String. Desired url string element to search in tweet.
        Returns:
            -url_df= Dataframe. Any tweets that meet above query's criteria.
'''
def find_links(**kwargs):
    url_tweets = []
    copy_query = kwargs['dft'].copy().reset_index(drop=True)
    for row in copy_query.to_dict('records'):
        # CHECK URLS
        u = row['urls']
        if isinstance(u, str):
            u = ast.literal_eval(u)
            if len(u) > 0:
                # Go through list of urls
                for u_check in u:
                    #Search for it
                    result = re.search(kwargs['url'], u_check)
                    #If match found, append tweet to list
                    if result != None:
                        url_tweets.append(row)
    
    url_df = pd.DataFrame(url_tweets)
    if len(url_df) == 0:
        print('No tweets found.')
        return url_df
    
    # Sort by descending RT counts
    url_df.sort_values('retweets_count', ascending=False)
        
    return url_df

'''
    find_mentions: Queries full corpus with username, period date range, and mentioned username.
        It returns a dataframe of all tweets found during that period.
        
        Arguments:
            -dft= Dataframe. Full corpus of tweets.
            -st= String. Option designation for search:
                -mentions_only= Searches just mentions
                -user_and_mentions= Searches for tweet author, then searches tweet with mentioned user.
            -un= String. Desired username of twitter user who authored tweet.
            -pd= List of Strings. Dates for period range.
            -mentioned= String. Desired username of twitter user who is mentioned in tweet.
        Returns:
            -pt_df= Dataframe. Any tweets that meet above query's criteria.
'''
def find_mentions(**kwargs):
    period_tweets = []
    p_query = kwargs['dft'].copy().reset_index(drop=True)

    if kwargs['st'] == 'mentions_only':
        for row in p_query.to_dict('records'):
            # CHECK MENTIONS
            m = row['mentions']
            if isinstance(m, str):
                m = ast.literal_eval(m)
                if len(m) > 0:
                    # Go through list of mentions
                    for mention_check in m:
                        if kwargs['mentioned'] == mention_check:
                            period_tweets.append(row)

    elif kwargs['st'] == 'user_and_mentions':
        query = p_query[p_query['username'] == kwargs['un']]
        copy_query = query.copy().reset_index(drop=True)
        for row in copy_query.to_dict('records'):
            m = row['mentions']
            if isinstance(m, str):
                m = ast.literal_eval(m)
                if len(m) > 0:
                    # Go through list of mentions
                    for mention_check in m:
                        if kwargs['mentioned'] == mention_check:
                            period_tweets.append(row)
    
    pt_df = pd.DataFrame(period_tweets)
    
    if len(pt_df) == 0:
        return pt_df
    
    # Sort by descending RT counts
    pt_df.sort_values('retweets_count', ascending=False)
        
    return pt_df

def write_sample_keys(source):
    result = []
    for p1 in range(len(source)):
            for p2 in range(p1+1,len(source)):
                    result.append([source[p1],source[p2]])
                    result.append([source[p2],source[p1]])
    return result

'''
    query_controller: Accepts hub user data and searches for tweets germane to the detected module community.
    
    Arguments:
        - hubs: 
        - hub_col_period
        - hub_col_module
        - hub_col_users
        - col_dates
        - period_range
        - module_range
        - corpus:
        - period_dates:
        - htg_list:
    Returns:
        - DataFrame with period, module, node name, and content
'''
def query_controller(**kwargs):
    new_corpus_dict = {}
    
    #1. Parse each period
    for p in range(kwargs['period_range'][0],kwargs['period_range'][1]+1):
        
        p = str(p)
        new_corpus_dict[p] = {}
        
        # Reduce corpus to period
        corpus_htg = kwargs['corpus'][kwargs['corpus']['date'].isin(kwargs['period_dates'][p])]
        
        #2. Parse each period
        for m in range(kwargs['module_range'][0],kwargs['module_range'][1]+1):
            
            m = str(m)
            new_corpus_dict[p][m] = {}
                        
            #3. create source-target hub user list
            hubs = kwargs['hubs']
            hubs_subset = hubs[(hubs[kwargs['hub_col_period']] == int(p)) & (hubs[kwargs['hub_col_module']] == int(m))]
            hu_list = hubs_subset[[kwargs['hub_col_users']]].values.tolist()
            hub_user_list = []
            for hul in hu_list:
                hub_user_list.append(hul[0])
                
            #4. Create sampling list of lists
            sample_keys = write_sample_keys(hub_user_list)

            for sk in sample_keys:
                new_corpus_dict[p][m][sk[0]] = {
                    'um':[],
                    'm':[],
                    'actual':[]
                }

                #2. Query user_and_mentions
                query_user_and_mentions = find_mentions(
                    dft=corpus_htg,
                    st='user_and_mentions', #mentions_only or user_and_mentions
                    un=sk[0], #ignored, if 'mentions_only'
                    mentioned=sk[1]
                )

                # If no um, search for any authored tweets by user source
                if query_user_and_mentions.empty:
                    query_a = corpus_htg[(corpus_htg['username'] == sk[0])]

                    if query_a.empty:
                        # Find hub info for user
                        hub_user = hubs[
                            (hubs[kwargs['hub_col_period']] == int(p)) 
                            & (hubs[kwargs['hub_col_module']] == int(m)) 
                            & (hubs[kwargs['hub_col_users']] == sk[0])
                        ]
                        # Translate df as dict
                        hu_dict_list = hub_user.to_dict('records')
                        hu_dict = hu_dict_list[0]

                        # Add 'None'
                        hu_dict.update({'tweet': 'None'})
                        new_corpus_dict[p][m][sk[0]]['actual'].append(hu_dict)

                    elif not query_a.empty:
                        # Sort by descending RT counts
                        sorted_df = query_a.sort_values('retweets_count', ascending=False)

                        # # Create tweet output to add
                        # sdf = sorted_df.iloc[:1]
                        # add_tweets = sdf['username'].values[0]+' :: RTs '+str(sdf['retweets_count'].values[0])+', Likes '+str(sdf['likes_count'].values[0])+': '+sdf['tweet'].values[0]

                        # Find hub info for user
                        hub_user = hubs[
                            (hubs[kwargs['hub_col_period']] == int(p)) 
                            & (hubs[kwargs['hub_col_module']] == int(m)) 
                            & (hubs[kwargs['hub_col_users']] == sk[0])
                        ]
                        # Translate df as dict
                        hu_dict_list = hub_user.to_dict('records')
                        hu_dict = hu_dict_list[0]

                        # Add most RT'd tweet
                        hu_dict.update({'tweet': sorted_df.to_dict('records')})
                        new_corpus_dict[p][m][sk[0]]['m'].append(hu_dict)

                elif not query_user_and_mentions.empty:                        
                    # Sort by descending RT counts
                    sorted_df = query_user_and_mentions.sort_values('retweets_count', ascending=False)

                    # # Create tweet output to add
                    # sdf = sorted_df.iloc[:1]
                    # add_tweets = sdf['username'].values[0]+' :: RTs '+str(sdf['retweets_count'].values[0])+', Likes '+str(sdf['likes_count'].values[0])+': '+sdf['tweet'].values[0]

                    # Find hub info for user
                    hub_user = hubs[
                        (hubs[kwargs['hub_col_period']] == int(p)) 
                        & (hubs[kwargs['hub_col_module']] == int(m)) 
                        & (hubs[kwargs['hub_col_users']] == sk[0])
                    ]
                    # Translate df as dict
                    hu_dict_list = hub_user.to_dict('records')
                    hu_dict = hu_dict_list[0]

                    # Add most RT'd tweet
                    hu_dict.update({'tweet': sorted_df.to_dict('records')})
                    new_corpus_dict[p][m][sk[0]]['um'].append(hu_dict)
    
    return new_corpus_dict

'''
    convert_to_df: Converts the Dict output from query_controller into a Dataframe with top result per user. If no tweet found , appends as None.
'''
def convert_to_df(corp_dict):
    final_list = []
    for p in corp_dict:
        for m in corp_dict[p]:
            for user in corp_dict[p][m]:

                # if no user and mentions
                if len(corp_dict[p][m][user]['um']) == 0:

                    # Check if no mentions only
                    if len(corp_dict[p][m][user]['m']) == 0:

                        if len(corp_dict[p][m][user]['actual']) != 0:
                            final_list.append(corp_dict[p][m][user]['actual'][0])

                    #  Check if mentions only
                    if len(corp_dict[p][m][user]['m']) != 0:
                        final_list.append(corp_dict[p][m][user]['m'][0])

                if len(corp_dict[p][m][user]['um']) != 0:
                    final_list.append(corp_dict[p][m][user]['um'][0])

    fl_df = pd.DataFrame(final_list)
    return fl_df

def print_subset(query, columns, n):
    qu = query.sort_values('retweets_count', ascending=False)
    
    # Print out returned tweets with reduced columns. Change columns, if desired.
    if len(qu) == 0:
        print('no tweets')
    else:
        for q in qu[columns].to_dict('records')[:n]:
            print(q,'\n\n')