from flask import Flask, request, jsonify
import time, os
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

# Folder to save graph images
GRAPH_DIR = "static/graphs"
os.makedirs(GRAPH_DIR, exist_ok=True)

# Algorithms
def bubble_sort(n):
    arr = np.random.randint(0, 100, n)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def linear_search(n):
    for i in range(n):
        if i == n - 1:
            return i

def binary_search(n):
    arr = sorted(np.random.randint(0, 100, n))
    target = arr[-1]
    left, right = 0, n - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

def nested_loops(n):
    for i in range(n):
        for j in range(n):
            pass

# Mapping query values to functions
algorithms = {
    "bubble": bubble_sort,
    "linear": linear_search,
    "binary": binary_search,
    "nested": nested_loops
}

@app.route('/analyze')
def analyze():
    algo_key = request.args.get('algo')
    n = int(request.args.get('n', 1000))
    step = int(request.args.get('steps', 10))

    if algo_key not in algorithms:
        return jsonify({"error": "Invalid algorithm"}), 400

    algo_func = algorithms[algo_key]
    input_sizes = list(range(step, n + 1, step))
    times = []

    start_time = time.time()
    for size in input_sizes:
        t0 = time.time()
        algo_func(size)
        t1 = time.time()
        times.append(t1 - t0)
    end_time = time.time()

    # Plotting
    fig, ax = plt.subplots()
    ax.plot(input_sizes, times, marker='o')
    ax.set_title(f"{algo_key} time complexity")
    ax.set_xlabel("Input size")
    ax.set_ylabel("Time (s)")

    # Save plot to file
    filename = f"{algo_key}_{int(time.time())}.png"
    filepath = os.path.join(GRAPH_DIR, filename)
    plt.savefig(filepath)
    plt.close()

    return jsonify({
        "algo": algo_key,
        "items": n,
        "steps": step,
        "start_time": start_time,
        "end_time": end_time,
        "total_time_ms": round((end_time - start_time) * 1000, 2),
        "graph_file": f"/{filepath}"
    })

if __name__ == '__main__':
    app.run(port=3000)

