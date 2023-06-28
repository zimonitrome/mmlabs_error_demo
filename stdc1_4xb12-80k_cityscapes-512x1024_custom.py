_base_ = [
    # 'mmsegmentation/configs/_base_/models/stdc.py',
    'custom_config/stdc_custom.py',
    'mmsegmentation/configs/_base_/datasets/cityscapes.py',
    'mmsegmentation/configs/_base_/default_runtime.py',
    'mmsegmentation/configs/_base_/schedules/schedule_80k.py'
]
crop_size = (512, 1024)
data_preprocessor = dict(size=crop_size)
model = dict(data_preprocessor=data_preprocessor)
param_scheduler = [
    dict(type='LinearLR', by_epoch=False, start_factor=0.1, begin=0, end=1000),
    dict(
        type='PolyLR',
        eta_min=1e-4,
        power=0.9,
        begin=1000,
        end=80000,
        by_epoch=False,
    )
]

# Need to override tta_pipeline because it's too long for mlflow to log
img_ratios = [0.5, 0.75, 1.0, 1.25, 1.5]
tta_pipeline = [
    dict(type='LoadImageFromFile', backend_args=None),
    dict(
        type='TestTimeAug',
        transforms=[
            [
                dict(type='Resize', scale_factor=r, keep_ratio=True)
                for r in img_ratios
            ],
            [
                dict(type='RandomFlip', prob=0., direction='horizontal'),
                dict(type='RandomFlip', prob=1., direction='horizontal')
            ], [dict(type='LoadAnnotations')], [dict(type='PackSegInputs')]
        ])
]
train_dataloader = dict(dataset=dict(seg_map_suffix="_gtFine_labelIds.png", img_suffix="_leftImg8bit.png.jpg"))
val_dataloader = dict(dataset=dict(seg_map_suffix="_gtFine_labelIds.png", img_suffix="_leftImg8bit.png.jpg"))
test_dataloader = val_dataloader

train_cfg = dict(max_iters=8, val_interval=2)
default_hooks = dict(
    checkpoint=dict(interval=2)
)

visualizer = dict(
    type="SegLocalVisualizer", vis_backends=[dict(type="MLflowVisBackend", save_dir="mlruns", artifact_suffix=(".json", ".py", "yaml", ".pth"))]
)