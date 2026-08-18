import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class Workflow:
    def __init__(self):
        self.steps = []
        self.current_step = 0
        self.context = {}
        
    def add_step(self, step_name, step_function):
        """Add a step to the workflow"""
        self.steps.append({
            'name': step_name,
            'function': step_function,
            'completed': False
        })
        
    def execute(self, initial_data=None):
        """Execute the workflow"""
        self.context['data'] = initial_data or {}
        self.context['start_time'] = datetime.utcnow().isoformat()
        
        for step in self.steps:
            try:
                result = step['function'](self.context)
                self.context[step['name']] = result
                step['completed'] = True
                self.current_step += 1
            except Exception as e:
                logger.error(f"Workflow step {step['name']} failed: {e}")
                return {
                    'error': f"Step {step['name']} failed: {str(e)}",
                    'completed_steps': self.current_step
                }
        
        self.context['end_time'] = datetime.utcnow().isoformat()
        return self.context
    
    def reset(self):
        """Reset the workflow"""
        self.steps = []
        self.current_step = 0
        self.context = {}
        
    def get_progress(self):
        """Get workflow progress"""
        total = len(self.steps)
        completed = sum(1 for s in self.steps if s['completed'])
        return {
            'total_steps': total,
            'completed_steps': completed,
            'progress': (completed / total * 100) if total > 0 else 0
        }