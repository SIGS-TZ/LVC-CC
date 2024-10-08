import csv
import json

from lvccc.config import update_config
from lvccc.helper import mkdir
from lvccc.task import (
    CodecTask,
    ComposeTask,
    RenderTask,
    Yuv2imgTask,
    YuvCopyTask,
    gen_infomap,
)

config = update_config('config.toml')

summary_dir = config.path.output / 'summary'
src_dir = summary_dir / 'tasks'
dst_dir = summary_dir / 'csv'
mkdir(dst_dir)

infomap = gen_infomap(src_dir)


with (dst_dir / "anchor.csv").open("w", encoding="utf-8", newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    headers = [
        'Sequence',
        'QP',
        'Bitrate',
        'LLPSNR-Y',
        'LLPSNR-U',
        'LLPSNR-V',
        'MVPSNR-Y',
        'MVPSNR-U',
        'MVPSNR-V',
    ]
    csv_writer.writerow(headers)

    for seq_name in config.cases.seqs:
        tcopy = YuvCopyTask(seq_name=seq_name, frames=config.frames)

        for vtm_type in config.cases.vtm_types:
            for qp in config.QP.anchor.get(seq_name, []):
                tcodec = CodecTask(vtm_type=vtm_type, qp=qp).with_parent(tcopy)
                tyuv2img = Yuv2imgTask().with_parent(tcodec)
                trender = RenderTask().with_parent(tyuv2img)
                tcompose = ComposeTask().with_parent(trender)

                json_path = src_dir / tcodec.full_tag / "psnr.json"
                if not json_path.exists():
                    csv_writer.writerow(['Not Found'] + [0] * (len(headers) - 1))

                with json_path.open() as f:
                    metrics: dict = json.load(f)

                csv_writer.writerow(
                    [
                        seq_name,
                        qp,
                        metrics['bitrate'],
                        metrics['llpsnr_y'],
                        metrics['llpsnr_u'],
                        metrics['llpsnr_v'],
                        metrics['mvpsnr_y'],
                        metrics['mvpsnr_u'],
                        metrics['mvpsnr_v'],
                    ]
                )
