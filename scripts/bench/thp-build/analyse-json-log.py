#!/usr/bin/env python3

import json
import sys

# --- CONFIGURATION ---
# Set how many top changed files you want to see
N = 20
# ---------------------

def extract_instructions(file_path):
  """Parses a single JSON log and returns a dict of {module_name: instruction_count}."""
  module_data = {}
  try:
    with open(file_path, 'r', encoding='utf-8') as f:
      for line in f:
        line = line.strip()
        if not line:
          continue
        try:
          entry = json.loads(line)
          metric = entry.get("metric", "")

          # Target: "build/module/<Name>//instructions"
          if metric.startswith("build/module/") and metric.endswith("//instructions"):
            name = metric[len("build/module/") : -len("//instructions")]
            value = entry.get("value")
            if value is not None:
              module_data[name] = value
        except json.JSONDecodeError:
          continue
  except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    sys.exit(1)
  return module_data

def compare_logs(file1, file2):
  # Load data
  base_metrics = extract_instructions(file1)
  new_metrics = extract_instructions(file2)

  diffs = []
  total_change = 0.0

  # Calculate differences for modules present in both files
  for name, new_val in new_metrics.items():
    if name in base_metrics:
      old_val = base_metrics[name]
      diff = new_val - old_val
      diffs.append((name, diff))
      total_change += diff
    else:
      sys.stderr.write(f"Module {name} missing in first run\n")
      pass

  # Sort by absolute value of difference, descending
  diffs.sort(key=lambda x: abs(x[1]), reverse=True)

  # Calculate sub-total for the top N files
  top_n_diffs = diffs[:N]
  subset_change = sum(d[1] for d in top_n_diffs)

  # --- Summary Output ---
  print("-" * 40)
  print(f"File 1 ({file1}): {len(base_metrics)} modules")
  print(f"File 2 ({file2}): {len(new_metrics)} modules")
  print(f"Total Instruction Change: {total_change/1e9:+.2f}G")
  #print(f"Total Instruction Change: {total_change:+,g}")
  print(f"Top {len(top_n_diffs)} Net Change: {subset_change/1e9:+.2f}G")
  print("-" * 40)

  for name, diff in top_n_diffs:
    if diff != 0:
      print(f"('{name}', {diff/1e9:+.2f})G")

if __name__ == "__main__":
  if len(sys.argv) != 3:
    print("Usage: python compare_instructions.py <base_log.json> <new_log.json>")
  else:
    compare_logs(sys.argv[1], sys.argv[2])
