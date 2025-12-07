# Add to forecasting/experiments.py for fine-tuned TimeGPT comparison

import os
from pathlib import Path
from nixtla import NixtlaClient


def load_finetuned_model_id():
    """Load the fine-tuned model ID from artifacts"""
    model_id_file = Path("forecasting/artifacts/timegpt_finetune/finetune_model_id.txt")

    if not model_id_file.exists():
        print("Warning: Fine-tuned model ID not found")
        print(f"Run fine-tuning first: python forecasting/timegpt_finetune_job.py")
        return None

    with open(model_id_file, "r") as f:
        model_id = f.read().strip()

    return model_id


def run_timegpt_finetuned_forecast(df, horizon, freq):
    """Run forecast with fine-tuned TimeGPT model"""

    model_id = load_finetuned_model_id()
    if not model_id:
        return None

    # Ensure nixtla package installed and API key set
    from nixtla import NixtlaClient

    client = NixtlaClient(api_key=os.getenv("NIXTLA_API_KEY"))

    print(f"Running TimeGPT forecast with fine-tuned model: {model_id}")

    forecast = client.forecast(df=df, h=horizon, freq=freq, finetune_id=model_id)

    return forecast


def run_comparison_experiment():
    """Compare TimeGPT zero-shot, fine-tuned, and baselines"""

    # ... existing setup code ...

    results = []

    # 1. TimeGPT Zero-Shot (baseline)
    if NIXTLA_API_KEY:
        print("\n1. Running TimeGPT Zero-Shot...")
        forecast_zeroshot = run_timegpt_zeroshot(test_df, horizon, freq)
        metrics_zeroshot = calculate_metrics(actual, forecast_zeroshot)
        results.append({"model": "TimeGPT Zero-Shot", **metrics_zeroshot})

    # 2. TimeGPT Fine-Tuned (custom model)
    if NIXTLA_API_KEY:
        print("\n2. Running TimeGPT Fine-Tuned...")
        forecast_finetuned = run_timegpt_finetuned_forecast(test_df, horizon, freq)
        if forecast_finetuned is not None:
            metrics_finetuned = calculate_metrics(actual, forecast_finetuned)
            results.append({"model": "TimeGPT Fine-Tuned", **metrics_finetuned})

    # 3. StatsForecast Baselines
    print("\n3. Running StatsForecast baselines...")
    # ... AutoETS, AutoARIMA, SeasonalNaive ...

    # 4. Generate comparison table
    results_df = pd.DataFrame(results)
    print("\n" + "=" * 60)
    print("COMPARISON RESULTS")
    print("=" * 60)
    print(results_df.to_string(index=False))

    # Highlight best model
    best_model = results_df.loc[results_df["smape"].idxmin(), "model"]
    print(f"\n🏆 Best model: {best_model}")

    return results_df
