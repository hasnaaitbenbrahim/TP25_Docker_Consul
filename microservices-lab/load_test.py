import time
import requests
import concurrent.futures
import statistics
import sys
import argparse

def run_request(url):
    start = time.time()
    try:
        resp = requests.get(url)
        latency = (time.time() - start) * 1000 # ms
        return latency, resp.status_code
    except Exception as e:
        return 0, 500

def load_test(url, users, duration):
    print(f"Starting load test for {url} with {users} users for {duration} seconds...")
    start_time = time.time()
    end_time = start_time + duration
    
    latencies = []
    errors = 0
    requests_count = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=users) as executor:
        futures = []
        while time.time() < end_time:
            # Fill the pool
            while len(futures) < users and time.time() < end_time:
                futures.append(executor.submit(run_request, url))
            
            # Process completed
            done, not_done = concurrent.futures.wait(futures, timeout=0.1, return_when=concurrent.futures.FIRST_COMPLETED)
            futures = list(not_done)
            
            for f in done:
                lat, status = f.result()
                requests_count += 1
                if status != 200:
                    errors += 1
                else:
                    latencies.append(lat)
    
    total_time = time.time() - start_time
    throughput = requests_count / total_time
    
    if latencies:
        avg_latency = statistics.mean(latencies)
        p95_latency = statistics.quantiles(latencies, n=20)[18] # 95th percentile
    else:
        avg_latency = 0
        p95_latency = 0
        
    print(f"Results for {url}:")
    print(f"  Users: {users}")
    print(f"  Requests: {requests_count}")
    print(f"  Errors: {errors}")
    print(f"  Throughput: {throughput:.2f} req/s")
    print(f"  Avg Latency: {avg_latency:.2f} ms")
    print(f"  P95 Latency: {p95_latency:.2f} ms")
    print("-" * 30)
    
    return throughput, avg_latency

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--users", type=int, default=10)
    parser.add_argument("--duration", type=int, default=10)
    parser.add_argument("--type", type=str, default="all")
    args = parser.parse_args()
    
    endpoints = {
        "rest": "http://localhost:8082/api/clients/1/car/rest",
        "feign": "http://localhost:8082/api/clients/1/car/feign",
        "webclient": "http://localhost:8082/api/clients/1/car/webclient"
    }
    
    if args.type == "all":
        for name, url in endpoints.items():
            load_test(url, args.users, args.duration)
    else:
        load_test(endpoints[args.type], args.users, args.duration)
