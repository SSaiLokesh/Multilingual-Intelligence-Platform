
pip install -r requirements.txt

python -m spacy download en_core_web_sm

python -c "import spacy; nlp=spacy.load('en_core_web_sm'); print('Model loaded successfully')"

