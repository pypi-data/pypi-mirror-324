import logging

from tinysmith.llm.adapters import LLMAdapter, SystemMessage, UserMessage
from tinysmith.llm.utils import json_load_list
from tinysmith.modules.modules import Module
from tinysmith.modules.rag.utils import EmbeddedDocs
from tinysmith.orchestrator.state import State

logger = logging.getLogger(__name__)

rag_question_prompt = """You are a question generator for a knowledge retrieval task. 
The user is an expert CTF player that just ran a command and sends you the challenge, command, and its output.
Generate a list of max. three questions about the output. Those questions will be used to search all 
CTF writeups and the most relevant ones will be returned to help the player solve the challenge.

- Use keywords of the broader topics in which the output is likely embedded. 
- Use program or library names and error messages that are likely to be found in the writeup. 
- Don't include very specific values that are unlikely to be found in existing writeups.

Don't mention CTF or writeups in the questions. Phrase the questions as if you were asking a search engine.
Pose the question as clear and concise as possible.

### Format
Please ouput your answer as the following JSON scheme:
```
[
    "<question 1>",
    "<queston ...>
] 
```
If there are no interesting questions to answer for a message, respond with the following JSON scheme:
```
[]
```"""

class RagWithQueryGenerator(Module):
    """
    Module that queries a knowledgebase with generated questions about the command and result. The 
    resulting documents are provided to the agent through the state object in the module's 
    namespace.
    """

    def __init__(self, 
                 name:str,
                 embedding_model: str,
                 embedding_path: str,
                 llm_adapter: None|LLMAdapter = None,
                 k: int = 3):
        """Create a new RAGWithQueryGenerator module.

        Args:
            name (str): Name of the module.
            embedding_model (str): Name of the embedding model.
            embedding_path (str): Path to the embedding model.
            llm_adapter (LLMAdapter): The LLMAdapter that generates queries related to the command
                                      and response. 
            k (int): Number of documents to retrieve.
        """
        self.name = name
        assert llm_adapter is not None, "LLMAdapter must be provided."
        self.llm_adapter = llm_adapter
        
        chunks_path = embedding_path.replace('.npz', '_docs.csv')
        self.docs = EmbeddedDocs(embedding_model=embedding_model,
                                 embedding_path=embedding_path, 
                                 chunks_path=chunks_path)
        self.k = k

    def preprocessing(self, obs: str, state: State) -> None:
        if not obs:
            return
        sys_prompt = SystemMessage(rag_question_prompt)
        query_prompt = UserMessage(f"Challenge:{state.get('challenge_description')}\n\nCommand > {state.get_response()}: \n{obs}")
        response = self.llm_adapter.generate([sys_prompt, query_prompt])
        queries = json_load_list(response)
        logger.debug(f"RAGWithQueryGenerator: {response}")
        if len(queries) == 0:
            return
        if len(queries) > 3:
            queries = queries[:3]
        elif len(queries) > self.k:
            queries = queries[:self.k]

        j = self.k // len(queries)
        result = []
        for query in queries:
            logger.debug(f"Querying RAG with {query}")
            result.extend([doc['result'] for doc in self.docs.query(query, j)])
        
        result = list(set(result))

        logger.debug(f"RAGWithQueryGenerator: {result}")
        rag_module = {}
        rag_module['knowledge'] = result
        state.set(self.name, rag_module)

    def postprocessing(self, response: str, state: State) -> None:
        pass

    def reset(self):
        pass


