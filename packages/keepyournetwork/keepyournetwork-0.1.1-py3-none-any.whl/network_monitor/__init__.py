"""
KeepYourNetwork - A powerful network monitoring and analysis tool

This package provides real-time network traffic monitoring, bandwidth analysis,
and system statistics through a beautiful terminal user interface.

Features:
- Real-time network speed monitoring
- Bandwidth usage analysis
- Packet statistics and error tracking
- Session information and summaries
- Beautiful and intuitive terminal UI

For more information, visit:
https://github.com/HFerrahoglu/KeepYourNetwork
"""

__version__ = "0.1.1"
__author__ = "Hamza Ferrahoğlu"
__email__ = "hamzaferrahoglu@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright 2024 Hamza Ferrahoğlu"

from .monitor import NetworkMonitor

__all__ = ["NetworkMonitor"] 