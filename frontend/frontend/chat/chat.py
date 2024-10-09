from openai import OpenAI
from frontend.utils.env import OPENAI_KEY
from frontend.utils.prompts import SYSTEM_PROMPT
from frontend.db.chroma import ChromaDB

class ChatLLM:
    def __init__(self) -> None:
        self.system_prompt = {
            'role': 'system',
            'content': SYSTEM_PROMPT
        }
        self.msg_chain = [self.system_prompt]
        self.client = OpenAI(
            api_key=OPENAI_KEY
        )
        self.chroma = ChromaDB()
    
    def chat(self, prompt, retrieve=False, filter={}):
        if retrieve:
            docs = self.chroma.query(q=prompt, k=10, filter=filter)
            s = "REQUEST: {prompt}\nSOURCES:\n{sources}"
            docs_dict = {i+1:{"url": d.metadata["url"], "content": d.page_content} for i, d in enumerate(docs)}
            sources = "\n".join([f"[{k}]({v['url']}): {v['content'].replace('\n',' ')}" for k, v in docs_dict.items()])
            prompt = s.format(prompt=prompt, sources=sources)
            
            response = self.client.chat.completions.create(
                messages=self.msg_chain + [{"role": "user", "content": prompt}],
                model="gpt-4o-mini"
            )
        else:
            response = self.client.chat.completions.create(
                messages=self.msg_chain + [{"role": "user", "content": prompt}],
                model="gpt-4o-mini"
            )
        
        response = response.choices[0].message.content

        self.msg_chain.append({"role":"user", "content": prompt})
        self.msg_chain.append({"role":"assistant", "content": response})
        
        return response