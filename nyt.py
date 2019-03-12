from nytimesarticle import articleAPI
import csv
import time


def parse_articles(articles):
    '''
    This function takes in a response to the NYT api and parses
    the articles into a list of dictionaries
    '''
    news = []

    if 'fault' in articles or articles['status'] != 'OK':
        print(articles)
        return []

    for article in articles['response']['docs']:
        rec = {}
        for k, v in article.items():
            rec['id'] = article['_id']

            if k == 'abstract':
                rec['abstract'] = v
            elif k == 'headline':
                rec['headline'] = v['main']
            elif k == 'news_desk':
                rec['desk'] = v
            elif k == 'pub_date':
                rec['date'] = v[0:10]
            elif k == 'section_name':
                rec['section'] = v
            elif k == 'snippet':
                rec['snippet'] = v
            elif k == 'source':
                rec['source'] = v
            elif k == 'type_of_material':
                rec['type'] = v
            elif k == 'web_url':
                rec['url'] = v
            elif k == 'word_count':
                rec['word_count'] = v

        # locations
        locations = []
        for x in range(0, len(article['keywords'])):
            if 'glocations' in article['keywords'][x]['name']:
                locations.append(article['keywords'][x]['value'])
        rec['locations'] = locations
        # subject
        subjects = []
        for x in range(0, len(article['keywords'])):
            if 'subject' in article['keywords'][x]['name']:
                subjects.append(article['keywords'][x]['value'])
        rec['subjects'] = subjects
        news.append(rec)
        # print(rec)
    return news


def get_articles(begin_date, end_date, query):
    '''
    This function accepts a year in string format (e.g.'1980')
    and a query (e.g.'Amnesty International') and it will
    return a list of parsed articles (in dictionaries)
    for that year.
    '''
    api = articleAPI('Tmsq1B5GKZ9O8WLqYXxHEb6UG6Q6YE2k')
    # api = articleAPI('ARZ7pk2xuOAxjQts3LftoBXfi1PWt6s7')
    all_articles = []
    for i in range(0, 100):
        articles = api.search(q=query, page=i, begin_date=begin_date, end_date=end_date)
        articles = parse_articles(articles)
        all_articles = all_articles + articles
        time.sleep(6)
    return all_articles


cur_country = 'Russia'
begin_date, end_date = 20180101, 20181231
country_year = get_articles(begin_date, end_date, cur_country)

keys = country_year[0].keys()
with open('./data/'+ cur_country.lower() +'-mentions2018.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(country_year)
