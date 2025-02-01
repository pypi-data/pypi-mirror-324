class TopicModelingData:
    def __init__(self):
        self._base_model = None
        self._model_type = None
        self._docs = None
        self._tokenized_docs = None
        self._dictionary = None
        self._corpus = None
        self._pred_topics = None

    @property
    def base_model(self):
        return self._base_model

    @property
    def model_type(self):
        return self._model_type

    @property
    def tokenized_docs(self):
        return self._tokenized_docs

    @property
    def dictionary(self):
        return self._dictionary

    @property
    def corpus(self):
        return self._corpus

    @property
    def pred_topics(self):
        return self._pred_topics

    @property
    def docs(self):
        return self._docs

    @base_model.setter
    def base_model(self, value):
        self._base_model = value

    @model_type.setter
    def model_type(self, value):
        self._model_type = value

    @tokenized_docs.setter
    def tokenized_docs(self, value):
        self._tokenized_docs = value

    @dictionary.setter
    def dictionary(self, value):
        self._dictionary = value

    @corpus.setter
    def corpus(self, value):
        self._corpus = value

    @pred_topics.setter
    def pred_topics(self, value):
        self._pred_topics = value

    @docs.setter
    def docs(self, value):
        self._docs = value