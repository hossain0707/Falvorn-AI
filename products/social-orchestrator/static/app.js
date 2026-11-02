/* Falvorn Social: state stays in memory; API key is never stored in browser storage. */
(() => {
  'use strict';
  let key = '', posts = [], messages = [], signals = [], mode = 'offline';
  const $ = (id) => document.getElementById(id);
  const escape = (v) => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const flash = (message, error=false) => { $('alert').textContent=message; $('alert').className=error?'error':''; };
  async function api(path, options={}) {
    if (!key) throw Error('Connect with the admin API key first.');
    const response = await fetch(path, { ...options, headers:{'X-API-Key':key, ...(options.body?{'Content-Type':'application/json'}:{}), ...options.headers}});
    let data; try { data=await response.json(); } catch { data=null; }
    if (!response.ok) throw Error(typeof data?.detail === 'string' ? data.detail : `HTTP ${response.status}`);
    return data;
  }
  const send = (path, body, method='POST')=>api(path,{method,body:JSON.stringify(body)});
  async function safe(fn) {try{await fn();}catch(e){flash(e.message||String(e),true);}}
  const fmt = (v)=>v ? new Date(v).toLocaleString() : 'Unscheduled';
  async function refresh(){
    const [state, brand, allPosts, inbox, audit] = await Promise.all([
      api('/api/status'),api('/api/brand'),api('/api/posts'),api('/api/inbox'),api('/api/audit')]);
    posts=allPosts;messages=inbox;mode=state.mode;
    $('mode').textContent=mode==='dry_run'?'DRY RUN':'LIVE MODE';
    $('connection').textContent='Connected · '+(mode==='dry_run'?'simulation':'live');
    $('conn-instagram').textContent=state.instagram_ready?'Credentials present':'Not connected';
    $('conn-linkedin').textContent=state.linkedin_ready?'Credentials present':'Not connected';
    $('conn-youtube').textContent=state.youtube_ready?'Credentials present':'Not connected';
    $('conn-llm').textContent=state.llm_connected?'AI configured':'Template fallback';
    $('stat-posts').textContent=posts.length;
    $('stat-review').textContent=posts.filter(p=>p.status==='draft').length;
    $('stat-queued').textContent=posts.filter(p=>p.status==='scheduled').length;
    $('stat-inbox').textContent=messages.filter(m=>['pending','awaiting_approval'].includes(m.status)).length;
    $('brand-name').value=brand.name;$('brand-voice').value=brand.voice;
    $('brand-audience').value=brand.audience;$('brand-banned').value=brand.banned_terms.join(', ');
    renderPosts();renderInbox();renderAudit(audit);
  }
  function renderPosts(){
    $('posts').className=posts.length?'post-grid':'post-grid empty';
    $('posts').innerHTML=posts.length?posts.map(p=>`<article class="post"><header><span>${escape(p.platform)}</span><span class="state ${escape(p.status)}">${escape(p.status)}</span></header><h3>${escape(p.title)}</h3><p>${escape(p.body)}</p><p class="muted">${escape(fmt(p.scheduled_at))}${p.remote_id?' · ID: '+escape(p.remote_id):''}${p.error?' · '+escape(p.error):''}</p><footer>${p.status==='draft'?`<button class="outline" data-act="approve" data-id="${p.id}">Approve content</button>`:''}${p.status==='approved'?`<button class="outline" data-act="schedule" data-id="${p.id}">Schedule</button><button class="primary" data-act="publish" data-id="${p.id}">Publish now</button>`:''}${p.status==='scheduled'?`<button class="ghost" data-act="cancel" data-id="${p.id}">Cancel schedule</button>`:''}${p.media_file?`<button class="ghost" data-act="media" data-file="${p.media_file}">Download media</button>`:''}</footer></article>`).join(''):'No posts yet. Create your first draft in Content Studio.';
  }
  function renderInbox(){
    $('inbox-list').className=messages.length?'messages':'messages empty';
    $('inbox-list').innerHTML=messages.length?messages.map(m=>`<div class="message"><small>${escape(m.platform)} · ${escape(fmt(m.received_at))} · ${escape(m.status)}</small><p><b>Customer:</b> ${escape(m.message)}</p><textarea id="reply-${m.id}" rows="3" placeholder="Draft a reviewable reply">${escape(m.reply||'')}</textarea><div class="button-row"><button class="outline" data-act="draft-reply" data-id="${m.id}" ${['pending','awaiting_approval'].includes(m.status)?'':'disabled'}>Draft AI reply</button><button class="outline" data-act="save-reply" data-id="${m.id}" ${['pending','awaiting_approval'].includes(m.status)?'':'disabled'}>Save edit</button><button class="primary" data-act="send-reply" data-id="${m.id}" ${m.status==='awaiting_approval'?'':'disabled'}>Approve & send</button></div>${m.error?`<p>${escape(m.error)}</p>`:''}</div>`).join(''):'No incoming messages yet.';
  }
  function renderAudit(rows){$('audit-list').className=rows.length?'events':'events empty';$('audit-list').innerHTML=rows.length?rows.map(r=>`<div class="event"><span>${escape(fmt(r.at))}</span><b>${escape(r.event)}</b><span>${escape(r.resource)} ${escape(r.detail)}</span></div>`).join(''):'No events recorded.';}
  $('connect').onclick=()=>safe(async()=>{const attempt=$('key').value.trim();if(!attempt)throw Error('Provide the API key.');key=attempt;await refresh();$('key').value='';flash('Dashboard connected.');});
  $('generate').onclick=()=>safe(async()=>{const result=await send('/api/drafts/generate',{topic:$('topic').value,platform:$('platform').value,goal:$('goal').value});$('title').value=result.title;$('body').value=result.body;$('draft-source').textContent=`Source: ${result.source==='llm'?'configured language model':'deterministic template (no AI key configured)'}`;flash('Draft ready for review.');});
  $('save').onclick=()=>safe(async()=>{await send('/api/posts',{title:$('title').value,body:$('body').value,platform:$('platform').value,source:$('draft-source').textContent.includes('model')?'llm':'manual',media_file:$('media-file').value||null,media_url:$('media-url').value||null});await refresh();flash('Draft saved. Approve it in the queue before publishing.');location.hash='#queue';});
  for(const kind of ['poster','video'])$(kind).onclick=()=>safe(async()=>{const result=await send('/api/media/'+kind,{title:$('title').value||$('topic').value,subtitle:$('body').value.slice(0,160)});$('media-file').value=result.filename;if(result.public_url)$('media-url').value=result.public_url;$('media-output').textContent='Created: '+result.filename+(result.public_url?' · Public asset ready':' · Set PUBLIC_MEDIA_URL to host on Instagram');flash('Real media asset rendered on server.');});
  $('refresh-posts').onclick=()=>safe(refresh);
  $('brand-save').onclick=()=>safe(async()=>{await send('/api/brand',{name:$('brand-name').value,voice:$('brand-voice').value,audience:$('brand-audience').value,banned_terms:$('brand-banned').value.split(',').map(x=>x.trim()).filter(Boolean)},'PUT');flash('Brand voice saved.');});
  $('get-signals').onclick=()=>safe(async()=>{const data=await api('/api/signals?q='+encodeURIComponent($('search-query').value));signals=data.items;$('signal-list').className=signals.length?'signals':'signals empty';$('signal-list').innerHTML=signals.length?signals.map((s,i)=>`<div class="signal"><a href="${escape(s.url)}" target="_blank" rel="noopener noreferrer">${escape(s.title)}<br><small>${escape(s.source)} · ${escape(s.published)}</small></a><button class="ghost" data-act="idea" data-idx="${i}">Use idea</button></div>`).join(''):'No matching headlines returned.';flash('News signals loaded; verify sources before posting.');});
  $('ingest').onclick=()=>safe(async()=>{await send('/api/inbox/ingest',{sender_id:$('sender').value,message:$('message').value});await refresh();flash('Incoming message added for review.');});
  document.addEventListener('click',event=>safe(async()=>{
    const button=event.target.closest('button[data-act]');if(!button)return;
    const {act,id,idx,file}=button.dataset;
    if(act==='idea'){const s=signals[Number(idx)];$('topic').value=s.title;location.hash='#compose';flash('News topic copied to composer; check the linked source.');return;}
    if(act==='media'){const r=await fetch('/api/media/'+encodeURIComponent(file),{headers:{'X-API-Key':key}});if(!r.ok)throw Error('Media request failed: '+r.status);const url=URL.createObjectURL(await r.blob());const a=document.createElement('a');a.href=url;a.download=file;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),60000);return;}
    if(act==='schedule'){
      const at=prompt('Schedule date/time in ISO 8601 with timezone (e.g. 2026-12-05T10:00:00+09:00):');if(!at)return;
      await send('/api/posts/'+id+'/schedule',{at});
    }else if(act==='save-reply'){
      await send('/api/inbox/'+id+'/reply',{text:$('reply-'+id).value},'PUT');
    }else if(act==='draft-reply'){await send('/api/inbox/'+id+'/draft',{});
    }else if(act==='send-reply'){
      if(!confirm('Approve and send this reply? '+(mode==='dry_run'?'DRY RUN: no platform message will be sent.':'LIVE: this will message the customer.')))return;
      await send('/api/inbox/'+id+'/send',{});
    }else {
      if(act==='publish'&&!confirm('Publish this APPROVED post? '+(mode==='dry_run'?'DRY RUN only.':'LIVE external API action.')))return;
      await send('/api/posts/'+id+'/'+act,{});
    }
    await refresh();flash('Action completed: '+act);
  }));
})();
