import argparse
import requests
import concurrent.futures


def make_request(url):
    try:
        # Make a GET request to the specified URL
        response = requests.get(url)

        # Return True if the request is successful (status code 2xx), False otherwise
        return response.ok
    except requests.RequestException:
        # Return False for network errors
        return False


def make_requests(url, num_requests, num_concurrent):
    # Create a list of URLs to make requests to
    urls = [url] * num_requests

    successes = 0
    failures = 0

    # Create a ThreadPoolExecutor with the specified number of concurrent workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
        # Submit tasks for each URL
        futures = [executor.submit(make_request, url) for url in urls]

        # Wait for all tasks to complete
        for future in concurrent.futures.as_completed(futures):
            # Increment successes or failures based on the result of each task
            if future.result():
                successes += 1
            else:
                failures += 1

    # Print summary
    print(f"Successes: {successes}")
    print(f"Failures: {failures}")


if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Make concurrent HTTP requests")

    # Add command-line options
    parser.add_argument("-u", "--url", type=str, help="URL to test", required=True)
    parser.add_argument("-n", "--num-requests", type=int, default=10, help="Number of requests to make")
    parser.add_argument("-c", "--num-concurrent", type=int, default=1, help="Number of concurrent requests")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Make the requests
    make_requests(args.url, args.num_requests, args.num_concurrent)
