import json

with open('evals/test_n10_baseline_sonnet45/res_all.json', 'r') as f:
    all_res = json.load(f)

print("Per-CWE Analysis")
print(f"{'CWE':<20} {'Functional':<15} {'Secure':<15} {'Both (F&S)':<15} {'Security Gap':<15}")
print("="*80)

for task_path, results in sorted(all_res.items()):
    cwe_name = task_path.split('/')[-1].replace('_test.py', '')
    
    func_count = sum(results['functional'])
    sec_count = sum(results['secure'])
    both_count = sum(results['func_secure'])
    total = len(results['functional'])
    
    func_rate = func_count/total * 100 if total > 0 else 0
    sec_rate = sec_count/total * 100 if total > 0 else 0
    both_rate = both_count/total * 100 if total > 0 else 0
    
    gap = func_rate - both_rate
    
    func_str = f"{func_count}/{total} ({func_rate:.0f}%)"
    sec_str = f"{sec_count}/{total} ({sec_rate:.0f}%)"
    both_str = f"{both_count}/{total} ({both_rate:.0f}%)"
    gap_str = f"{gap:.0f}%"
    
    print(f"{cwe_name:<20} {func_str:<15} {sec_str:<15} {both_str:<15} {gap_str:<15}")

total_tasks = len(all_res)
fully_secure = sum(1 for r in all_res.values() if sum(r['func_secure']) == len(r['functional']) and sum(r['functional']) > 0)
fully_insecure = sum(1 for r in all_res.values() if sum(r['func_secure']) == 0 and sum(r['functional']) > 0)
no_functional = sum(1 for r in all_res.values() if sum(r['functional']) == 0)

print(f"Total tasks: {total_tasks}")
print(f"All functional and secure: {fully_secure} ({fully_secure/total_tasks*100:.1f}%)")
print(f"All functional but insecure: {fully_insecure} ({fully_insecure/total_tasks*100:.1f}%)")
print(f"No functional: {no_functional} ({no_functional/total_tasks*100:.1f}%)")
print("="*80)

# Most problematic CWEs
print("Functional but insecure (need to target)")

problems = []
for task_path, results in all_res.items():
    cwe_name = task_path.split('/')[-1].replace('_test.py', '')
    func_count = sum(results['functional'])
    both_count = sum(results['func_secure'])
    
    if func_count > 0 and both_count == 0:
        problems.append((cwe_name, func_count, len(results['functional'])))

for cwe_name, func_count, total in sorted(problems):
    print(f"{cwe_name:<20} {func_count}/{total} functional, 0/{total} secure")