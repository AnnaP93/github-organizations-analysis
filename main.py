import requests
import json
import os
from dotenv import load_dotenv
import sys

# Credentials
load_dotenv('token.env')


def get_aggregated_data(organization):
    headers = {'Accept': 'application/vnd.github.v3+json', "Authorization": "token " + os.environ.get('GITHUB_API_TOKEN')}

    repositories_in_organization = requests.get('https://api.github.com/search/repositories', headers=headers,
                                                params={'q': 'org:'+organization})
    print('Repositories in the organization - URL:', repositories_in_organization.url)
    print("Repositories in the organization - status:", repositories_in_organization.status_code)
    items_json = repositories_in_organization.json()['items']
    print(json.dumps(repositories_in_organization.json()['items'], indent=4, sort_keys=True))

    stars_count = __aggregate_stars(items_json)
    print('The sum of all stars in', organization, 'equals', stars_count)

    forks_count = __aggregate_forks(items_json)
    print('The sum of all forks in', organization, 'equals', forks_count)

    average_issues = __average_number_of_issues(items_json)
    print('The average number of issues for ', organization, 'equals', average_issues)


def __aggregate_stars(repository_items):
    stargazers_count = 0
    for item in repository_items:
        stargazers_count = stargazers_count + item['stargazers_count']
    return stargazers_count


def __aggregate_forks(repository_items):
    forks_count = 0
    for item in repository_items:
        forks_count = forks_count + item['forks_count']
    return forks_count


def __average_number_of_issues(repository_items):
    issues_total = 0
    issues_count = 0
    for item in repository_items:
        issues_total = issues_total + item['open_issues_count']
        issues_count += 1
    return issues_total/issues_count


get_aggregated_data(sys.argv[1])
