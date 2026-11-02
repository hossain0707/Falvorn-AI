"""Durable single-process-compatible SQLite store with atomic transitions and audit log."""
import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone


def utcnow():
    return datetime.now(timezone.utc).isoformat()


class Store:
    def __init__(self, path):
        self.path = path
        self.migrate()

    @contextmanager
    def db(self, write=False):
        conn = sqlite3.connect(self.path, timeout=15, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA busy_timeout=15000')
        conn.execute('PRAGMA foreign_keys=ON')
        try:
            if write:
                conn.execute('BEGIN IMMEDIATE')
            yield conn
            if write:
                conn.commit()
        except BaseException:
            if write:
                conn.rollback()
            raise
        finally:
            conn.close()

    def migrate(self):
        with sqlite3.connect(self.path) as con:
            con.execute('PRAGMA journal_mode=WAL')
            con.executescript('''
                CREATE TABLE IF NOT EXISTS brand (
                    id INTEGER PRIMARY KEY CHECK(id=1), name TEXT NOT NULL,
                    voice TEXT NOT NULL, audience TEXT NOT NULL, banned_terms TEXT NOT NULL
                );
                INSERT OR IGNORE INTO brand VALUES (1,'Falvorn AI',
                    'Practical, clear, confident; avoid hype and unsupported claims',
                    'Business leaders and AI engineers','[]');
                CREATE TABLE IF NOT EXISTS posts (
                    id TEXT PRIMARY KEY, title TEXT NOT NULL, body TEXT NOT NULL,
                    platform TEXT NOT NULL, source TEXT NOT NULL, media_file TEXT,
                    media_url TEXT, status TEXT NOT NULL DEFAULT 'draft',
                    scheduled_at TEXT, remote_id TEXT, error TEXT,
                    created_at TEXT NOT NULL, updated_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_posts_schedule ON posts(status,scheduled_at);
                CREATE TABLE IF NOT EXISTS inbox (
                    id TEXT PRIMARY KEY, sender_id TEXT NOT NULL, platform TEXT NOT NULL,
                    message TEXT NOT NULL, received_at TEXT NOT NULL,
                    reply TEXT, status TEXT NOT NULL DEFAULT 'pending', remote_id TEXT,
                    error TEXT
                );
                CREATE TABLE IF NOT EXISTS audit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL,
                    event TEXT NOT NULL, resource TEXT NOT NULL, detail TEXT NOT NULL
                );
            ''')

    def audit(self, conn, event, resource, detail=''):
        conn.execute('INSERT INTO audit(at,event,resource,detail) VALUES(?,?,?,?)',
                     (utcnow(), event, resource, detail[:500]))

    def brand(self):
        with self.db() as c:
            r = dict(c.execute('SELECT * FROM brand WHERE id=1').fetchone())
            r['banned_terms'] = json.loads(r['banned_terms'])
            return r

    def set_brand(self, name, voice, audience, banned_terms):
        with self.db(True) as c:
            c.execute('UPDATE brand SET name=?,voice=?,audience=?,banned_terms=? WHERE id=1',
                      (name,voice,audience,json.dumps(banned_terms)))
            self.audit(c, 'brand.updated', 'brand')
        return self.brand()

    def create_post(self, data):
        pid = str(uuid.uuid4())
        at = utcnow()
        with self.db(True) as c:
            c.execute('''INSERT INTO posts(id,title,body,platform,source,media_file,media_url,created_at,updated_at)
                      VALUES(?,?,?,?,?,?,?,?,?)''',
                      (pid,data['title'],data['body'],data['platform'],data.get('source','manual'),
                       data.get('media_file'),data.get('media_url'),at,at))
            self.audit(c, 'post.created', pid, data['platform'])
        return self.post(pid)

    def post(self, pid):
        with self.db() as c:
            r = c.execute('SELECT * FROM posts WHERE id=?',(pid,)).fetchone()
            return dict(r) if r else None

    def posts(self):
        with self.db() as c:
            return [dict(x) for x in c.execute('SELECT * FROM posts ORDER BY created_at DESC LIMIT 200')]

    def transition(self, pid, old, new, scheduled_at=None):
        with self.db(True) as c:
            q = c.execute('''UPDATE posts SET status=?,scheduled_at=?,updated_at=?,error=NULL
                                WHERE id=? AND status=?''',(new,scheduled_at,utcnow(),pid,old))
            if q.rowcount != 1:
                return False
            self.audit(c, 'post.'+new, pid)
        return True

    def claim(self, pid, expected_status):
        return self.transition(pid, expected_status, 'publishing')

    def due(self):
        with self.db() as c:
            return [dict(r) for r in c.execute('''SELECT * FROM posts
                 WHERE status='scheduled' AND scheduled_at<=? ORDER BY scheduled_at LIMIT 20''',(utcnow(),))]

    def finish(self, pid, status, remote_id='', error=''):
        assert status in ('published','uploaded_private','simulated','failed','needs_reconciliation')
        with self.db(True) as c:
            updated = c.execute('''UPDATE posts SET status=?,remote_id=?,error=?,updated_at=?
                           WHERE id=? AND status='publishing' ''',(status,remote_id,error[:500],utcnow(),pid))
            if updated.rowcount:
                self.audit(c,'post.'+status,pid,error)

    def inbox_add(self, sender_id, platform, message, received_at, explicit_id=None):
        iid = explicit_id or str(uuid.uuid4())
        with self.db(True) as c:
            q=c.execute('''INSERT OR IGNORE INTO inbox(id,sender_id,platform,message,received_at)
                           VALUES(?,?,?,?,?)''',(iid,sender_id,platform,message,received_at))
            if q.rowcount:
                self.audit(c,'inbox.received',iid,platform)
        return self.inbox_item(iid)

    def inbox_item(self, iid):
        with self.db() as c:
            r=c.execute('SELECT * FROM inbox WHERE id=?',(iid,)).fetchone()
            return dict(r) if r else None

    def inbox_list(self):
        with self.db() as c:
            return [dict(r) for r in c.execute('SELECT * FROM inbox ORDER BY received_at DESC LIMIT 200')]

    def set_reply(self, iid, reply):
        with self.db(True) as c:
            q=c.execute("UPDATE inbox SET reply=?,status='awaiting_approval' WHERE id=? AND status IN ('pending','awaiting_approval')",(reply,iid))
            if q.rowcount:
                self.audit(c,'reply.drafted',iid)
            return bool(q.rowcount)

    def claim_reply(self,iid):
        with self.db(True) as c:
            q=c.execute("UPDATE inbox SET status='sending' WHERE id=? AND status='awaiting_approval' AND reply IS NOT NULL",(iid,))
            if q.rowcount:
                self.audit(c,'reply.approved',iid)
            return bool(q.rowcount)

    def finish_reply(self,iid,status,remote_id='',error=''):
        with self.db(True) as c:
            c.execute("UPDATE inbox SET status=?,remote_id=?,error=? WHERE id=? AND status='sending'",(status,remote_id,error[:500],iid))
            self.audit(c,'reply.'+status,iid,error)

    def audit_list(self):
        with self.db() as c:
            return [dict(r) for r in c.execute('SELECT * FROM audit ORDER BY id DESC LIMIT 200')]
