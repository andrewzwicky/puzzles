import requests
from bs4 import BeautifulSoup
from session import SESSION
from pprint import pprint

PROBLEM_URL = "https://adventofcode.com/2020/day/{}"
INPUT_URL = PROBLEM_URL + "/input"
ANSWER_URL = PROBLEM_URL + "/answer"
ANSWER_PAYLOAD = {"level":"1", "answer":None}


def print_problem(day):
    problem_response = requests.get(PROBLEM_URL.format(day), cookies={"session":SESSION})
    problem_soup = BeautifulSoup(problem_response.content, "html.parser")
    
    problem_soup.header.decompose()

    for _tag in problem_soup.select(".share"):
        _tag.decompose()

    for _tag in problem_soup.select("#sponsor"):
        _tag.decompose()
        
    return str(problem_soup)

def get_problem_input(day):
    input_response = requests.get(INPUT_URL.format(day), cookies={"session":SESSION})
    
    raw_text = input_response.text
    cleaned_data = input_response.text.strip().split('\n')

    print("Raw Data:")
    print(repr(raw_text[:min(80, len(raw_text))]))
    
    print("Split Data:")
    if len(cleaned_data) != 0:
        pprint(cleaned_data[:min(10, len(cleaned_data))])
    
    else:
        cleaned_data = cleaned_data[0]
        pprint(cleaned_data[:min(80, len(cleaned_data))])
    
    return raw_text, cleaned_data
    
def submit_answer(day, level, answer):
    if answer is None:
        return False
    pprint(answer)
    answer_response = requests.post(
        url=ANSWER_URL.format(day),
        cookies={"session":SESSION},
        data={"level": level, "answer": answer},
    )

    answer_soup = BeautifulSoup(answer_response.text, "html.parser")
    
    message = answer_soup.article.text
    pprint(message)
    if "That's the right answer" in message:
        return True
    else:
        return False
    