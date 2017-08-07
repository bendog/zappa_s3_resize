# Zappa S3 resize
An AWS Lambda to automatically resize S3 bucket image files, using Python3, Zappa and Pillow.

When a file is uploaded to the bucket specified in `zappa_settings.json`, the lambda will execute and create the image sizes specified in `config.py`

## Install

    $ pip install -U -r requirements.txt
    
## Configure

create a `config.py` file, following the example file `config_example.py`, and specify your own aws settings in a `zappa_settings.json` based on `zappa_settings_example.json`

## Deploy

as specified in the [Zappa](https://github.com/Miserlou/Zappa)