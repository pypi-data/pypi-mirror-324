from __future__ import annotations

import json
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Literal

from saea_benchmark.align_seqs import compute_identity, get_max_identities
from saea_benchmark.model_eval import evaluate_with_model


class BenchmarkExperiment:
    def __init__(
        self,
        full_fasta_file_path: str,
        split_file_path: str,
        suite: list[Literal["blast", "model"]] = ["blast", "model"],
    ):
        self.full_fasta_file_path = full_fasta_file_path
        self.split_file_path = split_file_path
        self.suite = suite
        if not self.suite:
            raise ValueError("Please provide at least one benchmarking suite")
        self.results = None

    def run_blast_benchmark(
        self,
        max_identity_threshold: float = 0.8,
        exclude_clusters: list[int] = None,
        **kwargs,
    ):
        identities = get_max_identities(
            self.full_fasta_file_path, self.split_file_path, **kwargs
        )
        output = compute_identity(
            input_df=identities,
            threshold=max_identity_threshold,
            exclude_clusters=exclude_clusters,
        )
        output["threshold"] = max_identity_threshold
        return output

    def run_model_benchmark(self, **kwargs):
        output = evaluate_with_model(split_df_path=self.split_file_path, **kwargs)
        output["metric"] = kwargs["metric_name"]
        output["seed"] = kwargs.get("seed", 42)
        return output

    def run_suite(self, arguments: dict[str, Any], concurrent: bool = True):
        def run_blast() -> dict:
            return self.run_blast_benchmark(**arguments["blast"])

        def run_model() -> dict:
            required = ["train_val_adata_path", "test_adata_path", "metric_name"]
            if not all(arguments["model"].get(arg) for arg in required):
                raise ValueError("Missing required model benchmark arguments")
            return self.run_model_benchmark(**arguments["model"])

        tasks: list[Callable] = []
        if "blast" in self.suite:
            tasks.append(run_blast)
        if "model" in self.suite:
            tasks.append(run_model)

        if not tasks:
            return {}

        if concurrent:
            with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
                results = list(executor.map(lambda f: f(), tasks))
        else:
            results = [task() for task in tasks]

        self.results = self._merge_results(results)
        return self.results

    def _merge_results(self, results):
        all_keys = set()
        for result in results:
            all_keys.update(result.keys())

        final_dict = {key: {} for key in all_keys}
        for result in results:
            for idx, metrics in result.items():
                if isinstance(metrics, dict):
                    final_dict[idx].update(
                        {k: v for k, v in metrics.items() if not isinstance(v, dict)}
                    )
                else:
                    final_dict[idx] = metrics
        return final_dict

    def save_results(self, output_file_path: str):
        if not self.results:
            raise ValueError("No results to save. Run the experiment first.")
        _, ext = output_file_path.rsplit(".", 1)
        assert ext == "json", "Please provide a JSON file path"
        with open(output_file_path, "w") as f:
            json.dump(self.results, f, indent=4)
