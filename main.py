import requests
import os
from dotenv import load_dotenv
import sys
from prettytable import PrettyTable


def get_all_repositories_data(organization):
    all_info = []
    url = 'https://api.github.com/search/repositories'
    is_final_page = False
    while not is_final_page:
        response = __get_api_response(url, organization)
        for item in response.json()['items']:
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
    all_repository_stats = [organization, stars_in_all_repositories, forks_in_all_repositories,
                            average_issues_in_all_repositories]
    return all_repository_stats


def __get_api_response(url, company):
    headers = {'Accept': 'application/vnd.github.v3+json', "Authorization": "token " + os.environ.get('GITHUB_API_TOKEN')}
    repositories_in_organization = requests.get(url=url, headers=headers,
                                                params={'q': 'org:' + company})
    return repositories_in_organization


if __name__ == "__main__":
    # Credentials
    load_dotenv('token.env')

    repository_stats_table: PrettyTable = PrettyTable()
    repository_stats_table.field_names = ["Organization", "Total Number of Stars", "Total Number of Forks",
                                          "Average Number of Issues"]
    organizations = sys.argv[1:]
    for single_company in organizations:
        single_company_stats = get_all_repositories_data(single_company)
        repository_stats_table.add_row(single_company_stats)
    print(repository_stats_table)

