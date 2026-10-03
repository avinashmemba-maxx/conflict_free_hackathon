from flask import Flask, render_template, request, jsonify
from scheduler import generate_schedule

app = Flask(__name__)

@app.route('/')
def home():
    # Serves the frontend interface
    return render_template('index.html')

@app.route('/api/schedule', methods=['POST'])
def schedule_events():
    # 1. Receive data from the frontend
    data = request.json
    events = data.get('events', [])
    venues = data.get('venues', [])
    
    # 2. Pass to your backtracking solver
    # This will handle the O((V x T)^E) complexity and MRV heuristics
    result = generate_schedule(events, venues)
    
    # 3. Return the clash-free schedule or a failure report
    if result['success']:
        return jsonify({"status": "success", "schedule": result['data']})
    else:
        return jsonify({"status": "error", "message": "No feasible schedule exists. Please relax constraints."})

if __name__ == '__main__':
    app.run(debug=True)