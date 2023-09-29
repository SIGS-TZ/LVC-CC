import subprocess
from pathlib import Path

from vvchelper.command import png2yuv420
from vvchelper.config.self import from_file
from vvchelper.logging import get_logger
from vvchelper.utils import get_src_pattern, mkdir, path_from_root

log = get_logger()

all_cfg = from_file(Path('pipeline.toml'))
cfg = all_cfg['pre']['pre2yuv']

src_dirs = path_from_root(all_cfg, all_cfg['pre']['preprocess']['dst'])
log.debug(f"src_dirs: {src_dirs}")
dst_dir = path_from_root(all_cfg, cfg['dst'])
mkdir(dst_dir)
log.debug(f"dst_dirs: {dst_dir}")

for src_dir in src_dirs.iterdir():
    if not src_dir.is_dir():
        continue

    seq_name = src_dir.name
    log.debug(f"processing seq: {seq_name}")

    fname_sample = next(src_dir.glob('*.png')).name

    cmds = png2yuv420.build(
        all_cfg['program']['ffmpeg'],
        src_dir / get_src_pattern(fname_sample),
        (dst_dir / seq_name).with_suffix('.yuv'),
    )
    subprocess.run(cmds)
