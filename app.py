import os
import sys
import getopt
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def main():
    code_path, code_start, code_end, test_path, test_start, test_end = sys.argv[1:]

    with open(code_path, "r") as cp:
        code = "".join(cp.readlines()[int(code_start) - 1 : int(code_end)])

    with open(test_path, "r") as tp:
        unit_test = "".join(tp.readlines()[int(test_start) - 1 : int(test_end)])

    print(generate_prompt(code, unit_test))

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": generate_prompt(code, unit_test)}],
    )

    print(response["choices"][0]["message"]["content"])


def generate_prompt(code, unit_test):
    return f"""
Given the following code: 

{code} 

and this test which tests the happy path of the function: 

{unit_test}

generate the tests wich cover the other branches of the function.
    """


if __name__ == "__main__":
    main()
