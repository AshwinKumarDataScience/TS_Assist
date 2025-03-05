from flask import Flask, request, render_template
import csv

app = Flask(__name__)

# Load data from issues.csv
def load_issues():
    with open('issues.csv', 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

# Rule-based troubleshooting for new issues
NEW_ISSUE_TROUBLESHOOTING = {
    "overheating": "1. Turn off the headset and let it cool for 10 minutes.\n2. Check for obstructions or debris.\n3. Ensure proper ventilation and avoid high temperatures.\n4. Update firmware if available.",
    "battery draining quickly": "1. Check battery level and charge fully.\n2. Ensure no background apps are draining power.\n3. Update firmware or software.\n4. Contact support if issue persists.",
    "connection drops": "1. Restart the headset and device.\n2. Ensure Bluetooth is enabled and stable.\n3. Move away from interference (e.g., Wi-Fi routers).\n4. Re-pair the device."
}

# Generate troubleshooting steps for new issues using rules
def generate_troubleshooting(query):
    query_lower = query.lower()
    for keyword, steps in NEW_ISSUE_TROUBLESHOOTING.items():
        if keyword in query_lower:
            return steps
    return "1. Restart the device and system.\n2. Check for software updates.\n3. Verify hardware connections.\n4. Escalate to support if unresolved."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query'].lower()
        issues = load_issues()
        # Search for matches in Keywords
        matches = [issue for issue in issues if any(keyword in query for keyword in issue['Keywords'].lower().split())]
        if matches:
            return render_template('results.html', matches=matches)
        else:
            # Generate troubleshooting steps for new issues
            troubleshooting = generate_troubleshooting(query)
            return render_template('no_match.html', query=query, troubleshooting=troubleshooting)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)