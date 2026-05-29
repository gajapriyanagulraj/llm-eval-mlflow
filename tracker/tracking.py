import mlflow
import json
import os


def get_all_runs(experiment_name: str = "llm-evaluation") -> list:
    client = mlflow.tracking.MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        print(f"No experiment found with name: {experiment_name}")
        return []
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.avg_score DESC"]
    )
    results = []
    for run in runs:
        results.append({
            "run_id": run.info.run_id,
            "run_name": run.info.run_name,
            "model": run.data.params.get("model", "unknown"),
            "avg_score": run.data.metrics.get("avg_score", 0),
            "avg_latency": run.data.metrics.get("avg_latency", 0),
            "failures": run.data.metrics.get("failures", 0),
        })
    return results


def print_leaderboard():
    runs = get_all_runs()
    if not runs:
        print("No runs found. Run evaluate.py first.")
        return
    print("\n===== Model Leaderboard =====")
    print(f"{'Model':<20} {'Score':>7} {'Latency':>10} {'Failures':>10}")
    print("-" * 52)
    for r in runs:
        print(
            f"{r['model']:<20} "
            f"{r['avg_score']:>7.2f} "
            f"{r['avg_latency']:>9.2f}s "
            f"{int(r['failures']):>10}"
        )
    os.makedirs("reports", exist_ok=True)
    with open("reports/leaderboard.json", "w") as f:
        json.dump(runs, f, indent=2)
    print("\nSaved to reports/leaderboard.json")


if __name__ == "__main__":
    print_leaderboard()
