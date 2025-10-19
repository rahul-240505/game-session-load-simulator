Game Session Load Simulator

This project is a distributed load testing framework designed to simulate thousands of concurrent game players interacting with a backend API. It was built to demonstrate proficiency in backend development, cloud infrastructure, and the core responsibilities of a Systest Engineer.

The system includes a secure, token-based Django REST API, a Python-based load generation client using Locust, and is designed to be containerized with Docker for deployment on cloud platforms like AWS.

Core Technologies

Backend: Django, Django REST Framework

Database & Caching: MySQL, Redis

Load Testing: Locust

Infrastructure & Deployment: Docker, AWS (EC2)

Monitoring & Visualization: Prometheus, Grafana (planned)

Languages: Python, SQL

Project Architecture

The system uses a standard client-server model designed for performance testing:

Django REST Backend: A secure API with endpoints for user registration (/api/users/) and token-based login (/api/login/). All other endpoints require token authentication.

Locust Load Clients: A Python script defines the "game call pattern" where a virtual user registers, logs in to get a token, and then makes repeated authenticated calls to protected endpoints.

Data Layer: MySQL is used for persistent storage of user accounts, while Redis is used for high-throughput caching tasks.

Performance Analysis & Bottleneck Identification

A key goal of this project was to perform a full cycle of performance testing: establish a baseline, stress the system to find its limits, and conduct a root cause analysis of a simulated bottleneck.

Test A: Initial Performance Baseline

The first test was to establish a baseline performance metric under a light, controlled load.

Setup: 10 concurrent users with a spawn rate of 2 users/sec.

Result: The API demonstrated excellent performance, with a 95th percentile latency of just 12ms for authenticated requests. The system was stable with 0 failures.

Statistics (10 Users):
![images/low-load_stats.png]

Charts (10 Users):
![images/low-load_charts.png]

Test B: High-Load Stress Test

The second test was designed to measure the API's performance and stability under a significant load to find its throughput limits.

Setup: 100 concurrent users with a spawn rate of 10 users/sec.

Result: The API remained highly responsive and stable, stabilizing at ~50 requests per second with 0 failures. The p99 latency for authenticated requests remained exceptionally low at under 50ms.

Statistics (100 Users):
![images/high-load_stats.png]

Charts (100 Users):
![images/high-load_charts.png]

Test C: Bottleneck Simulation & Analysis

To demonstrate root cause analysis, a 1-second delay (time.sleep(1)) was intentionally introduced into the user list API view to simulate a slow database query. The initial 10-user test was run again to precisely measure the impact.
![images/delay_simulation.png]

Setup: 10 concurrent users with a spawn rate of 2 users/sec (with bottleneck).

Result: The impact was immediate and dramatic. The p99 latency for the affected endpoint spiked to over 1000ms. The Locust charts clearly visualized this consistent bottleneck, proving the ability to identify and quantify the exact impact of a performance regression.

Statistics (10 Users with Delay):
![images/bottleneck_stats.png]

Charts (10 Users with Delay):
![images/bottleneck_charts.png]

This three-stage analysis demonstrates a complete end-to-end system testing workflow, from establishing a baseline to identifying and proving the impact of a specific performance issue.