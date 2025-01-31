from dataclasses import dataclass

from datasets import load_dataset
from rouge import Rouge
from rougek import RougeK

from rouge4llm.utils import AspectType, Result, SplitType
from rouge4llm.summarizer import Summarizer

rouge_f: Rouge = Rouge(
    metrics=["rouge-n", "rouge-l"], max_n=2, apply_best=True, apply_avg=False
)
rougek = RougeK()


@dataclass(frozen=True)
class Evaluator:
    docs: list[str]
    refs: list[list[str]]
    kws_li: list[list[str]]

    def _rougek(self, cands: list[str]) -> float:
        scores = []
        for cand, kws in zip(cands, self.kws_li):
            if len(kws) > 0:
                scores.append(rougek(cand, kws))
            else:
                continue
        return sum(scores) / len(scores)

    def run(self, cands: list[str]) -> Result:
        scores: Result = rouge_f.get_scores(cands, self.refs)
        scores["rougek"] = self._rougek(cands)
        return scores


@dataclass(frozen=True)
class EvaluationRunner:
    evaluator: Evaluator

    def run(self, summarizer: Summarizer) -> tuple[Result, list[str]]:
        cands = summarizer.summarize(self.evaluator.docs)
        return self.evaluator.run(cands), cands


def load_scitldr_evaluator(split: SplitType) -> Evaluator:
    ds = load_dataset("sobamchan/scitldr-kws", split=split)
    docs: list[str] = [" ".join(sents) for sents in ds["source"]]
    refs_li: list[list[str]] = ds["target"]
    kws_li: list[list[str]] = ds["keywords"]

    evaluator = Evaluator(docs=docs, refs=refs_li, kws_li=kws_li)

    return evaluator


def load_aclsum_evaluator(aspect: AspectType, split: SplitType) -> Evaluator:
    ds = load_dataset(f"sobamchan/aclsum-{aspect}-kws", split=split)
    docs: list[str] = [" ".join(sents) for sents in ds["source"]]
    refs_li: list[list[str]] = ds["target"]
    kws_li: list[list[str]] = ds["keywords"]

    evaluator = Evaluator(docs=docs, refs=refs_li, kws_li=kws_li)

    return evaluator
