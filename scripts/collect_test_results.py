import sys
import os
import shutil
import subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cweval.evaluate import Evaler

def clear_test_imports():
    test_modules = [key for key in sys.modules.keys() if '_test' in key]
    for module in test_modules:
        del sys.modules[module]

def run_individual_test(test_file_path: str) -> dict:
    result = subprocess.run(
        ['python', '-m', 'pytest', test_file_path, '-v', '--tb=short'],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )
    
    stdout = result.stdout
    functional = 'functionality' in stdout and 'PASSED' in stdout
    secure = 'security' in stdout and 'PASSED' in stdout
    
    has_func_fail = 'functionality' in stdout and 'FAILED' in stdout
    has_sec_fail = 'security' in stdout and 'FAILED' in stdout
    
    if 'functionality' in stdout:
        functional = not has_func_fail
    
    if 'security' in stdout:
        secure = not has_sec_fail
    
    return {
        'functional': functional,
        'secure': secure,
        'return_code': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr,
        'all_passed': result.returncode == 0
    }

if __name__ == '__main__':
    eval_path = "evals/test_n10_for_feedback_driven_haiku3"
    eval = Evaler(eval_path=eval_path, num_proc=1)
    
    print("Parsing files")
    eval.parse_generated()
    
    print("Compiling (if necessary)")
    eval.compile_parsed()

    print("Copy test files from benchmark folder")
    eval._copy_test_files()
    
    print("Running tests")
    import json
    import glob
    
    all_gen_results = []
    
    for i, generated_path in enumerate(eval.generated_paths):
        test_files = glob.glob(f"{generated_path}/core/py/*_test.py")
        
        if not test_files:
            print("No test files found")
            continue
        
        gen_results = {}
        all_test_feedback = []
        
        for test_file in sorted(test_files):
            test_name = os.path.basename(test_file)
            
            clear_test_imports()
            for root, dirs, files in os.walk(generated_path):
                if '__pycache__' in dirs:
                    shutil.rmtree(os.path.join(root, '__pycache__'), ignore_errors=True)
            
            test_result = run_individual_test(test_file)
            
            feedback_dir = "test_feedback_haiku3"
            os.makedirs(feedback_dir, exist_ok=True)
            feedback_file = test_file.replace('_test.py', '_feedback.txt')
            feedback_file = os.path.join(feedback_dir, os.path.basename(test_file.replace('_test.py', '_feedback.txt')))

            with open(feedback_file, 'w') as f:
                f.write(f"Functional: {'PASS' if test_result['functional'] else 'FAIL'}\n")
                f.write(f"Security:   {'PASS' if test_result['secure'] else 'FAIL'}\n")
                f.write(f"All Tests:  {'PASS' if test_result['all_passed'] else 'FAIL'}\n")
                f.write(f"\n{'='*60}\n")
                f.write("DETAILED OUTPUT:\n")
                f.write(f"{'='*60}\n\n")
                f.write(test_result['stdout'])
                if test_result['stderr']:
                    f.write(f"\n\n{'='*60}\n")
                    f.write("ERRORS:\n")
                    f.write(f"{'='*60}\n\n")
                    f.write(test_result['stderr'])
            
            gen_results[test_file] = {
                'functional': test_result['functional'],
                'secure': test_result['secure'],
            }
            
            all_test_feedback.append({
                'test': test_name,
                'functional': test_result['functional'],
                'secure': test_result['secure'],
                'all_passed': test_result['all_passed']
            })
        
        res_json_path = os.path.join(generated_path, 'res.json')
        with open(res_json_path, 'w') as f:
            json.dump(gen_results, f, indent=4)
        
        summary_path = os.path.join(generated_path, 'test_summary.json')
        with open(summary_path, 'w') as f:
            json.dump({
                'total_tests': len(test_files),
                'functional_pass': sum(1 for r in gen_results.values() if r['functional']),
                'security_pass': sum(1 for r in gen_results.values() if r['secure']),
                'both_pass': sum(1 for r in gen_results.values() if r['functional'] and r['secure']),
                'tests': all_test_feedback
            }, f, indent=4)