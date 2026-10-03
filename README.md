# 🗓️ ConflictFree Engine 
**Intelligent Constraint Satisfaction Event Scheduler**

An advanced hackathon prototype that completely automates college event scheduling using a powerful CSP (Constraint Satisfaction Problem) backtracking engine. It eliminates venue clashes, faculty double-booking, and resource constraints instantly.

## 🚀 Core Features (Hackathon Highlights)
- **True CSP Backtracking with MRV:** Replaces basic "First-Come-First-Serve" with the Minimum Remaining Values heuristic. It prioritizes heavily constrained events (like Mega Events) and uses "Best Fit" logic to map small classes to small rooms, preserving the Main Auditorium.
- **Predictive Auto-Detect UI:** The frontend intelligently auto-selects required equipment (Projectors, PA Systems, Stage Lighting) and event types simply based on the keywords typed into the Event Name.
- **Strict Constraint Validation:** Actively prevents venue double-booking, ensures faculty coordinators aren't scheduled in two places at once, and strictly validates classroom capacity against expected participant counts.
- **Bulk Data Import:** Built-in HTML5 File Reader to instantly parse and schedule massive amounts of events via `.csv` upload.
- **Impossible State Handling:** If a schedule is mathematically impossible, the engine outputs actionable conflict resolution advice rather than failing silently.

## 💻 Tech Stack
- **Backend Core:** Python, Flask
- **Frontend UI:** HTML5, Bootstrap 5, Vanilla JavaScript
- **Algorithm Architecture:** Custom CSP Backtracking, MRV Sorting, Forward Checking

## 🛠️ How to Run Locally (For Jury & Evaluators)
1. On this repository page, click the green **`<> Code`** button and select **Download ZIP**.
2. Extract the folder and open it in your terminal or VS Code.
3. Install Flask (if not already installed):
   ```bash
   pip install flask
