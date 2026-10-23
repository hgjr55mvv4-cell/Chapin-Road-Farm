import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const root=resolve(dirname(fileURLToPath(import.meta.url)), '..');
const home=readFileSync(resolve(root,'index.html'),'utf8');
const demo=readFileSync(resolve(root,'harbor-co-listener/index.html'),'utf8');
test('homepage has useful metadata and accessible wayfinding',()=>{
  assert.match(home,/^<!doctype html>/i);
  assert.match(home,/<title>Chapin Road Farm · Open Research<\/title>/);
  assert.match(home,/name="description"/);
  assert.match(home,/aria-label="Main navigation"/);
  assert.match(home,/id="research"/);
  assert.match(home,/id="join"/);
});
test('homepage runs without remote script or stylesheet and links to existing local demo',()=>{
  assert.doesNotMatch(home,/<script\b/i);
  assert.doesNotMatch(home,/<link[^>]+href="https?:/i);
  const links=[...home.matchAll(/\bhref="([^"]+)"/g)].map(x=>x[1]);
  for(const link of links){
    assert.ok(!link.startsWith('/'),'project Pages incompatible root link: '+link);
    if(link.startsWith('http')||link.startsWith('#'))continue;
    assert.ok(existsSync(resolve(root,link)),'missing local target '+link);
  }
});
test('honest status distinctions are present',()=>{
  for(const term of ['no integrated AI listener','Unconfirmed hypothesis','Engineering design · not qualified'])
    assert.ok(home.includes(term),'missing: '+term);
});
test('existing manual listening interface remains present',()=>{
  for(const id of ['file','audio','mark','heard','felt','respond','export','clear','timeline'])
    assert.ok(demo.includes('id="'+id+'"'),'missing prototype control: '+id);
});
test('research index status matches public description',()=>{
  const json=JSON.parse(readFileSync(resolve(root,'research-index.json'),'utf8'));
  const harbor=json.projects.find(p=>p.id==='harbor-co-listener');
  assert.ok(harbor);
  assert.equal(harbor.ai_audio_perception_integrated,false);
  assert.equal(harbor.personal_longitudinal_learning_verified,false);
});
