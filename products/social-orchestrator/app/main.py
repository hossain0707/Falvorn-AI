"""HTTP API: every external publishing action requires a separate approval transition."""
import hashlib
import hmac
import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Literal
from fastapi import FastAPI, Depends, Header, HTTPException, Request, Query
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field, field_validator
from .config import Settings
from .store import Store, utcnow
from . import services


class BrandIn(BaseModel):
    name: str = Field(min_length=2,max_length=100)
    voice: str = Field(min_length=5,max_length=600)
    audience: str = Field(min_length=3,max_length=300)
    banned_terms: list[str] = Field(default_factory=list,max_length=30)

class DraftIn(BaseModel):
    topic: str = Field(min_length=3,max_length=400)
    platform: Literal['instagram','linkedin','youtube']
    goal: str = Field(default='educate',max_length=120)

class PostIn(BaseModel):
    title: str = Field(min_length=3,max_length=140)
    body: str = Field(min_length=3,max_length=4500)
    platform: Literal['instagram','linkedin','youtube']
    source: Literal['manual','llm','template'] = 'manual'
    media_file: str | None = None
    media_url: str | None = None

    @field_validator('media_file')
    @classmethod
    def safe_filename(cls,v):
        if v is not None and not re.fullmatch(r'[a-f0-9-]{36}\.(png|mp4)',v):
            raise ValueError('Expected generated media UUID filename')
        return v

class ScheduleIn(BaseModel):
    at: datetime

class InboxIn(BaseModel):
    sender_id: str = Field(min_length=1,max_length=200)
    message: str = Field(min_length=1,max_length=2000)
    received_at: datetime | None = None

class ReplyIn(BaseModel):
    text: str = Field(min_length=2,max_length=1200)

class CreativeIn(BaseModel):
    title: str = Field(min_length=3,max_length=125)
    subtitle: str = Field(default='',max_length=180)


def make_app(settings=None):
    settings=settings or Settings.from_env()
    settings.validate()
    store=Store(settings.db_path)
    api=FastAPI(title='Falvorn Social Orchestrator',version='0.1.0',docs_url=None,redoc_url=None)
    api.state.settings=settings
    api.state.store=store

    @api.middleware('http')
    async def headers(request,call_next):
        response=await call_next(request)
        response.headers.update({'X-Content-Type-Options':'nosniff','X-Frame-Options':'DENY',
                                 'Referrer-Policy':'no-referrer','Cache-Control':'no-store',
                                 'Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'"})
        return response

    def authorized(x_api_key: str | None=Header(None)):
        if not x_api_key or not hmac.compare_digest(x_api_key,settings.api_key):
            raise HTTPException(401,'Invalid API key')
        return True

    def missing(value):
        if not value:raise HTTPException(404,'Resource not found')
        return value

    @api.get('/health')
    def health():
        return {'ok':True,'service':'falvorn-social','version':'0.1.0'}

    static=Path(__file__).resolve().parent.parent/'static'
    @api.get('/',response_class=HTMLResponse)
    def page():
        return (static/'index.html').read_text()

    @api.get('/static/{file}')
    def static_file(file):
        if file not in ('app.js','style.css'):
            raise HTTPException(404)
        return FileResponse(static/file)

    @api.get('/public/media/{filename}')
    def media(filename: str):
        # Only enabled when operator explicitly configured a public HTTPS origin.
        if not settings.public_media_url or not re.fullmatch(r'[a-f0-9-]{36}\.(png|mp4)',filename):
            raise HTTPException(404)
        path=Path(settings.media_dir)/filename
        if not path.is_file():raise HTTPException(404)
        return FileResponse(path,media_type='video/mp4' if filename.endswith('.mp4') else 'image/png',
                            headers={'Cache-Control':'public,max-age=3600'})

    @api.get('/api/status',dependencies=[Depends(authorized)])
    def status():
        return {'mode':'dry_run' if settings.dry_run else 'live',
                'llm_connected':bool(settings.llm_api_key),
                'instagram_ready':bool(settings.meta_token and settings.meta_ig_id),
                'linkedin_ready':bool(settings.linkedin_token and settings.linkedin_author),
                'youtube_ready':bool(settings.youtube_token),
                'public_media_ready':bool(settings.public_media_url)}

    @api.get('/api/brand',dependencies=[Depends(authorized)])
    def brand():return store.brand()

    @api.put('/api/brand',dependencies=[Depends(authorized)])
    def update_brand(data:BrandIn):return store.set_brand(**data.model_dump())

    @api.get('/api/signals',dependencies=[Depends(authorized)])
    def signals(q:str=Query('',max_length=90)):
        try:return {'source':'Google News RSS (not ranked trends)', 'items':services.news_signals(settings,q)}
        except Exception as e:raise HTTPException(502,'Could not retrieve RSS news signals') from e

    @api.post('/api/drafts/generate',dependencies=[Depends(authorized)])
    def generate(data:DraftIn):
        try:
            body,source=services.draft(settings,store.brand(),data.topic,data.platform,data.goal)
            return {'title':data.topic[:120],'body':body,'source':source,'platform':data.platform}
        except Exception as e:raise HTTPException(502,'Text model request failed') from e

    @api.get('/api/posts',dependencies=[Depends(authorized)])
    def posts():return store.posts()

    @api.post('/api/posts',dependencies=[Depends(authorized)])
    def create_post(data:PostIn):
        if data.media_file and not (Path(settings.media_dir)/data.media_file).is_file():
            raise HTTPException(422,'Generated media file missing')
        if data.media_url:
            try:services.ensure_https(data.media_url)
            except services.IntegrationError as e:raise HTTPException(422,str(e)) from e
        return store.create_post(data.model_dump())

    @api.post('/api/posts/{pid}/approve',dependencies=[Depends(authorized)])
    def approve(pid:str):
        if not store.transition(pid,'draft','approved'):
            raise HTTPException(409,'Only existing draft posts can be approved')
        return store.post(pid)

    @api.post('/api/posts/{pid}/schedule',dependencies=[Depends(authorized)])
    def schedule(pid:str,data:ScheduleIn):
        if data.at.tzinfo is None or data.at <= datetime.now(timezone.utc)+timedelta(seconds=5):
            raise HTTPException(422,'Schedule must be at least 5 seconds ahead with timezone')
        at=data.at.astimezone(timezone.utc).isoformat()
        if not store.transition(pid,'approved','scheduled',at):
            raise HTTPException(409,'Approve the post before scheduling')
        return store.post(pid)

    def publish(pid,old):
        if not store.claim(pid,old):
            raise HTTPException(409,'Post is not ready or already being handled')
        post=store.post(pid)
        try:
            status,remote=services.publish_post(settings,post)
            store.finish(pid,status,remote)
        except services.IntegrationError as e:
            store.finish(pid,'failed',error=str(e))
        except Exception as e:
            # Network timeout may occur AFTER a successful provider post: no blind retry.
            store.finish(pid,'needs_reconciliation',error='Uncertain API result; check provider before retrying')
        return store.post(pid)

    @api.post('/api/posts/{pid}/publish',dependencies=[Depends(authorized)])
    def publish_now(pid:str):
        return publish(pid,'approved')

    @api.post('/api/posts/{pid}/cancel',dependencies=[Depends(authorized)])
    def cancel(pid:str):
        if not store.transition(pid,'scheduled','cancelled'):
            raise HTTPException(409,'Only scheduled posts can be cancelled')
        return store.post(pid)

    @api.post('/api/media/poster',dependencies=[Depends(authorized)])
    def poster(data:CreativeIn):
        filename=services.creative_image(settings,data.title,data.subtitle)
        return {'filename':filename,'public_url':settings.public_media_url+'/public/media/'+filename if settings.public_media_url else None}

    @api.post('/api/media/video',dependencies=[Depends(authorized)])
    def video(data:CreativeIn):
        try:filename=services.creative_video(settings,data.title,data.subtitle)
        except services.IntegrationError as e:raise HTTPException(503,str(e)) from e
        return {'filename':filename,'public_url':settings.public_media_url+'/public/media/'+filename if settings.public_media_url else None}

    @api.get('/api/media/{filename}',dependencies=[Depends(authorized)])
    def private_media(filename:str):
        if not re.fullmatch(r'[a-f0-9-]{36}\.(png|mp4)',filename):raise HTTPException(404)
        path=Path(settings.media_dir)/filename
        if not path.is_file():raise HTTPException(404)
        return FileResponse(path)

    @api.get('/api/inbox',dependencies=[Depends(authorized)])
    def inbox():return store.inbox_list()

    @api.post('/api/inbox/ingest',dependencies=[Depends(authorized)])
    def ingest(data:InboxIn):
        timestamp=(data.received_at or datetime.now(timezone.utc))
        if timestamp.tzinfo is None:raise HTTPException(422,'received_at must include timezone')
        return store.inbox_add(data.sender_id,'instagram',data.message,timestamp.isoformat())

    @api.post('/api/inbox/{iid}/draft',dependencies=[Depends(authorized)])
    def draft_reply(iid:str):
        item=missing(store.inbox_item(iid))
        try:answer,source=services.make_reply(settings,store.brand(),item['message'])
        except Exception as e:raise HTTPException(502,'Reply generation failed') from e
        if not store.set_reply(iid,answer):raise HTTPException(409,'Message already handled')
        return {'item':store.inbox_item(iid),'source':source}

    @api.put('/api/inbox/{iid}/reply',dependencies=[Depends(authorized)])
    def edit_reply(iid:str,data:ReplyIn):
        if not store.set_reply(iid,data.text):raise HTTPException(409,'Message already handled')
        return store.inbox_item(iid)

    @api.post('/api/inbox/{iid}/send',dependencies=[Depends(authorized)])
    def approve_reply(iid:str):
        item=missing(store.inbox_item(iid))
        received=datetime.fromisoformat(item['received_at'])
        if received.tzinfo is None or received < datetime.now(timezone.utc)-timedelta(hours=24):
            raise HTTPException(422,'Message is outside the conservative 24-hour reply window')
        if not store.claim_reply(iid):raise HTTPException(409,'Draft and review reply before sending')
        try:
            remote=services.send_reply(settings,item)
            store.finish_reply(iid,'simulated' if settings.dry_run else 'sent',remote)
        except services.IntegrationError as e:store.finish_reply(iid,'failed',error=str(e))
        except Exception:store.finish_reply(iid,'needs_reconciliation',error='Check provider before retrying')
        return store.inbox_item(iid)

    @api.get('/api/audit',dependencies=[Depends(authorized)])
    def audit():return store.audit_list()

    @api.get('/webhooks/meta')
    def meta_verify(request:Request):
        p=request.query_params
        if (settings.meta_verify_token and p.get('hub.mode')=='subscribe' and
                hmac.compare_digest(p.get('hub.verify_token',''),settings.meta_verify_token)):
            return PlainTextResponse(p.get('hub.challenge',''))
        raise HTTPException(403,'Invalid webhook verification')

    @api.post('/webhooks/meta')
    async def meta_ingest(request:Request,x_hub_signature_256:str|None=Header(None)):
        if not settings.meta_app_secret:
            raise HTTPException(503,'Webhook signing secret not configured')
        raw=await request.body()
        if len(raw)>200_000:raise HTTPException(413)
        expected='sha256='+hmac.new(settings.meta_app_secret.encode(),raw,hashlib.sha256).hexdigest()
        if not x_hub_signature_256 or not hmac.compare_digest(x_hub_signature_256,expected):
            raise HTTPException(401,'Invalid Meta webhook signature')
        try:data=json.loads(raw)
        except ValueError:raise HTTPException(400,'Invalid JSON')
        count=0
        # For messaging events. Ignore delivery echoes and any unsupported event types.
        for entry in data.get('entry',[])[:20]:
            for event in entry.get('messaging',[])[:50]:
                msg=event.get('message') or {}
                sender=event.get('sender',{}).get('id','')
                mid=msg.get('mid','')
                text=msg.get('text','')
                if not sender or not mid or not text or msg.get('is_echo'):
                    continue
                ts=event.get('timestamp')
                received=(datetime.fromtimestamp(ts/1000,timezone.utc).isoformat() if isinstance(ts,(int,float)) else utcnow())
                store.inbox_add(str(sender)[:200],'instagram',str(text)[:2000],received,explicit_id=hashlib.sha256(mid.encode()).hexdigest())
                count+=1
        return {'ok':True,'processed':count}

    return api

# Importing the module alone never creates the database; ASGI app construction is explicit.
app=make_app() if os.getenv('SOCIAL_API_KEY') else None
