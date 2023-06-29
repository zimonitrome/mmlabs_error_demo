0.  Clone repo and submodule:
    ```
    https://github.com/zimonitrome/mmlabs_error_demo.git
    cd mmlabs_error_demo
    git submodule update --init --recursive
    ```

1.  Optionally install conda environment.
    **OBS: We actually only need MLFlow in order to reproduce the bug on Databricks as it will install the Conda environment on host.**
    But to run locally you will need to install:
    ```
    conda env create -f openmmlab-environment-gpu.yml
    ```
    or
    ```
    conda env create -f openmmlab-environment-cpu.yml
    ```

2.  Download dataset gtFine_trainvaltest.zip (241MB): https://www.cityscapes-dataset.com/downloads/
    Unzip such that
    ```
    <root>
    ├── mmsegmentation
    ├── guide.md
    └── data
        └── cityscapes
            ├── train
            ├── test
            └── val
    ```

3.  Run locally:
    ```
    python mmsegmentation/tools/train.py stdc1_4xb12-80k_cityscapes-512x1024_custom.py
    ```

4.  Run in Databricks:

    Change `instance_profile_arn` in cluster-4-gpus.json.

    ```
    export MLFLOW_TRACKING_URI=databricks ; mlflow run . --entry-point main --backend databricks --experiment-id <your-experiment-id> --backend-config cluster-4-gpus.json
    ```