import subprocess
from pathlib import Path

from vvchelper.command import png2yuv420
from vvchelper.config.self import from_file
from vvchelper.logging import get_logger
from vvchelper.utils import get_src_pattern, mkdir, path_from_root

log = get_logger()

all_cfg = from_file("pipeline.toml")
cfg = all_cfg['wopre']['raw2yuv']

src_dirs: Path = path_from_root(all_cfg, cfg['src'])
log.debug(f"src_dirs: {src_dirs}")
dst_dir: Path = path_from_root(all_cfg, cfg['dst'])
log.debug(f"dst_dir: {dst_dir}")
mkdir(dst_dir)


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
