# Agents/__init__.py
"""
Smart Crop AI - Multi-Agent System
Agricultural Intelligence Platform
"""

__version__ = "1.0.0"
__author__ = "Team TechTribe"

# Import all agent functions for easier access
try:
    from .crop_advisor import get_crop_advice
    from .market_broker import get_market_broker_response
    from .crop_disease_detector import analyze_crop_image
    from .alert_agent import check_disease_alert, collect_user_report
    
    __all__ = [
        'get_crop_advice',
        'get_market_broker_response', 
        'analyze_crop_image',
        'check_disease_alert',
        'collect_user_report'
    ]
except ImportError as e:
    print(f"Warning: Could not import some agents: {e}")
    __all__ = []