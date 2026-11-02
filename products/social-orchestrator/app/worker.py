"""Single-tenant polling worker; run only one instance per SQLite database."""
import logging
import time
from .config import Settings
from .store import Store
from .services import publish_post,IntegrationError

log=logging.getLogger(__name__)

def tick(store,settings):
    count=0
    for post in store.due():
        if not store.claim(post['id'],'scheduled'):
            continue
        count+=1
        try:
            status,remote=publish_post(settings,post)
            store.finish(post['id'],status,remote)
        except IntegrationError as e:
            store.finish(post['id'],'failed',error=str(e))
        except Exception:
            log.exception('Uncertain publication; reconciliation required for %s',post['id'])
            store.finish(post['id'],'needs_reconciliation',error='Uncertain provider result; do not blindly retry')
    return count


def main():
    logging.basicConfig(level=logging.INFO)
    settings=Settings.from_env();settings.validate()
    store=Store(settings.db_path)
    log.info('Worker started: dry_run=%s',settings.dry_run)
    while True:
        tick(store,settings)
        time.sleep(5)

if __name__=='__main__':main()
