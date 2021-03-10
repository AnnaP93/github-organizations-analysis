# Github Organizations Analysis

### Program Objective

Call organizations from GitHub repositories and see their total number of stars, forks and the average number of issues.

### Description & Requirements

It is a command-line program that returns aggregated GitHub stats for the requested organization's repository. It requires the Python interpreter, version 3.2+, SQLite database, and Personal Access Token (PAT) from GitHub. More information about creating PAT can be found here - https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token

Please note that the program is using a virtual environment (venv) which settings might be found in the `requirements.txt`.


#####  Passing Personal Access Token via environment variables

To keep the PAT secure, it is passed via `.env` file:

1) Create `token.env` file and set a PAT to a variable named "GITHUB_API_TOKEN" 
2) Add `token.env` to `.gitignore` to keep the PAT secure.


##### Connecting to SQLite database

The program is configured to connect with _github_companies_analysis.db_ SQLite database that is included in the project repository. This database can be used for retrieving GitHub organization(s) repositories' stats, or the new SQLite database can be created if needed.

### How the program works?

In the command-line interface call `python` `main.py` and the name(s) of the organization(s), keeping **one space between the entries**. It should be noted that the call time is recorded. Thus, if the same organization is requested within less than a week - the previously-recorded stats will show up. However, if the same organization is called after one week from the previous request - the new stats and record time will be generated.


### Input Example

`python` `main.py` `python` `freecodecamp`

### Output Example

_For the first entry:_

- organization: python
- total_number_of_stars: 56639.0 
- total_number_of_forks: 23848.0 
- average_number_of_issues: 54.4  
- record_time: 2021-01-18 18:22:37.598955


_For the second entry:_

- organization: freecodecamp
- total_number_of_stars: 359942.0
- total_number_of_forks: 42075.0
- average_number_of_issues: 9.1  
- record_time: 2021-01-18 2021-01-19 00:05:00.916054




