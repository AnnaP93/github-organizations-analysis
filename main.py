from typing import Type

import requests
import os
from dotenv import load_dotenv
import sys
from prettytable import PrettyTable


def print_all_repositories_data(organization):
    all_info = []
    url = 'https://api.github.com/search/repositories'

    #print('Repositories in the organization - URL:', response.url)
    #print("Repositories in the organization - status:", response.status_code)

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

    stars_in_all_repositories = __aggregate_stars(all_info)
    print("Aggregated number of stars across all repositories in ", organization, 'is', stars_in_all_repositories)

    forks_in_all_repositories = __aggregate_forks(all_info)
    print("Aggregated number of forks across all repositories in ", organization, 'is', forks_in_all_repositories)

    average_issues_in_all_repositories = __aggregate_number_of_issues(all_info)
    print("Aggregated number of issues across all repositories in ", organization, 'is', average_issues_in_all_repositories)

    all_repository_stats = [organization, stars_in_all_repositories, forks_in_all_repositories, average_issues_in_all_repositories]
    print(all_repository_stats)

    repository_stats_table: PrettyTable = PrettyTable()
    repository_stats_table.field_names = ["Organization", "Total Number of Stars", "Total Number of Forks", "Average Number of Issues"]
    repository_stats_table.add_row([organization, stars_in_all_repositories, forks_in_all_repositories, average_issues_in_all_repositories])
    print(repository_stats_table)


def get_aggregated_data(organization):
    headers = {'Accept': 'application/vnd.github.v3+json', "Authorization": "token " + os.environ.get('GITHUB_API_TOKEN')}
    url = 'https://api.github.com/search/repositories'
    all_repositories_stars_count = 0
    all_repositories_forks_count = 0
    all_repositories_issues_total = 0
    all_repositories_issues_count = 0

    while url:
        repositories_in_organization = requests.get(url=url, headers=headers,
                                                    params={'q': 'org:'+organization})
        # print('Repositories in the organization - URL:', repositories_in_organization.url)
        # print("Repositories in the organization - status:", repositories_in_organization.status_code)
        response_links = repositories_in_organization.links

        items_json = repositories_in_organization.json()['items']

        stars_count = __aggregate_stars(items_json)
        all_repositories_stars_count += stars_count

        forks_count = __aggregate_forks(items_json)
        all_repositories_forks_count += forks_count

        average_issues = __aggregate_number_of_issues(items_json)
        all_repositories_issues_total += average_issues[0]
        all_repositories_issues_count += average_issues[1]

        if 'next' in response_links:
            url = repositories_in_organization.links['next']['url']
        else:
            break
    print('Stars count equals ', all_repositories_stars_count, 'in', organization)
    print('Forks count equals ', all_repositories_forks_count, 'in', organization)
    print('Average number of issues (together with pull requests) equals ',
          round(all_repositories_issues_total/all_repositories_issues_count, 1), 'in', organization)


def __get_api_response(url, organization):
    headers = {'Accept': 'application/vnd.github.v3+json', "Authorization": "token " + os.environ.get('GITHUB_API_TOKEN')}
    repositories_in_organization = requests.get(url=url, headers=headers,
                                                params={'q': 'org:' + organization})
    return repositories_in_organization


def __aggregate_stars(repository_items):
    return sum(map(lambda repository: repository['stargazers_count'], repository_items))


def __aggregate_forks(repository_items):
    return sum(map(lambda repository: repository['forks_count'], repository_items))


def __aggregate_number_of_issues(repository_items):
    return sum((map(lambda repository: repository['open_issues_count'], repository_items)))/len(repository_items)


# get_aggregated_data(sys.argv[1])
if __name__ == "__main__":
    # Credentials
    load_dotenv('token.env')
    # get_all_repositories_data(sys.argv[1])
    print_all_repositories_data('automapper')
    # get_aggregated_data(sys.argv[1])
