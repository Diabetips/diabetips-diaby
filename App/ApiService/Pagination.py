class Pagination:
    def __init__(self,
                 size,
                 default,
                 current=-1,
                 previous=-1,
                 next=-1,
                 last=-1,
                 start=0,
                 end=0):
        self.periodEnable = start + end > 0
        self.size = size
        self.default = default
        self.current = default if current == -1 else current
        self.previous = default if previous == -1 else previous
        self.next = default if next == -1 else next
        self.last = default if last == -1 else last
        self.start = start
        self.end = end
        self.updated = False

    def reset(self):
        self.current = self.default
        self.previous = self.default
        self.next = self.default
        self.last = self.default
        self.updated = False

    def is_first(self):
        return self.current <= self.previous

    def is_last(self):
        return self.current >= self.last & self.updated

    def next_page(self):
        self.current = self.next

    def last_page(self):
        self.current = self.previous

    def getRequestParameters(self):
        self.updated = True
        if self.periodEnable:
            return f"page={self.current}&size={self.size}&start={int(self.start)}&end={int(self.end)}"
        return f"page={self.current}&size={self.size}"

    def setInterval(self, start, end):
        self.start = start
        self.end = end
        self.periodEnable = True

    def updateFromHeader(self, header):
        if header is None:
            return
        if header["previous"] is not None:
            self.previous = int(header["previous"])
        if header["next"] is not None:
            self.next = int(header["next"])
        if header["last"] is not None:
            self.last = int(header["last"])
