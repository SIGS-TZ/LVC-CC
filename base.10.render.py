import subprocess
from pathlib import Path

from vvchelper.command import render
from vvchelper.config.raytrix import RaytrixCfg
from vvchelper.config.self import from_file
from vvchelper.logging import get_logger
from vvchelper.utils import mkdir, path_from_root

log = get_logger()

all_cfg = from_file(Path('pipeline.toml'))
cfg = all_cfg['base']['render']

src_dirs = path_from_root(all_cfg, all_cfg['base']['raw2png']['dst'])
log.debug(f"src_dirs: {src_dirs}")
dst_dirs = path_from_root(all_cfg, cfg['dst'])
log.debug(f"dst_dirs: {dst_dirs}")

for src_dir in src_dirs.iterdir():
    if not src_dir.is_dir():
        continue

    seq_name = src_dir.name
    log.debug(f"processing seq: {seq_name}")

    src_dir = src_dirs / seq_name
    dst_dir = dst_dirs / seq_name
    mkdir(dst_dir)

    rlc_cfg_rp = cfg['rlc_cfg'].format(seq_name=seq_name)
    rlc_cfg_rp = path_from_root(all_cfg, rlc_cfg_rp)
    rlc_cfg = RaytrixCfg.from_file(rlc_cfg_rp)

    rlc_cfg.Calibration_xml = str(rlc_cfg_rp.with_name('calibration.xml'))
    rlc_cfg.RawImage_Path = str(src_dir / "frame#%03d.png")
    rlc_cfg.Output_Path = str(dst_dir / "frame#%03d")
    rlc_cfg.Isfiltering = 1
    rlc_cfg.end_frame = 30

    rlc_cfg_wp = dst_dir / 'rlc.cfg'
    rlc_cfg.to_file(rlc_cfg_wp)

    cmds = render.build(
        all_cfg['program']['rlc'],
        rlc_cfg_wp,
    )
    subprocess.run(cmds)
