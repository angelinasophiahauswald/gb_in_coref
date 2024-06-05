import coreferee, spacy
nlp = spacy.load('de_core_news_sm')
nlp.add_pipe('coreferee')
doc = nlp('Meine Schwester hat einen Hund. Sie liebt ihn sehr.')
doc._.coref_chains.print()