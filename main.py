import requests

def get_most_used_function(repo_owner, repo_name):
    # Make a GET request to the GitHub API to get the repository contents
    response = requests.get(f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents")

    if response.status_code == 200:
        # Get the list of files in the repository
        files = response.json()

        # Dictionary to store the count of each function
        function_counts = {}

        # Iterate over each file in the repository
        for file in files:
            # Make a GET request to get the file contents
            if file['download_url'] is None:
                continue
            file_response = requests.get(file['download_url'])

            if file_response.status_code == 200:
                # Read the file contents
                file_contents = file_response.text

                # Split the file contents into lines
                lines = file_contents.split('\n')

                # Iterate over each line in the file
                for line in lines:
                    # Check if the line contains a function definition
                    if line.startswith('def '):
                        # Get the function name
                        function_name = line.split(' ')[1].split('(')[0]

                        # Increment the count of the function in the dictionary
                        function_counts[function_name] = function_counts.get(function_name, 0) + 1

        # Get the most used function
        most_used_function = max(function_counts, key=function_counts.get)

        return most_used_function

    else:
        # Handle the case when the repository is not found or the API request fails
        return None

# Example usage
repo_owner = "cardze"
repo_name = "todo_list-django"
most_used_function = get_most_used_function(repo_owner, repo_name)
print(f"The most used function in the {repo_owner}/{repo_name} repository is: {most_used_function}")