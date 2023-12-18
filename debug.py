from mcahelper.cfg import node
from mcahelper.task import CodecTask, Png2yuvTask, PreprocTask, Yuv2pngTask

node.set_node_cfg('node-cfg.toml')

task1 = PreprocTask(seq_name="Tunnel_Train")
task2 = Png2yuvTask(frames=1, pretask=task1)
task3 = CodecTask(vtm_type='AI', frames=1, QP=46, pretask=task2)
task4 = Yuv2pngTask(pretask=task3)

# task1.run()
#task2.run()
#task3.run()
task4.run()
