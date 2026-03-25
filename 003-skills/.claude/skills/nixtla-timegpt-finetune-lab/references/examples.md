## Examples

### Example 1: Basic Fine-Tuning

```bash
python {baseDir}/scripts/prepare_finetune_data.py \
    --input sales.csv --output train.csv

python {baseDir}/scripts/submit_finetune.py \
    --train train.csv \
    --model_name "my-sales-model" \
    --horizon 14
```

**Output**:
```
Fine-tuning job submitted: job_abc123
Model ID saved to: artifacts/finetune_model_id.txt
```

### Example 2: Compare Zero-Shot vs Fine-Tuned

```bash
python {baseDir}/scripts/compare_finetuned.py \
    --test test.csv \
    --finetune_id my-sales-model
```

**Output**:
```
Model Comparison:
  TimeGPT Zero-Shot: SMAPE=12.3%
  TimeGPT Fine-Tuned: SMAPE=8.7%
  Improvement: 29.3%
```
