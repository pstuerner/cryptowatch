from langchain_openai import OpenAIEmbeddings


class CustomOpenAIEmbeddings(OpenAIEmbeddings):

    def __init__(self, openai_api_key, *args, **kwargs):
        super().__init__(openai_api_key=openai_api_key, *args, **kwargs)

    def _embed_documents(self, texts):
        embeddings = [
            self.client.create(input=text, model="text-embedding-ada-002").data[0].embedding 
            for text in texts
        ]
        return embeddings
        
    def __call__(self, input):
        return self._embed_documents(input)