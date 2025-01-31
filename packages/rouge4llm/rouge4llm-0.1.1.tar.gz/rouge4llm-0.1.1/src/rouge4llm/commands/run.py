from argparse import ArgumentParser
import sienna
from dataclasses import dataclass
from pathlib import Path

from rouge4llm.evaluator import (
    EvaluationRunner,
    load_aclsum_evaluator,
    load_scitldr_evaluator,
)
from rouge4llm.summarizer import LLaMASummarizer
from rouge4llm.utils import AspectType, DatasetType, SplitType


@dataclass(frozen=True)
class Config:
    model_name: str
    sys_inst: str
    dataset: DatasetType
    aspect: AspectType
    split: SplitType
    output_dir: Path | None


def parse_args() -> Config:
    parser = ArgumentParser()
    parser.add_argument("--model-name", type=str, required=True)
    parser.add_argument("--sys-inst", type=str, required=True)
    parser.add_argument("--dataset", type=DatasetType.parse_arg, required=True)
    parser.add_argument(
        "--aspect-type", type=AspectType.parse_arg, required=False, default=None
    )
    parser.add_argument(
        "--split", type=SplitType.parse_arg, required=False, default=None
    )
    parser.add_argument("--output-dir", type=str, required=False, default=None)
    args = parser.parse_args()
    return Config(
        model_name=args.model_name,
        sys_inst=args.sys_inst,
        dataset=args.dataset,
        aspect=args.aspect_type,
        split=args.split,
        output_dir=Path(args.output_dir) if args.output_dir is not None else None,
    )


def run():
    config = parse_args()

    match config.dataset:
        case DatasetType.scitldr:
            evaluator = load_scitldr_evaluator(config.split)
        case DatasetType.aclsum:
            evaluator = load_aclsum_evaluator(config.aspect, config.split)

    summarizer = LLaMASummarizer.load(
        config.model_name, system_instruction=config.sys_inst
    )

    runner = EvaluationRunner(evaluator)

    result, cands = runner.run(summarizer)

    if config.output_dir:
        sienna.save(result, config.output_dir / "result.json")
        sienna.save(cands, config.output_dir / "candidate_summaries.txt")
    else:
        print(result)


if __name__ == "__main__":
    run()
