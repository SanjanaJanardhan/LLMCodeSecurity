# CS 6158 Fall 2025 Project: Towards Secure/Insecure Code Generation
Authors: Shriya Sudhakar (ss3576), Sanjana Janardhan (sj882)

### Repo structure
scripts/ contains all of the scripts used to run experiments.
- contains scripts that were acquired from CWEval to run tests as well as scripts we wrote for the project
benchmark/ contains the benchmark data (from CWEval) used to run experiments
- contains prompt as well as tests for generated code
misc folders such as feedback_driven, few_shot, few_shot_insecure, test_feedback_haiku3, and test_feedback_sonnet45 contain runs were leftover from experimentation, and also contain things such as pytest outputs that were provided to model for feedback driven prompt strategy.

### Where to find result data:
- Result data can be found in scripts/evals. They are named by prompt type and model.

### How to run project:
To preface, alot of files had very internal workflows that might make it difficult to run (in addition to adding API Keys, which we didn't incorporate as a command line argument to make running things locally for us easier).

Set up a conda env: conda create -n <name> python=3.8
We used python 3.8 for prompting Claude, and then a separate environment for running tests (python 3.10).

In the scripts/ directory, you will find a file called cwe_eval_generate.py. This is the main file that we ran our prompting experiments. 

The script uses Claude to generate code responses. You must then provide a claude api_key. The best way actually to provide your api key is to just paste in your api_key in line 25 where it says: self.client = anthropic.Anthropic(api_key="")

You should then be able to call cwe_eval_generate.py as such:
python cwe_eval_generate.py gen --ppt="direct" --n=10 --temperature=0.1 \
    --eval_path="evals/test_gpt_dan" --langs='["py"]'

--ppt argument is for the prompting strategy, n = 10 sets the number of samples per prompt, temperature sets the temperature to 0.1. The eval path is where you want your generated code to be outputted. Finally, the langs arg when set to python only runs the python arguments. We recommend sticking with python since we didn't test on other languages.

The default model is set to claude-sonnet-4-5-20250929. If you want to change this, you should change it via the model arg: --model=<claude_model_api_name>

If you want to test ChatGPT (note: need to be in a python3.10 env) you should run the cwe_eval_generate_openai.py script. Similarly, set the api key on line 25 and then also run similar command. Here is the structure that it should be run with:
python cwe_eval_generate_openai.py gen --ppt="fewshot" --n=10 --use_openai=True --model=gpt-5.1 --temperature=0.1 \
    --eval_path="evals/test_gpt_run" --langs='["py"]'

include the --use_openai=True argument, and also use --model=gpt-5.1

The two scripts for generating cases are actually super similar, but were just duplicated and split for collaboration and debugging purposes during the project.

### To run evaluation:
Run the run_eval_clear_pycache.py script. No command line args needed. However, you must change the evaluation directory on line 14: eval = Evaler(eval_path="evals/test_gpt_dan", num_proc=1). the eval_path would be whatever you chose as your eval_path when running cwe_eval_generate.py. This file runs all of the tests. 

To generate a summary of per CWE breakdown, first run run_eval_clear_pycache.py, then run analyze_per_cwe.py. This file also doesn't accept command line arguments, though you do need to also change the eval path on line 3.