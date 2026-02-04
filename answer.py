from flask import Flask, request, jsonify
import time, os
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# Flask app
app = Flask(__name__)

# Graph directory
GRAPH_DIR = "static/graphs"
os.makedirs(GRAPH_DIR, exist_ok=True)

# Database setup
engine = create_engine("mysql+pymysql://<HOST_NAME>:<PASSWORD>@<USER_NAME>:<PORT>/<DATABASE_NAME") # Complete this using your credintials of your database
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# SQLAlchemy model
class AnalysisResult(Base):
    __tablename__ = 'analysis_results'
    id = Column(Integer, primary_key=True)
    algo = Column(String(50))
    items = Column(Integer)
    steps = Column(Integer)
    start_time = Column(Float)
    end_time = Column(Float)
    total_time_ms = Column(Float)
    time_complexity = Column(String(20))
    path_to_graph = Column(String(255))

Base.metadata.create_all(engine)

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

algorithms = {
    "bubble": bubble_sort,
    "linear": linear_search,
    "binary": binary_search,
    "nested": nested_loops
}

# Route for Analyze
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

# To save Analysis to database
@app.route('/save_analysis', methods=['POST'])
def save_analysis():
    data = request.get_json()
    required = ['algo', 'items', 'steps', 'start_time', 'end_time', 'total_time_ms', 'time_complexity', 'path_to_graph']
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400

    result = AnalysisResult(
        algo=data['algo'],
        items=data['items'],
        steps=data['steps'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        total_time_ms=data['total_time_ms'],
        time_complexity=data['time_complexity'],
        path_to_graph=data['path_to_graph']
    )
    session.add(result)
    session.commit()

    return jsonify({"message": "Analysis saved", "id": result.id}), 201

# Retrieve Analysis from database
@app.route('/retrieve_analysis')
def retrieve_analysis():
    analysis_id = request.args.get('id')
    if not analysis_id:
        return jsonify({"error": "Missing analysis ID"}), 400

    result = session.get(AnalysisResult, int(analysis_id))
    if not result:
        return jsonify({"error": "Analysis not found. Check your ID & Try again"}), 404

    return jsonify({
        "algo": result.algo,
        "items": result.items,
        "steps": result.steps,
        "start_time": result.start_time,
        "end_time": result.end_time,
        "total_time_ms": result.total_time_ms,
        "time_complexity": result.time_complexity,
        "path_to_graph": result.path_to_graph
    })

if __name__ == '__main__':
    app.run(port=3000)
