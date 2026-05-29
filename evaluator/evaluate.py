import json
import time
import ollama
import mlflow
from datetime import datetime

PROMPTS_FILE = "prompts/prompts.json"
MODEL_NAME = "llama3"


def load_prompts(path):
    with open(path, "r") as f:
        return json.load(f)


def score_response(response: str) -> int:
    length = len(response.split())
    if length > 80:
        return 9
    elif length > 40:
        return 7
    elif length > 10:
        return 5
    else:
        return 2


def evaluate(model: str = MODEL_NAME):
    prompts = load_prompts(PROMPTS_FILE)

    mlflow.set_experiment("llm-evaluation")

    with mlflow.start_run(run_name=f"{model}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"):
        mlflow.log_param("model", model)
        mlflow.log_param("prompt_count", len(prompts))

        results = []
        total_latency = 0
        total_score = 0
        failures = 0

        for i, prompt in enumerate(prompts):
            print(f"[{i+1}/{len(prompts)}] Prompt: {prompt}")
            try:
                start = time.time()
                response = ollama.chat(
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )
                latency = round(time.time() - start, 2)
                text = response["message"]["content"]
                score = score_response(text)

                print(f"  Latency: {latency}s | Score: {score}")

                results.append({
                    "prompt": prompt,
                    "response": text,
                    "latency": latency,
                    "score": score,
                    "status": "success"
                })

                total_latency += latency
                total_score += score

            except Exception as e:
                print(f"  FAILED: {e}")
                failures += 1
                results.append({
                    "prompt": prompt,
                    "response": "",
                    "latency": 0,
                    "score": 0,
                    "status": "failure"
                })

        n = len(prompts) - failures
        avg_latency = round(total_latency / n, 2) if n > 0 else 0
        avg_score = round(total_score / n, 2) if n > 0 else 0

        mlflow.log_metric("avg_latency", avg_latency)
        mlflow.log_metric("avg_score", avg_score)
        mlflow.log_metric("failures", failures)

        import os
        os.makedirs("reports", exist_ok=True)
        output_path = f"reports/{model}-results.json"
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        mlflow.log_artifact(output_path)

        print(f"\nDone. Avg Latency: {avg_latency}s | Avg Score: {avg_score} | Failures: {failures}")


if __name__ == "__main__":
    evaluate()
