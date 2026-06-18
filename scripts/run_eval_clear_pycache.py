import sys
import os
import shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cweval.evaluate import Evaler

def clear_test_imports():
    test_modules = [key for key in sys.modules.keys() if '_test' in key]
    for module in test_modules:
        del sys.modules[module]

if __name__ == '__main__':
    eval = Evaler(eval_path="evals/test_gpt_dan", num_proc=1)

    print("parse files")
    eval.parse_generated()
    
    print("compile if needed")
    eval.compile_parsed()


    print("copy test files from benchmark folder")
    eval._copy_test_files()
    
    print("run tests")
    from cweval.run_tests import run_tests
    import json
    
    all_gen_results = []
    for i, generated_path in enumerate(eval.generated_paths):
        clear_test_imports()
        
        for root, dirs, files in os.walk(generated_path):
            if '__pycache__' in dirs:
                shutil.rmtree(os.path.join(root, '__pycache__'), ignore_errors=True)
        for root, dirs, files in os.walk('cweval'):
            if '__pycache__' in dirs:
                shutil.rmtree(os.path.join(root, '__pycache__'), ignore_errors=True)
        
        try:
            file_res_list = run_tests(generated_path)
            all_gen_results.append(file_res_list)
            
            all_res = {
                file_res.file: {
                    'functional': file_res.functional,
                    'secure': file_res.secure,
                }
                for file_res in file_res_list
            }
            res_json_path = os.path.join(generated_path, 'res.json')
            with open(res_json_path, 'w') as f:
                json.dump(all_res, f, indent=4)
            
        except Exception as e:
            print(f"error: {e}")
            all_gen_results.append([])
        
        clear_test_imports()
        for root, dirs, files in os.walk(generated_path):
            if '__pycache__' in dirs:
                shutil.rmtree(os.path.join(root, '__pycache__'), ignore_errors=True)
        for root, dirs, files in os.walk('cweval'):
            if '__pycache__' in dirs:
                shutil.rmtree(os.path.join(root, '__pycache__'), ignore_errors=True)
    
    print("\n" + "="*60)
    print("Step 4: Merging results...")
    eval._merge_results()
    
    print("\nStep 5: Reporting metrics...")
    eval.report_pass_at_k(mode='auto')