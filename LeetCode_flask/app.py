from flask import Flask, render_template, request, jsonify
import textwrap

app = Flask(__name__)

# Sample LeetCode problem data
leetcode_problems = {
    "two_sum": {
        "title": "Two Sum",
        "description": "Given an array of integers, return indices of the two numbers such that they add up to a specific target.",
        "difficulty": "Easy",
        "example": "Input: nums = [2, 7, 11, 15], target = 9\nOutput: [0, 1]",
        "test_cases": [
            {"input": {"nums": [2, 7, 11, 15], "target": 9}, "output": [0, 1]},
            {"input": {"nums": [3, 2, 4], "target": 6}, "output": [1, 2]},
        ],
        "solution": "def two_sum(nums, target):\n    for i in range(len(nums)):\n        for j in range(i + 1, len(nums)):\n            if nums[i] + nums[j] == target:\n                return [i, j]\n"
    }
}

@app.route('/')
def index():
    return render_template('index.html', problems=leetcode_problems)

@app.route('/problem/<problem_id>')
def show_problem(problem_id):
    problem = leetcode_problems.get(problem_id)
    if problem:
        return render_template('problem.html', problem=problem, problem_id=problem_id)
    else:
        return "Problem not found", 404

@app.route('/submit_solution/<problem_id>', methods=['POST'])
def submit_solution(problem_id):
    problem = leetcode_problems.get(problem_id)
    if not problem:
        return "Problem not found", 404

    user_solution = request.form['solution']
    solution_function_code = textwrap.dedent(user_solution)

    def execute_solution(test_input):
        local_vars = {}
        exec(solution_function_code, {}, local_vars)
        solution_fn = local_vars.get(problem_id)
        return solution_fn(**test_input)

    correct = True
    for case in problem['test_cases']:
        expected = case['output']
        actual = execute_solution(case['input'])
        if expected != actual:
            correct = False
            return f"Test case failed! Expected {expected}, but got {actual}"

    if correct:
        return "All test cases passed!"
    else:
        return "Some test cases failed."

@app.route('/solution/<problem_id>')
def show_solution(problem_id):
    problem = leetcode_problems.get(problem_id)
    if problem and 'solution' in problem:
        return jsonify(solution=problem['solution'])
    else:
        return jsonify(solution="Solution not available"), 404

if __name__ == '__main__':
    app.run(debug=True)
