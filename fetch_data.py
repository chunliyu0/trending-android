import requests
from bs4 import BeautifulSoup
import urllib
from stackoverflow.items import  StackoverflowItem

def parse_question_detail_page(detail_url):
    detail_page = requests.get(detail_url)
    q_item = StackoverflowItem()
    if detail_page.status_code == 200:
        detail = BeautifulSoup(detail_page.content, 'html.parser')
        q_item['question_title'] = detail.select('.question-hyperlink')[0].get_text()[4:]

        # question_title = str(detail.select('.post-text')[0])
        # question_tags =

def parse_question_list_page(url):
    site = requests.get(url)
    top_questions = []
    if site.status_code == 200:
        content = BeautifulSoup(site.content, 'html.parser')
        questions = content.select('.question-summary')[0:10:1]
        for question in questions:
            q_item = StackoverflowItem()
            excerpt = question.select('.excerpt')[0].get_text()
            print(f'excerpt: {excerpt}')
            tags_ = question.select('.tags a')
            tags = []
            for tag_ in tags_:
                tags.append(tag_.get_text())
            print(f'tags:{tags}')

            detail_url = urllib.parse.urljoin('https://stackoverflow.com',
                                      question.select('.question-hyperlink')[0].get('href'))
            # q_item = parse_question_detail_page(detail_url)
            q_item['links'] = detail_url
            q_item['question_title'] = question.select('.question-hyperlink')[0].get_text()[4:]
            q_item['question_excerpt'] = excerpt
            q_item['tags'] = tags
            q_item['asked_time'] = question.find(class_='started fr').select('.relativetime')[0].get_text()
            q_item['votes'] =  question.select('.votes')[0].find(class_='vote-count-post').get_text()
            top_questions.append(q_item)
            print(f'q_item: {q_item["question_title"]}')
    else:
        print('failed parsing url!')
    return top_questions

def fetch_10_top_questions():
    """
    url: https://stackoverflow.com/search?tab=newest&q=[android]+duplicate:no
    :param
    :return:
    """
    base_url = 'https://stackoverflow.com/'
    newest_search_query = 'search?tab=newest&q=[android]+duplicate:no'
    most_voted_search_query = 'search?tab=votes&q=[android]+duplicate:no+created:7d..'
    newest_questions = parse_question_list_page(base_url+newest_search_query)
    most_voted_questions =parse_question_list_page(base_url+most_voted_search_query)
    data = {'newest_questions': newest_questions,'most_voted_questions':most_voted_questions}
    return data

def fetch_10_newest():
    base_url = 'https://stackoverflow.com/search?tab=newest&q=[android]+duplicate:no+created:7d..'
    site = requests.get(base_url)
    newest_questions = []
    if site.status_code == 200:
        content = BeautifulSoup(site.content,'html.parser')
        questions = content.select('.question-summary')[0:10:1]

        for question in questions:
            q_item = StackoverflowItem()
            q_item['question_title'] = question.select('.question-hyperlink')[0].get_text()
            q_item['asked_time'] = question.find(class_='started fr').select('.relativetime')[0].get_text()
            newest_questions.append(q_item)
            print(f'q_item: {q_item["question_title"]}')
    else:
        print('failed fetching 10 newest questions on Android')
    return newest_questions

def fetch_10_popular():
    pass



