import http from 'k6/http';
import { sleep } from 'k6';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 }, // Ramp up to 10 VUs in 30 seconds
    { duration: '1m', target: 10 }, // Stay at 10 VUs for 1 minute
    { duration: '30s', target: 0 }, // Ramp down to 0 VUs in 30 seconds
  ],
};

export default function () {
  // Generate a random sleep_for value between 0.1 and 4
  const sleepFor = (Math.random() * (4 - 0.1) + 0.1).toFixed(1);

  // Construct the URL with the query parameter
  const url = `http://localhost:8000/sleep?sleep_for=${sleepFor}`;

  // Send the GET request
  const res = http.get(url);

  // Validate response status and log the result
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time is acceptable': (r) => r.timings.duration < 5000, // Example threshold
  });

  // Optional: Sleep to simulate user think time
  //sleep(1);
}
