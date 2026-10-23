"""Fetch actual pinned public ESC-10 WAV files, fail closed on license or metadata mismatches."""
import csv,json,re,urllib.request
from pathlib import Path

DOCUMENT=json.loads(Path("sources.json").read_text())
ROOT="https://raw.githubusercontent.com/karolpiczak/ESC-50/"+DOCUMENT["provenance"]["commit"]+"/"

def get(path,maxbytes=1500000):
    req=urllib.request.Request(ROOT+path,headers={"User-Agent":"HarborResearch-Noncommercial-DEV/0.1"})
    with urllib.request.urlopen(req,timeout=30) as response:
        data=response.read(maxbytes+1)
    if len(data)>maxbytes:raise ValueError("Unexpected source size: "+path)
    return data

def main():
    metadata=get("meta/esc50.csv").decode("utf8")
    license_text=get("LICENSE").decode("utf8")
    index={row["filename"]:row for row in csv.DictReader(metadata.splitlines())}
    folder=Path("clip_cache");folder.mkdir(exist_ok=True)
    for x in DOCUMENT["sources"]:
        filename=x["filename"];row=index.get(filename)
        if (not row or row["category"]!=x["category"] or row["esc10"]!="True"
            or row["src_file"]!=x["source_id"] or
            int(row["fold"])!=(1 if x["role"]=="train" else int(filename[0]))):
            raise ValueError("Class, fold or source identity mismatch: "+filename)
        original=re.sub(r"-\d+\.wav$",".ogg",filename)
        lines=[line for line in license_text.splitlines() if line.startswith("- ["+original+"]")]
        if len(lines)!=1 or not lines[0].endswith("by "+x["author"]+" [CC0]"):
            raise ValueError("Original CC0 clip attribution not verified: "+filename)
        audio=get("audio/"+filename)
        if len(audio)<1024 or audio[:4]!=b"RIFF":
            raise ValueError("Expected actual WAV bytes, not LFS pointers: "+filename)
        (folder/filename).write_bytes(audio)
        print("VERIFIED_SOURCE",filename,len(audio),"bytes, individual source CC0, author",x["author"])
    print("VERIFIED_ESC10_METADATA_AND_LICENSE count",len(DOCUMENT["sources"]))

if __name__=="__main__":main()
