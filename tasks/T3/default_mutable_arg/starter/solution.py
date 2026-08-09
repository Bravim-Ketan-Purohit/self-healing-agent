class Logger:
    def __init__(self):
        self.entries = []

    def log(self, msg: str, tags: list[str] | None = None) -> dict:
        """Create a log entry with msg and tags. Returns the entry dict."""
        pass
