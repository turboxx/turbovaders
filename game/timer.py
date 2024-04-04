import time


class Timer:
    def __init__(self):
        self.time_started = None
        self.time_started_real = None
        self.time_paused = None
        self.time_stopped = None
        self.paused = False
        self.stopped = False

    def start(self):
        if self.stopped:
            return
        if self.time_started:
            return

        self.time_started = time.perf_counter()
        self.time_started_real = time.perf_counter()

    def pause(self):
        if self.stopped:
            return
        if not self.time_started or self.paused:
            return

        self.time_paused = time.perf_counter()
        self.paused = True

    def resume(self):
        if self.stopped:
            return

        if not self.time_started or not self.time_paused or not self.paused:
            return
        pause_time = time.perf_counter() - self.time_paused
        self.time_started = self.time_started + pause_time
        self.paused = False

    def stop(self):
        if self.stopped:
            return

        self.time_stopped = time.perf_counter()
        self.stopped = True

    def get(self, digits=1):
        if not self.time_started:
            return round(0, digits)

        if self.paused:
            return round(self.time_paused - self.time_started, digits)

        if self.stopped:
            return round(self.time_stopped - self.time_started, digits)

        return round(time.perf_counter() - self.time_started, digits)
