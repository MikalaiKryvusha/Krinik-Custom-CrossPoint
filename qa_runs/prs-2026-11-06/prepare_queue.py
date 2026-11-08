"""Read-only preflight of prepared PR branches and illustration URLs."""
from pathlib import Path
import json,re,subprocess

base=Path('/Users/kryvusha/Xteink')
run=Path(__file__).resolve().parent
items=[('01','screen-clean-menu','pr/screen-clean-menu','01-screen-cleaning.md',[]),('02','calibration','pr/screen-calibration','02-calibration.md',[]),('03','screen-redraw-delay','pr/screen-redraw-delay','03-delayed-redraw.md',['01']),('04','screen-clean-return','pr/screen-clean-return','04-home-control-center-clean.md',['01','03'])]
rows=[]
urls=set()
for key,folder,branch,body,needs in items:
 repo=base/'pr-fixes'/folder
 sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
 assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo,text=True).strip(),folder
 title=subprocess.check_output(['git','show','-s','--format=%s'],cwd=repo,text=True).strip()
 urls.update(re.findall(r'https://raw\.githubusercontent\.com/[^\s)]+',(run/'bodies'/body).read_text()))
 rows.append({'id':key,'repo':str(repo),'branch':branch,'sha':sha,'title':title,'body':str(run/'bodies'/body),'requires_merged':needs,'destination':'crosspoint-reader/crosspoint-reader','base':'develop'})
checks=[]
for url in sorted(urls):
 r=subprocess.run(['curl','--head','--fail','--silent','--show-error','--max-time','20','--output','/dev/null','--write-out','%{http_code}',url],text=True,capture_output=True)
 assert r.returncode==0 and r.stdout=='200',(url,r.stdout,r.stderr)
 checks.append({'url':url,'status':200})
(run/'queue.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(run/'assets-check.json').write_text(json.dumps(checks,indent=2)+'\n')
print(f'Queue ready: {len(rows)} clean branches; {len(checks)} illustration URLs HTTP 200; no PRs opened.')
