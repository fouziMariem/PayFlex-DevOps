import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  stages: [
    { duration: "30s", target: 10 },
    { duration: "1m", target: 20 },
    { duration: "30s", target: 0 },
  ],

  thresholds: {
    http_req_duration: ["p(95)<500"],
    http_req_failed: ["rate<0.01"],
  },
};

const BASE_URL = "http://localhost:8000";

export default function () {
  const response = http.get(`${BASE_URL}/health`);

  check(response, {
    "status is 200": (r) => r.status === 200,
    "API is healthy": (r) => r.json("status") === "healthy",
  });

  sleep(1);
}
