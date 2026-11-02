from dataclasses import replace
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import hashlib
import hmac
import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.config import Settings
from app.main import make_app
from app.store import Store
from app.worker import tick


@pytest.fixture
def setup(tmp_path):
    st=replace(Settings.from_env(),api_key='A'*32,db_path=str(tmp_path/'db.sqlite'),
               media_dir=str(tmp_path/'media'),public_media_url='',dry_run=True,
               llm_api_key='',meta_app_secret='test-signature-secret',meta_verify_token='my-verification')
    app=make_app(st)
    with TestClient(app) as c:
        yield c,st


def auth():return {'X-API-Key':'A'*32}


def test_unauthorized(setup):
    c,_=setup
    assert c.get('/health').status_code==200
    assert c.get('/api/posts').status_code==401
    assert c.get('/api/posts',headers={'X-API-Key':'bad'}).status_code==401


def test_draft_review_publish_simulation(setup):
    c,_=setup
    generated=c.post('/api/drafts/generate',headers=auth(),json={'topic':'Reusable project strategies','platform':'linkedin'}).json()
    assert generated['source']=='template'
    p=c.post('/api/posts',headers=auth(),json={'title':generated['title'],'body':generated['body'],'platform':'linkedin','source':'template'}).json()
    pid=p['id']
    assert c.post('/api/posts/'+pid+'/publish',headers=auth()).status_code==409
    assert c.post('/api/posts/'+pid+'/approve',headers=auth()).json()['status']=='approved'
    assert c.post('/api/posts/'+pid+'/approve',headers=auth()).status_code==409
    done=c.post('/api/posts/'+pid+'/publish',headers=auth()).json()
    assert done['status']=='simulated'
    assert done['remote_id'].startswith('dry-run-')
    assert c.post('/api/posts/'+pid+'/publish',headers=auth()).status_code==409
    assert len(c.get('/api/audit',headers=auth()).json())>=3


def test_schedule_and_worker(setup):
    c,settings=setup
    p=c.post('/api/posts',headers=auth(),json={'title':'Launch','body':'This is a scheduled announcement','platform':'linkedin'}).json()
    pid=p['id']
    assert c.post('/api/posts/'+pid+'/schedule',headers=auth(),json={'at':'2026-12-01T10:00:00+09:00'}).status_code==409
    c.post('/api/posts/'+pid+'/approve',headers=auth())
    assert c.post('/api/posts/'+pid+'/schedule',headers=auth(),json={'at':'2020-01-01T00:00:00+00:00'}).status_code==422
    future=(datetime.now(timezone.utc)+timedelta(minutes=10)).isoformat()
    assert c.post('/api/posts/'+pid+'/schedule',headers=auth(),json={'at':future}).json()['status']=='scheduled'
    store=Store(settings.db_path)
    assert tick(store,settings)==0
    with store.db(True) as db:
        db.execute('UPDATE posts SET scheduled_at=? WHERE id=?',('2020-01-01T00:00:00+00:00',pid))
    assert tick(store,settings)==1
    assert tick(store,settings)==0
    assert store.post(pid)['status']=='simulated'


def test_inbox_review_and_24h_guard(setup):
    c,_=setup
    data=c.post('/api/inbox/ingest',headers=auth(),json={'sender_id':'scoped-user-42','message':'Can I learn more?'}).json()
    path='/api/inbox/'+data['id']
    assert c.post(path+'/send',headers=auth()).status_code==409
    assert c.post(path+'/draft',headers=auth()).json()['source']=='template'
    assert c.put(path+'/reply',headers=auth(),json={'text':'Thank you! A team member will contact you.'}).status_code==200
    assert c.post(path+'/send',headers=auth()).json()['status']=='simulated'
    assert c.post(path+'/send',headers=auth()).status_code==409
    old=(datetime.now(timezone.utc)-timedelta(hours=25)).isoformat()
    another=c.post('/api/inbox/ingest',headers=auth(),json={'sender_id':'id-2','message':'Past window','received_at':old}).json()
    assert c.post('/api/inbox/'+another['id']+'/draft',headers=auth()).status_code==200
    assert c.post('/api/inbox/'+another['id']+'/send',headers=auth()).status_code==422


def test_generated_poster_and_public_access_off(setup):
    c,settings=setup
    result=c.post('/api/media/poster',headers=auth(),json={'title':'Real created image','subtitle':'Actual PNG'}).json()
    filename=result['filename']
    assert (Path(settings.media_dir)/filename).read_bytes()[:8]==b'\x89PNG\r\n\x1a\n'
    assert c.get('/api/media/'+filename,headers=auth()).status_code==200
    assert c.get('/api/media/'+filename).status_code==401
    assert c.get('/public/media/'+filename).status_code==404
    assert c.post('/api/posts',headers=auth(),json={'title':'Wrong media','body':'Hi world','platform':'instagram','media_file':'../x.png'}).status_code==422


def test_meta_webhook_signature_and_dedup(setup):
    c,_=setup
    assert c.get('/webhooks/meta?hub.mode=subscribe&hub.verify_token=my-verification&hub.challenge=200').text=='200'
    payload={'entry':[{'messaging':[{'sender':{'id':'123'},'message':{'mid':'m1','text':'Hello!'},'timestamp':int(datetime.now(timezone.utc).timestamp()*1000)}]}]}
    raw=json.dumps(payload).encode()
    assert c.post('/webhooks/meta',content=raw).status_code==401
    sig='sha256='+hmac.new(b'test-signature-secret',raw,hashlib.sha256).hexdigest()
    for _ in range(2):
        assert c.post('/webhooks/meta',content=raw,headers={'X-Hub-Signature-256':sig}).status_code==200
    inbox=c.get('/api/inbox',headers=auth()).json()
    assert len(inbox)==1
    assert inbox[0]['message']=='Hello!'


def test_brand_settings_and_post_validation(setup):
    c,_=setup
    brand={'name':'Research Labs','voice':'Simple, precise language without hype','audience':'Research engineers','banned_terms':['magic']}
    assert c.put('/api/brand',headers=auth(),json=brand).json()['banned_terms']==['magic']
    assert c.post('/api/posts',headers=auth(),json={'title':'Bad url','body':'Valid body','platform':'instagram','media_url':'http://127.0.0.1/a.png'}).status_code==422
    assert c.post('/api/posts',headers=auth(),json={'title':'Good url','body':'Valid body','platform':'instagram','media_url':'https://cdn.example.com/a.png'}).status_code==200


def test_real_mp4_renderer(setup):
    import shutil
    if not shutil.which('ffmpeg'):
        pytest.skip('FFmpeg not installed on this OS')
    c,settings=setup
    resp=c.post('/api/media/video',headers=auth(),json={'title':'Production workflow','subtitle':'Original animation'}).json()
    path=Path(settings.media_dir)/resp['filename']
    assert path.is_file() and path.stat().st_size>10000
    assert b'ftyp' in path.read_bytes()[:32]


def test_public_media_requires_explicit_operator_url(tmp_path):
    settings=replace(Settings.from_env(),api_key='B'*32,db_path=str(tmp_path/'db.sqlite'),
                     media_dir=str(tmp_path/'media'),public_media_url='https://cdn.example.org',dry_run=True)
    with TestClient(make_app(settings)) as c:
        r=c.post('/api/media/poster',headers={'X-API-Key':'B'*32},json={'title':'Shareable art'}).json()
        assert r['public_url'].startswith('https://cdn.example.org/public/media/')
        assert c.get('/public/media/'+r['filename']).status_code==200
        assert c.get('/public/media/../../etc/passwd').status_code in (404, 400)


def test_claim_is_atomic(setup):
    c,settings=setup
    post=c.post('/api/posts',headers=auth(),json={'title':'Race protection','body':'Safe message','platform':'linkedin'}).json()
    c.post('/api/posts/'+post['id']+'/approve',headers=auth())
    db1=Store(settings.db_path)
    db2=Store(settings.db_path)
    assert db1.claim(post['id'],'approved')
    assert not db2.claim(post['id'],'approved')


def test_integrations_reject_missing_credentials_and_local_urls(setup):
    from app.services import IntegrationError,ensure_https,publish_post
    c,settings=setup
    live=replace(settings,dry_run=False,linkedin_token='',meta_token='',youtube_token='')
    with pytest.raises(IntegrationError,match='LINKEDIN'):
        publish_post(live,{'platform':'linkedin','body':'Test','id':'test-id'})
    for url in ['http://example.com/abc.png','https://localhost/img.png','https://127.0.0.1/image.png','https://192.168.1.10/secret.png','https://[::1]/a.jpg']:
        with pytest.raises(IntegrationError):ensure_https(url)


def test_known_example_key_is_rejected(tmp_path):
    settings=replace(Settings.from_env(),api_key='CHANGE_ME_TO_RANDOM_STRING_LONGER_THAN_24_CHARS',
                     db_path=str(tmp_path/'db.sqlite'),media_dir=str(tmp_path/'media'))
    with pytest.raises(RuntimeError,match='SOCIAL_API_KEY'):
        make_app(settings)
