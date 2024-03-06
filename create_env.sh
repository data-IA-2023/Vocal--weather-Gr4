#!/bin/bash
python3.12 -m venv env
source env/bin/activate
pip install -r requirements.txt
python -m spacy download fr_core_news_md
