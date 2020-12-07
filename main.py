import requests
import os
from dotenv import load_dotenv
import sys
from prettytable import PrettyTable
from sqlite_git_organizations_demo import __fill_organizations_table
from sqlite_git_organizations_demo import __return_complete_table
import datetime


def get_all_repositories_data(organization):
    all_info = []
    url = 'https://api.github.com/search/repositories'
    is_final_page = False
    while not is_final_page:
        response = __get_api_response(url, organization)
        convert_to_json = response.json()['items']
        for item in convert_to_json:
            all_info.append(item)
        if 'next' in response.links:
            next_url = response.links['next']['url']
            url = next_url
            is_final_page = False
        else:
            is_final_page = True

    stars_in_all_repositories = sum(map(lambda repository: repository['stargazers_count'], all_info))
    forks_in_all_repositories = sum(map(lambda repository: repository['forks_count'], all_info))
    average_issues_in_all_repositories = round(sum((map(lambda repository: repository['open_issues_count'],
                                                        all_info)))/len(all_info), 1)
    time_of_record = datetime.datetime.now()
    all_repository_stats = [organization, stars_in_all_repositories, forks_in_all_repositories,
                            average_issues_in_all_repositories, time_of_record]
    return all_repository_stats


def __get_api_response(url, company):
    headers = {'Accept': 'application/vnd.github.v3+json', "Authorization": "token " + os.environ.get('GITHUB_API_TOKEN')}
    repositories_in_organization = requests.get(url=url, headers=headers,
                                                params={'q': 'org:' + company})
    return repositories_in_organization


if __name__ == "__main__":
    # Credentials
    load_dotenv('token.env')

    organizations = sys.argv[1:]
    for single_company in organizations:
        single_company_stats = get_all_repositories_data(single_company)
        # inserting_data_into_database = __fill_organizations_table(single_company_stats)
        complete_table = __return_complete_table()

    print(complete_table)

