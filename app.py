import requests
from datetime import datetime
from flask import Flask , render_template , request
app = Flask(__name__)

def calculate_grit(active_days, total_days):
    if total_days == 0:
        return 0, "No data" , "No Badge"
    ratio = active_days / total_days 
    percentage = round(ratio*100,2)
    if ratio >= 0.7:
        level = "High consistency" 
        badge = "Gold Grit Badge 🥇"
    elif ratio >=0.4:
        level= "Medium Consistency" 
        badge = "Silver Grit Badge 🥈"
    else: 
        level = "Low Consistency" 
        badge = "Bronze Grit Badge 🥉"
    return percentage, level,badge
    
@app.route("/", methods=["GET","POST"])
def home():
    percentage = None
    level = None
    badge = None
    if request.method == "POST":
        active_days = int(request.form["active_days"])
        total_days = int(request.form["total_days"])

        percentage, level, badge = calculate_grit(active_days, total_days)

    return render_template("index.html" , percentage=percentage, level=level, badge=badge)
@app.route("/github", methods=["POST"])
def github():
    username = request.form["username"]
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url)

    if response.status_code != 200:
        return "GitHub user not found"

    events = response.json()

    commit_days = set()
    for event in events:
        if event["type"] == "PushEvent":
            date = event["created_at"][:10]
            commit_days.add(date)
    active_days = len(commit_days)
    total_days = 30
    date_objects = [
        datetime.strptime(d, "%Y-%m-%d")
        for d in commit_days
    ]
    date_objects.sort(reverse=True)
    current_streak = 0
    if date_objects:
        current_streak = 1
        for i in range(len(date_objects) - 1):
            diff = (date_objects[i] - date_objects[i+1]).days
            if diff==1:
                current_streak +=1
            else:
                break
    percentage,level, badge = calculate_grit(active_days, total_days)
    return render_template("recruiter.html", percentage= percentage, level= level,badge= badge, active_days=active_days,current_streak=current_streak)
if __name__ == "__main__":
    app.run(debug=True, port=5001)
