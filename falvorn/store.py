"""Durable, single-node SQLite event store for agent runs and monitor subscriptions.

SQLite WAL is suitable for a controlled single-node deployment. It is NOT a
multi-worker queue, clustered event bus, or production tenancy boundary.
"""
import json
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any


class RunStore:
    def __init__(self, filename: str | Path):
        self.filename = Path(filename)
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        with self.connect() as db:
            db.executescript("""
            CREATE TABLE IF NOT EXISTS runs (
                id TEXT PRIMARY KEY, status TEXT NOT NULL,
                created_at REAL NOT NULL, updated_at REAL NOT NULL,
                answer TEXT, error TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_runs_created ON runs(created_at DESC);
            CREATE TABLE IF NOT EXISTS run_events (
                run_id TEXT NOT NULL, seq INTEGER NOT NULL,
                at REAL NOT NULL, type TEXT NOT NULL, payload TEXT NOT NULL,
                PRIMARY KEY(run_id, seq), FOREIGN KEY(run_id) REFERENCES runs(id)
            );
            CREATE TABLE IF NOT EXISTS monitor_subscriptions (
                id TEXT PRIMARY KEY, url TEXT NOT NULL, interval_seconds INTEGER NOT NULL,
                enabled INTEGER NOT NULL DEFAULT 1, next_check REAL NOT NULL,
                last_check REAL, last_changed INTEGER, last_error TEXT
            );
            """)
            # Interrupted in-process tasks cannot be resumed safely after restart.
            db.execute("UPDATE runs SET status='interrupted', error='Process restarted before completion', updated_at=? WHERE status IN ('queued','running')", (time.time(),))

    def connect(self):
        db = sqlite3.connect(self.filename, timeout=10)
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA busy_timeout=10000")
        db.execute("PRAGMA foreign_keys=ON")
        return db

    @staticmethod
    def dumps(v: Any) -> str:
        return json.dumps(v, ensure_ascii=False, default=str)

    def create(self, run_id: str, status='queued'):
        now = time.time()
        with self.lock, self.connect() as db:
            db.execute("INSERT INTO runs(id,status,created_at,updated_at) VALUES(?,?,?,?)", (run_id,status,now,now))

    def state(self, run_id: str, status: str, answer: Any = None, error: str | None = None):
        with self.lock, self.connect() as db:
            db.execute("UPDATE runs SET status=?, updated_at=?, answer=?, error=? WHERE id=?",
                       (status,time.time(),self.dumps(answer) if answer is not None else None,error,run_id))

    def event(self, run_id: str, kind: str, **payload):
        now = time.time()
        with self.lock, self.connect() as db:
            seq = db.execute("SELECT COALESCE(MAX(seq)+1, 0) FROM run_events WHERE run_id=?", (run_id,)).fetchone()[0]
            db.execute("INSERT INTO run_events(run_id,seq,at,type,payload) VALUES(?,?,?,?,?)",
                       (run_id,seq,now,kind,self.dumps(payload)))
            db.execute("UPDATE runs SET updated_at=? WHERE id=?", (now,run_id))
        return {"seq":seq,"at":now,"type":kind,**payload}

    def get(self, run_id: str, limit=500):
        with self.lock, self.connect() as db:
            db.row_factory = sqlite3.Row
            row = db.execute("SELECT * FROM runs WHERE id=?", (run_id,)).fetchone()
            if not row:
                return None
            evs = db.execute("SELECT * FROM run_events WHERE run_id=? ORDER BY seq ASC LIMIT ?",
                             (run_id,limit)).fetchall()
        return {"id": row['id'], "status":row['status'], "answer":json.loads(row['answer']) if row['answer'] else None,
                "error":row['error'], "created_at":row['created_at'], "updated_at":row['updated_at'],
                "events":[{"seq":e['seq'],"at":e['at'],"type":e['type'],**json.loads(e['payload'])} for e in evs]}

    def list(self, limit=50):
        with self.lock, self.connect() as db:
            rows = db.execute("SELECT id FROM runs ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
        return [self.get(row[0],limit=100) for row in rows]

    def add_subscription(self, sub_id: str, url: str, interval: int):
        with self.lock, self.connect() as db:
            db.execute("INSERT INTO monitor_subscriptions (id,url,interval_seconds,next_check) VALUES(?,?,?,?)",
                       (sub_id,url,interval,time.time()))
        return self.subscription(sub_id)

    def subscription(self, sub_id: str):
        with self.lock, self.connect() as db:
            db.row_factory = sqlite3.Row
            row = db.execute("SELECT * FROM monitor_subscriptions WHERE id=?",(sub_id,)).fetchone()
        return dict(row) if row else None

    def subscriptions(self, due_only=False):
        q = "SELECT * FROM monitor_subscriptions"
        if due_only:q += " WHERE enabled=1 AND next_check<=?"
        q += " ORDER BY next_check ASC LIMIT 100"
        with self.lock,self.connect() as db:
            db.row_factory=sqlite3.Row
            rows=db.execute(q,(time.time(),) if due_only else ()).fetchall()
        return [dict(row) for row in rows]

    def update_subscription(self, sub_id: str, enabled: bool):
        with self.lock, self.connect() as db:
            db.execute("UPDATE monitor_subscriptions SET enabled=?,next_check=? WHERE id=?",
                       (int(enabled),time.time(),sub_id))
        return self.subscription(sub_id)

    def mark_subscription(self, sub_id: str, changed: bool | None, error: str | None = None):
        sub=self.subscription(sub_id)
        if not sub:return
        with self.lock, self.connect() as db:
            db.execute("UPDATE monitor_subscriptions SET last_check=?,last_changed=?,last_error=?,next_check=? WHERE id=?",
                       (time.time(),None if changed is None else int(changed),error,time.time()+sub['interval_seconds'],sub_id))

    def delete_subscription(self, sub_id: str):
        with self.lock,self.connect() as db:
            n=db.execute("DELETE FROM monitor_subscriptions WHERE id=?",(sub_id,)).rowcount
        return bool(n)
