import csv
import logging
import sys

import numpy as np
import torch
from torch.functional import Tensor
import torch.nn.functional
from transformers import AutoModel, AutoTokenizer

logger = logging.getLogger(__name__)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
csv.field_size_limit(sys.maxsize)

class EmbeddedDocs:
    """A class that encapsulates embeddings of documents and all interactions with them.
    It can be used to add documents to the index, query the index, and load embeddings from a file.
    """
    def __init__(self, embedding_model: str, 
                 embedding_path: None|str = None, 
                 chunks_path: None|str = None):
        self._docs = []
        self._docs_embeddings = np.empty(shape=(0,1024))

        self.tokenizer = AutoTokenizer.from_pretrained(embedding_model)
        self.model = AutoModel.from_pretrained(embedding_model).to(device)

        self.is_loaded = False
        if embedding_path:
            assert chunks_path, "Chunks path must be provided if embedding path is provided."
            self.is_loaded = True
            self.chunks_path = chunks_path
            self._load_embeddings(embedding_path)


    def query(self, query: str, k=5) -> list[dict]:
        if not self._docs:
            raise ValueError("No documents have been added to the index.")
        query_embedding = self._embed_query(query)
        similarity_scores = self._cosine_similarity(query_embedding, self._docs_embeddings)[0]
        m = k*2
        top_m_docs = similarity_scores.argsort()[-m:][::-1]
        if self.is_loaded:
            logger.debug(f"Is loaded. Reading chunks from {self.chunks_path}")
            result = [{
                'score': similarity_scores[i],
                'result': self._read_chunk(self._docs[i])
                } for i in top_m_docs]
        else:
            logger.debug(f"Is not loaded. Returning indices.")
            result = [{
                'score': similarity_scores[i], 
                'result': self._docs[i]
                } for i in top_m_docs]

        # TODO: remove this before release
        # - remove m parameter above
        censor_list = []
        for i,r in enumerate(result):
            if 'picoctf' in r['result'].lower():
                censor_list.append(i)
        result = [r for i,r in enumerate(result) if i not in censor_list]
        results_top_k = result[:k]

            
        return results_top_k


    def add_docs(self, docs: list[str]):
        logger.debug(f"Adding {len(docs)} docs to index")
        self._docs.extend(docs)
        new_embeddings = self._embed_docs(docs)
        self._docs_embeddings = np.concatenate((self._docs_embeddings, new_embeddings), axis=0)


    def _embed_docs(self, docs: list[str]) -> np.ndarray:
        docs = [f"passage: {d}" for d in docs] 
        return self._embed(docs)


    def _load_embeddings(self, path):
        logger.info(f'Loading embeddings from {path}')
        try:
            loaded_file = np.load(path)
            self._docs = loaded_file['docs'].tolist()
            self._docs_embeddings = loaded_file['docs_embeddings']
        except FileNotFoundError:
            logger.error(f"Embeddings file {path} not found. No embeddings loaded.") 


    def _cosine_similarity(self, query_embedding: np.ndarray, docs_embedding: np.ndarray) -> np.ndarray:
        dot_product = np.dot(query_embedding, docs_embedding.T)
        return dot_product


    def _embed_query(self, query: str) -> np.ndarray:
        query = f"query: {query}"
        return self._embed([query])


    @torch.no_grad()
    def _embed(self, docs: list[str]) -> np.ndarray:
        tokens_dict = self.tokenizer(docs, padding=True, truncation=True, return_tensors='pt').to(device)
        outputs = self.model(**tokens_dict)
        embeddings = self._average_pool(outputs.last_hidden_state, tokens_dict['attention_mask'])
        embeddings_normalized = torch.nn.functional.normalize(embeddings, p=2, dim=1)
        return embeddings_normalized.cpu().numpy()


    def _average_pool(self, last_hidden_states: Tensor,
                     attention_mask: Tensor) -> Tensor:
        last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
        return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


    def _read_chunk(self, number: int) -> str|None:
        with open(self.chunks_path, 'r') as file:
            reader = csv.DictReader(file)
            next(reader)  
            for row in reader:
                if row['index'] == str(number):
                    return row['doc']
        return None

