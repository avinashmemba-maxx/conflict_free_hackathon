from datetime import datetime, timedelta

def generate_venues():
    venues = [{"name": "Main Auditorium", "capacity": 1000, "type": "auditorium", "equipment": ["Projector", "High-Power PA System", "Stage Lighting"]}]
    for block in ['A', 'B', 'C']:
        for floor in range(1, 5):
            for room in range(1, 6):
                venues.append({
                    "name": f"{block}-{floor}0{room}",
                    "capacity": 60, 
                    "type": "classroom",
                    "equipment": ["Projector"] # Classrooms don't have Stage Lighting
                })
    # BEST FIT HEURISTIC: Sort venues by capacity ASCENDING so small events fill small rooms first
    return sorted(venues, key=lambda v: v['capacity'])

def check_constraints(assignment, event, venue, test_date, test_time):
    # 1. Mega events MUST be in the Auditorium
    if event.get('is_mega') and venue['type'] != 'auditorium': return False
        
    # 2. Capacity check
    if venue['capacity'] < int(event['participants']): return False
        
    # 3. Equipment check (Does the venue have everything the event needs?)
    for eq in event.get('equipment', []):
        if eq not in venue['equipment']: return False
            
    for assigned in assignment:
        # 4. Venue double-booking check
        if assigned['venue'] == venue['name'] and assigned['date'] == test_date and assigned['time'] == test_time:
            return False
        # 5. Faculty Coordinator double-booking check!
        if assigned['coordinator'] == event['coordinator'] and assigned['date'] == test_date and assigned['time'] == test_time:
            return False
            
    return True

def backtrack(assignment, unassigned_events, venues, available_dates, time_slots):
    if not unassigned_events: return assignment 
        
    # MRV HEURISTIC (Minimum Remaining Values)
    # Sort by Mega Events first, then by Participant Count (descending). 
    # This schedules the hardest events first to prevent dead-ends later.
    unassigned_events = sorted(unassigned_events, key=lambda x: (not x.get('is_mega'), -int(x['participants'])))
    
    current = unassigned_events[0]
    pref_date = current['date']
    pref_time = current['time']
    
    # ATTEMPT 1: Exact Date & Time
    for venue in venues:
        if check_constraints(assignment, current, venue, pref_date, pref_time):
            new_assign = list(assignment)
            new_assign.append({**current, "venue": venue['name'], "status": "Success", "message": "Preferred slot secured."})
            res = backtrack(new_assign, unassigned_events[1:], venues, available_dates, time_slots)
            if res: return res

    # ATTEMPT 2: Same Date, Different Time
    for time_slot in time_slots:
        if time_slot == pref_time: continue
        for venue in venues:
            if check_constraints(assignment, current, venue, pref_date, time_slot):
                new_assign = list(assignment)
                new_assign.append({**current, "venue": venue['name'], "time": time_slot, "status": "Moved", "message": f"Time clash resolved. Shifted to {time_slot}."})
                res = backtrack(new_assign, unassigned_events[1:], venues, available_dates, time_slots)
                if res: return res

    # ATTEMPT 3: Completely Different Date
    for date in available_dates:
        if date == pref_date: continue
        for time_slot in time_slots:
            for venue in venues:
                if check_constraints(assignment, current, venue, date, time_slot):
                    new_assign = list(assignment)
                    new_assign.append({**current, "venue": venue['name'], "date": date, "time": time_slot, "status": "Moved", "message": f"Full day clash! Moved to {date}."})
                    res = backtrack(new_assign, unassigned_events[1:], venues, available_dates, time_slots)
                    if res: return res

    return None # Triggers backtracking

def generate_schedule(events, _):
    venues = generate_venues()
    time_slots = ["09:30 AM - 11:00 AM", "11:00 AM - 12:30 PM", "01:00 PM - 02:30 PM", "02:30 PM - 04:00 PM"]
    
    unique_dates = set(e['date'] for e in events if e.get('date'))
    if unique_dates:
        last_dt = datetime.strptime(max(unique_dates), "%Y-%m-%d")
        unique_dates.add((last_dt + timedelta(days=1)).strftime("%Y-%m-%d"))
    available_dates = sorted(list(unique_dates))
    
    final_schedule = backtrack([], events, venues, available_dates, time_slots)
    
    if final_schedule is not None:
        return {"success": True, "data": final_schedule}
    else:
        # Edge Case & Impossible State Handling
        return {"success": False, "message": "CRITICAL CONFLICT: Impossible State Reached. The Auditorium is fully booked across all available windows, or Faculty are double-booked. Suggest adding an extra date."}
