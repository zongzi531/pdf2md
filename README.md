# pdf2md

## install

### 1. install dependencies

```bash
conda create -n pdf2md python=3.10
conda activate pdf2md
python -m pip install tornado==6.4.1
python -m pip install detectron2 --extra-index-url https://wheels.myhloli.com
# setopt no_nomatch
python -m pip install magic-pdf[full]==0.6.2b1
```

### 2. downloading model weights files

```bash
git lfs clone https://huggingface.co/wanderkid/PDF-Extract-Kit
```

### 3. create the configuration file to `~/magic-pdf.json`

```json
{
  "bucket_info": {
    "bucket-name-1": ["ak", "sk", "endpoint"],
    "bucket-name-2": ["ak", "sk", "endpoint"]
  },
  "models-dir": "/**step 2 model clone path**/PDF-Extract-Kit/models",
  "device-mode": "cpu"
}
```

> [FAQ](https://github.com/opendatalab/MinerU/blob/master/docs/FAQ_zh_cn.md)
> 
> [MinerU Installation and Configuration](https://github.com/opendatalab/MinerU/tree/master?tab=readme-ov-file#installation-and-configuration)

## dev

```bash
python src/app.py
```
