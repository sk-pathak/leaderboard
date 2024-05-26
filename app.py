from flask import Flask, jsonify, render_template
import requests
import json

app = Flask(__name__)

# Function to fetch data from GitHub API
def fetch_pull_request_data(pull_request_id):
    url = f"https://api.github.com/repos/sk-pathak/GitStartedWithUs/pulls/{pull_request_id}"
    response = requests.get(url)
    return response.json()

# Function to update user points
def update_user_points(user_data, points):
    if 'points' in user_data:
        user_data['points'] += points
    else:
        user_data['points'] = points
    return user_data

# Main function to process pull requests
def process_pull_requests():
    pull_request_id = 1
    all_data = {}

    while True:
        pull_request_data = fetch_pull_request_data(pull_request_id)
        length=len(pull_request_data)
        
        if length == 2:
            break
        is_merged = False
        try:
            is_merged = pull_request_data['merged']
        except:
            print("Pull request not found")
        if is_merged and pull_request_data['state'] == "closed":
            user_login = pull_request_data['user']['login']
            points = 1
            if user_login in all_data:
                all_data[user_login] = update_user_points(all_data[user_login], points)
            else:
                all_data[user_login] = update_user_points({}, points)
        
        pull_request_id += 1

    sorted_data = dict(sorted(all_data.items(), key=lambda item: item[1]['points'], reverse=True))
    with open('data.json', 'w') as json_file:
        json.dump(all_data, json_file, indent=4)

    return sorted_data

@app.route('/')
def index():
    data = process_pull_requests()
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
