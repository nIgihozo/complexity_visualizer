# API Documentation: Algorithm Time Complexity Visualizer
This API allows users to analyze the time complexity of different algorithms by measuring their execution time over increasing input sizes. It returns performance metrics and a graph image showing how the algorithm scales.

## Endpoint
Code
GET /analyze

## Query Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| **algo** | string | Yes | The algorithm to analyze. Options: bubble, linear, binary, nested |
| **n** | int | No | Maximum input size to test. Default is 1000 |
| **steps** | int | No | Step size between input sizes. Default is 10 |

### Example Request
Code
http://localhost:3000/analyze?algo=bubble&n=1000&steps=100

### Example Response (JSON)
json
{
  "algo": "bubble",
  "items": 1000,
  "steps": 100,
  "start_time": 1706380000.123,
  "end_time": 1706380003.456,
  "total_time_ms": 3333.33,
  "graph_file": "/static/graphs/bubble_1706380000.png"
}

### Graph Output
- The graph is saved as a .png file in the static/graphs/ directory.

- You can view it in your browser using the graph_file path:

Code
http://localhost:3000/static/graphs/bubble_1706380000.png

## Error Responses
| Status Code | Message | Cause |
| :--- | :--- | :--- |
| 400 | `{"error": "Invalid algorithm"}` | The `algo` parameter is missing or does not match available options. |

## Supported Algorithms
| Key | Description | Time Complexity |
| :--- | :--- | :--- |
| **bubble** | Bubble Sort | $O(n^2)$ |
| **linear** | Linear Search | $O(n)$ |
| **binary** | Binary Search | $O(\log n)$ |
| **nested** | Nested Loops ($n^2$ loop) | $O(n^2)$ |

## Setup Instructions
**1. Install dependencies:**
bash
pip install flask numpy matplotlib

**2. Run the app:**
bash
python answer.py

**3. Test in your browser:**

