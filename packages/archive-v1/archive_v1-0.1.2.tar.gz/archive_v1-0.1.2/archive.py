import pathlib
import datetime
import shutil
from pathlib import Path
import argparse
import toml
from dataclasses import dataclass

CWD = Path().resolve()

@dataclass
class Config:
  root:Path
  archive_dir:Path
  tz:int

CONFIG_FILE='archive.toml'
def get_config() -> Config|None:
  dir=CWD
  while True:
    path=dir/CONFIG_FILE
    if path.exists():break
    par=dir.parent
    if par==dir:return None
    dir=par
  with path.open() as f:
    data=toml.load(f)
    return Config(
      dir,
      dir/data.get('path','.archive'),
      data.get('timezone',0),
    )

def main(targets):
    config=get_config()
    if config is None:
      print(f"{CONFIG_FILE}not found.")
      exit(0)
    tz=datetime.timezone(datetime.timedelta(hours=config.tz))
    today=datetime.datetime.now(tz).strftime("%Y%m%d")
    print(f"Today: {today}")
    root=config.root
    archive=config.archive_dir/today
    for t in targets:
      t = pathlib.Path(t)
      if not t.exists():
        print(f"{t} does not exist.")
        continue
      t_rel=t.resolve().relative_to(root)
      out=archive/t_rel
      ver=1
      while out.exists():
        ver+=1
        out=archive/f"{t_rel}.{ver}"
      out.parent.mkdir(parents=True,exist_ok=True)
      shutil.move(t,out)
      print(f"Moved {t} to {out}")

def cli():
    p=argparse.ArgumentParser('archive')
    p.add_argument('targets',nargs='+')
    main(p.parse_args().targets)

if __name__ == "__main__":
    cli()
