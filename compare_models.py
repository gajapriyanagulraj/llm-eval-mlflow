from evaluator.evaluate import evaluate
from tracker.tracking import print_leaderboard

MODELS = ["llama3"]


def run_comparison():
    print("Starting model comparison...\n")
    for model in MODELS:
        print("=" * 40)
        print(f"Evaluating model: {model}")
        print("=" * 40)
        try:
            evaluate(model=model)
        except Exception as e:
            print(f"Failed to evaluate {model}: {e}")
    print("\n\nAll models evaluated. Generating leaderboard...\n")
    print_leaderboard()


if __name__ == "__main__":
    run_comparison()
