"""
Tracks file size during streaming XML writes.
"""

class SizeMonitor:
    def __init__(self, max_bytes):
        self.max_bytes = max_bytes
        self.current = 0

    def add(self, data):
        self.current += len(data)

    def would_exceed(self, data):
        return self.current + len(data) > self.max_bytes

    def reset(self):
        self.current = 0
