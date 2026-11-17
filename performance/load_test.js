import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 20, // virtual users
  duration: "30s", // test duration

  thresholds: {
    http_req_duration: ["p(95)<200"], // 95% reqs have to answer before 200ms
    http_req_failed: ["rate<0.01"], // error rate less than 1%
  },
};

export default function () {
  const response = http.get("http://localhost:8000/health");

  check(response, {
    "status is 200": (r) => r.status === 200,
    "API is healthy": (r) => r.json("status") === "healthy",
  });

  sleep(1);
}
