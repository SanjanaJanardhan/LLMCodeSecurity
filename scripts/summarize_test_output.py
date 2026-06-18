import os
import anthropic

def summarize_pytest_output(file_content):
    client = anthropic.Anthropic(api_key="")
    
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": f"""Summarize this pytest output. Focus on:
                    - Overall test result (pass/fail)
                    - Key functional and security test outcomes
                    - Any significant errors or issues
                    
                    Pytest Output:
                    {file_content}
                    """
                }
            ]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error in summarization: {str(e)}"

def process_pytest_feedback_dir(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('_feedback.txt'):
            file_path = os.path.join(directory_path, filename)
            
            with open(file_path, 'r') as f:
                file_content = f.read()
            
            summary = summarize_pytest_output(file_content)
            
            with open(file_path, 'w') as f:
                f.write("summary:\n")
                f.write(summary)

def main():
    feedback_dir = "evals/test_n10_for_feedback_driven_haiku3/generated_0/core/py"
    process_pytest_feedback_dir(feedback_dir)

if __name__ == "__main__":
    main()