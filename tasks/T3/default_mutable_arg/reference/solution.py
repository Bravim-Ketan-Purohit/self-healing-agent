class Logger:
    def __init__(self):
        self.entries = []

    def log(self, msg: str, tags: list[str] | None = None) -> dict:
        """Create a log entry. Each entry gets its own independent tags list."""
        if tags is None:
            tags = []
        else:
            tags = tags.copy()
        entry = {"msg": msg, "tags": tags}
        self.entries.append(entry)
        return entry
