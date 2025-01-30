from dataclasses import dataclass

from tqdm import tqdm
from transformers import Pipeline, pipeline


@dataclass(frozen=True)
class Summarizer:
    def summarize(self, docs: list[str]) -> list[str]:
        raise NotImplementedError()


@dataclass(frozen=True)
class LLaMASummarizer:
    pipe: Pipeline
    system_instruction: str

    @classmethod
    def load(cls, model_name: str, system_instruction: str) -> "LLaMASummarizer":
        pipe = pipeline("text-generation", model=model_name)
        return cls(pipe=pipe, system_instruction=system_instruction)

    def summarize(self, docs: list[str]) -> list[str]:
        cands = []
        for doc in tqdm(docs):
            msg = [
                {"role": "system", "content": self.system_instruction},
                {"role": "user", "content": doc},
            ]
            outputs = self.pipe(
                msg, max_new_tokens=128, do_sample=False, top_p=None, temperature=None
            )
            cand = outputs[0]["generated_text"][-1]["content"]
            cands.append(cand)
            print(cand)
        return cands
