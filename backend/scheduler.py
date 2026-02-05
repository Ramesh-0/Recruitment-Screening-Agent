"""
Interview Scheduler
Manages interview scheduling and calendar integration
"""

from datetime import datetime, timedelta
import json

# In-memory storage (in production, use database)
scheduled_interviews = []


def schedule_interview(candidate_name, candidate_email, date, time, interview_type="Technical", duration_minutes=60):
    """
    Schedule an interview for a candidate
    
    Args:
        candidate_name: Candidate's full name
        candidate_email: Candidate's email
        date: Interview date (YYYY-MM-DD)
        time: Interview time (HH:MM)
        interview_type: Type of interview (Technical, Behavioral, etc.)
        duration_minutes: Interview duration in minutes
    
    Returns:
        Interview details with confirmation
    """
    
    try:
        # Parse datetime
        interview_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        end_datetime = interview_datetime + timedelta(minutes=duration_minutes)
        
        # Check for conflicts
        conflicts = check_scheduling_conflicts(interview_datetime, end_datetime)
        if conflicts:
            return {
                'success': False,
                'message': 'Time slot already booked',
                'conflicts': conflicts
            }
        
        # Create interview record
        interview = {
            'id': len(scheduled_interviews) + 1,
            'candidate_name': candidate_name,
            'candidate_email': candidate_email,
            'interview_type': interview_type,
            'start_time': interview_datetime.isoformat(),
            'end_time': end_datetime.isoformat(),
            'duration_minutes': duration_minutes,
            'status': 'scheduled',
            'scheduled_at': datetime.now().isoformat(),
            'meeting_link': generate_meeting_link(),
            'interviewer': 'TBD'
        }
        
        scheduled_interviews.append(interview)
        
        return {
            'success': True,
            'message': f"Interview scheduled successfully for {candidate_name}",
            'interview': interview,
            'calendar_invite': generate_calendar_invite(interview)
        }
        
    except ValueError as e:
        return {
            'success': False,
            'message': f'Invalid date/time format: {e}'
        }


def check_scheduling_conflicts(start_time, end_time):
    """Check if time slot conflicts with existing interviews"""
    conflicts = []
    
    for interview in scheduled_interviews:
        existing_start = datetime.fromisoformat(interview['start_time'])
        existing_end = datetime.fromisoformat(interview['end_time'])
        
        # Check for overlap
        if (start_time < existing_end and end_time > existing_start):
            conflicts.append({
                'candidate': interview['candidate_name'],
                'time': interview['start_time']
            })
    
    return conflicts


def generate_meeting_link():
    """Generate placeholder meeting link (integrate with Zoom/Teams in production)"""
    import random
    import string
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return f"https://meet.company.com/{code}"


def generate_calendar_invite(interview):
    """Generate calendar invite details"""
    start = datetime.fromisoformat(interview['start_time'])
    
    return {
        'title': f"{interview['interview_type']} Interview - {interview['candidate_name']}",
        'description': f"Interview with {interview['candidate_name']}\nType: {interview['interview_type']}\nMeeting Link: {interview['meeting_link']}",
        'start_time': interview['start_time'],
        'end_time': interview['end_time'],
        'location': interview['meeting_link']
    }


def get_available_slots(date, interview_type="Technical"):
    """Get available interview slots for a given date"""
    target_date = datetime.strptime(date, "%Y-%m-%d").date()
    
    # Standard interview hours: 9 AM - 5 PM
    working_hours = [
        "09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00"
    ]
    
    available_slots = []
    
    for time_slot in working_hours:
        slot_datetime = datetime.strptime(f"{date} {time_slot}", "%Y-%m-%d %H:%M")
        slot_end = slot_datetime + timedelta(hours=1)
        
        # Check if slot is available
        conflicts = check_scheduling_conflicts(slot_datetime, slot_end)
        
        if not conflicts:
            available_slots.append({
                'time': time_slot,
                'datetime': slot_datetime.isoformat(),
                'available': True
            })
    
    return available_slots


def cancel_interview(interview_id, reason=""):
    """Cancel a scheduled interview"""
    for interview in scheduled_interviews:
        if interview['id'] == interview_id:
            interview['status'] = 'cancelled'
            interview['cancellation_reason'] = reason
            interview['cancelled_at'] = datetime.now().isoformat()
            
            return {
                'success': True,
                'message': f"Interview {interview_id} cancelled successfully",
                'interview': interview
            }
    
    return {
        'success': False,
        'message': f'Interview {interview_id} not found'
    }


def get_scheduled_interviews(date=None):
    """Get all scheduled interviews, optionally filtered by date"""
    if date:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
        return [
            interview for interview in scheduled_interviews
            if datetime.fromisoformat(interview['start_time']).date() == target_date
            and interview['status'] == 'scheduled'
        ]
    
    return [i for i in scheduled_interviews if i['status'] == 'scheduled']

