from datetime import datetime, timedelta
import json
import uuid
import logging

logger = logging.getLogger(__name__)

class MedicineReminder:
    def __init__(self):
        self.reminders = []
        
    def create_reminder(self, user_id, medicine_name, dosage, frequency, start_date, notes=''):
        """Create a medicine reminder"""
        try:
            reminder = {
                'id': str(uuid.uuid4())[:8],
                'user_id': user_id,
                'medicine_name': medicine_name,
                'dosage': dosage,
                'frequency': frequency,  # daily, twice_daily, weekly, etc.
                'start_date': start_date,
                'next_dose': self._calculate_next_dose(start_date, frequency),
                'notes': notes,
                'active': True,
                'created_at': datetime.utcnow().isoformat()
            }
            
            self.reminders.append(reminder)
            return reminder
            
        except Exception as e:
            logger.error(f"Create reminder error: {e}")
            return None
    
    def _calculate_next_dose(self, start_date, frequency):
        """Calculate next dose time"""
        start = datetime.fromisoformat(start_date) if isinstance(start_date, str) else start_date
        
        if frequency == 'daily':
            return (start + timedelta(days=1)).isoformat()
        elif frequency == 'twice_daily':
            return (start + timedelta(hours=12)).isoformat()
        elif frequency == 'weekly':
            return (start + timedelta(weeks=1)).isoformat()
        else:
            return start.isoformat()
    
    def get_reminders(self, user_id):
        """Get reminders for a user"""
        return [r for r in self.reminders if r['user_id'] == user_id and r['active']]
    
    def get_due_reminders(self, user_id=None):
        """Get reminders that are due"""
        now = datetime.utcnow()
        due = []
        
        reminders = self.reminders if not user_id else [r for r in self.reminders if r['user_id'] == user_id]
        
        for reminder in reminders:
            if not reminder['active']:
                continue
                
            next_dose = datetime.fromisoformat(reminder['next_dose'])
            if next_dose <= now:
                due.append(reminder)
                # Update next dose
                reminder['next_dose'] = self._calculate_next_dose(reminder['next_dose'], reminder['frequency'])
        
        return due
    
    def mark_taken(self, reminder_id):
        """Mark a reminder as taken"""
        for reminder in self.reminders:
            if reminder['id'] == reminder_id:
                reminder['last_taken'] = datetime.utcnow().isoformat()
                reminder['next_dose'] = self._calculate_next_dose(
                    datetime.utcnow(),
                    reminder['frequency']
                )
                return True
        return False
    
    def snooze_reminder(self, reminder_id, minutes=30):
        """Snooze a reminder"""
        for reminder in self.reminders:
            if reminder['id'] == reminder_id:
                next_dose = datetime.fromisoformat(reminder['next_dose'])
                reminder['next_dose'] = (next_dose + timedelta(minutes=minutes)).isoformat()
                return True
        return False
    
    def deactivate_reminder(self, reminder_id):
        """Deactivate a reminder"""
        for reminder in self.reminders:
            if reminder['id'] == reminder_id:
                reminder['active'] = False
                return True
        return False