import os
import csv
import time
import threading
from datetime import datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, "data")
CSV_PATH = os.path.join(DATA_DIR, "sessions.csv")

DEFAULT_FOCUS = 25
DEFAULT_SHORT = 5
DEFAULT_LONG = 15

def make_data_folder():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def setup_csv():
    make_data_folder()
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id", "type", "start", "end", "seconds", "notes"])

def add_session(row):
    setup_csv()
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(row)

def read_sessions():
    if not os.path.exists(CSV_PATH):
        return []
    out = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            out.append(row)
    return out

def format_time(sec):
    m, s = divmod(int(sec), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h}h {m}m {s}s"
    return f"{m}m {s}s"

class Timer:
    def __init__(self, seconds):
        self.total = seconds
        self.remaining = seconds
        self.paused = False
        self.stopped = False
        self.thread = None

    def start(self, tick, done):
        def run():
            while self.remaining > 0 and not self.stopped:
                if not self.paused:
                    time.sleep(1)
                    self.remaining -= 1
                    tick(self.remaining)
                else:
                    time.sleep(0.2)
            if not self.stopped and self.remaining == 0:
                done()
        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.stopped = True
        self.paused = False

class StudyTimer:
    def __init__(self):
        self.timer = None
        self.current_type = None
        self.start_time = None
        self.seconds_planned = 0
        self.notes = ""

        setup_csv()

    def start(self, t, mins):
        if self.timer is not None:
            print("A session is already running.")
            return
        secs = mins * 60
        self.current_type = t
        self.start_time = datetime.now().isoformat(timespec="seconds")
        self.seconds_planned = secs
        self.notes = ""
        self.timer = Timer(secs)

        print(f"Starting {t} for {mins} minutes...")

        def tick(r):
            if r % 60 == 0 or r <= 10:
                print(f"Time left: {format_time(r)}")

        def done():
            end = datetime.now().isoformat(timespec="seconds")
            sid = f"{int(time.time())}-{t}"
            add_session([sid, t, self.start_time, end, self.seconds_planned, self.notes])
            print(f"\nSession finished! Total: {format_time(self.seconds_planned)}\n")
            self.timer = None
            self.current_type = None

        self.timer.start(tick, done)

    def pause_resume(self):
        if not self.timer:
            print("No session running.")
            return
        if self.timer.paused:
            self.timer.resume()
            print("Resumed.")
        else:
            self.timer.pause()
            print("Paused.")

    def cancel(self):
        if not self.timer:
            print("No active session.")
            return
        self.timer.stop()
        self.timer = None
        print("Session cancelled.")

    def add_note(self):
        if not self.timer:
            print("No active session.")
            return
        n = input("Note: ").strip()
        if n:
            if self.notes:
                self.notes += " "
            self.notes += n
            print("Note added.")

    def history(self):
        rows = read_sessions()
        if not rows:
            print("No past sessions.")
            return
        print("\nLast 10 sessions:")
        for r in rows[-10:]:
            print(f"{r['type']} | {r['start']} | {format_time(int(r['seconds']))} | {r['notes']}")
        print()

    def summary(self):
        rows = read_sessions()
        if not rows:
            print("No data yet.")
            return

        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())

        total_all = 0
        total_today = 0
        total_week = 0

        for r in rows:
            dur = int(r["seconds"])
            d = datetime.fromisoformat(r["start"]).date()
            total_all += dur
            if d == today:
                total_today += dur
            if d >= week_start:
                total_week += dur

        print("\nSummary:")
        print(f"Today:     {format_time(total_today)}")
        print(f"This week: {format_time(total_week)}")
        print(f"Overall:   {format_time(total_all)}\n")

def main():
    app = StudyTimer()

    while True:
        print("""
1) Focus session
2) Short break
3) Long break
4) Pause/Resume
5) Cancel session
6) Add note
7) History
8) Summary
q) Quit
""")
        c = input("Choose: ").strip().lower()
        if c == "1":
            app.start("focus", DEFAULT_FOCUS)
        elif c == "2":
            app.start("short_break", DEFAULT_SHORT)
        elif c == "3":
            app.start("long_break", DEFAULT_LONG)
        elif c == "4":
            app.pause_resume()
        elif c == "5":
            app.cancel()
        elif c == "6":
            app.add_note()
        elif c == "7":
            app.history()
        elif c == "8":
            app.summary()
        elif c == "q":
            print("Goodbye!")
            return
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
