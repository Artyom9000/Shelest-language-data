"""Rebuild complete Rime data using a pinned official host compiler; never app code."""
import argparse,hashlib,json,os,pathlib,shutil,subprocess,urllib.request,zipfile
ROOT=pathlib.Path(__file__).resolve().parent
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def fetch(url,path,sha,limit):
    if path.is_file() and digest(path)==sha:return
    with urllib.request.urlopen(url,timeout=120) as response:data=response.read(limit+1)
    if len(data)>limit or hashlib.sha256(data).hexdigest()!=sha:raise ValueError('Pinned input mismatch: '+path.name)
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=pathlib.Path,required=True);p.add_argument('--compiler-root',type=pathlib.Path);a=p.parse_args()
    catalog=json.loads((ROOT/'models.json').read_text(encoding='utf-8'));out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);work=out.parent/'rime-build';work.mkdir(exist_ok=True)
    compiler=a.compiler_root.resolve() if a.compiler_root else work/'compiler'
    if not a.compiler_root:
        archive=work/'compiler.7z';fetch(catalog['compilerArchive'],archive,catalog['compilerArchiveSha256'],32*1024*1024)
        extractor=shutil.which('7z') or str(pathlib.Path(os.environ['ProgramFiles'])/'7-Zip/7z.exe')
        subprocess.run([extractor,'x',str(archive),'-o'+str(compiler),'-y'],check=True)
    deployer=compiler/'dist/bin/rime_deployer.exe'
    if digest(deployer)!=catalog['compilerExeSha256']:raise ValueError('Unexpected compiler executable')
    data=work/'data';data.mkdir(exist_ok=True);(data/'build').mkdir(exist_ok=True)
    for source in catalog['sources']:fetch(source['url'],data/source['file'],source['sha256'],source['bytes'])
    env=os.environ.copy();env['PATH']=str(compiler/'dist/lib')+os.pathsep+env.get('PATH','')
    for name,sha in catalog['schemas'].items():
        schema=ROOT/'schemas'/name
        if digest(schema)!=sha:raise ValueError('Reviewed schema changed: '+name)
        shutil.copyfile(schema,data/name)
        subprocess.run([str(deployer),'--compile',str(data/name),str(data),str(data),str(data/'build')],cwd=data,env=env,check=True)
    reports=[]
    for original in catalog['models']:
        language=original['language'];files={};manifest='format=3\nengine.api=1\ncapability=composition\nengine='+original['engine']+'\nlanguage='+language+'\nversion='+original['version']+'\n'
        for name in original['files']:
            file=data/'build'/name;files[name]={'bytes':file.stat().st_size,'sha256':digest(file)}
            manifest+=f'file.{name}.bytes={files[name]["bytes"]}\nfile.{name}.sha256={files[name]["sha256"]}\n'
        destination=out/(language+'.slpack')
        with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for name,value in [('manifest.properties',manifest.encode()),*[(name,(data/'build'/name).read_bytes()) for name in files]]:
                entry=zipfile.ZipInfo(name,(2026,10,25,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;z.writestr(entry,value)
        reports.append(dict(language=language,engine=original['engine'],version=original['version'],files=files,packBytes=destination.stat().st_size,packSha256=digest(destination)))
    catalog['models']=reports;(out/'models.json').write_text(json.dumps(catalog,indent=2)+'\n',encoding='utf-8')
    with zipfile.ZipFile(out/'sources-and-notices.zip','w',zipfile.ZIP_DEFLATED) as z:
        for source in catalog['sources']:z.write(data/source['file'],'sources/'+source['file'])
        for folder in ['licenses','schemas']:
            for file in (ROOT/folder).iterdir():z.write(file,folder+'/'+file.name)
        z.write(ROOT/'README.md','README.md');z.write(out/'models.json','models.json')
    (out/'SHA256SUMS').write_text(''.join(digest(f)+'  '+f.name+'\n' for f in sorted(out.iterdir()) if f.is_file() and f.name!='SHA256SUMS'),encoding='utf-8')
    print(json.dumps(reports,indent=2))
if __name__=='__main__':main()
