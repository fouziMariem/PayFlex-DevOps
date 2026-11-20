import http from "k6/http";
import { check, sleep } from "k6";

const BASE_URL = "http://localhost:8000";
const SCENARIO = __ENV.TEST_SCENARIO || "normal";

const endpoints = {
  normal: "/health",
  performance_warning: "/medium",
  performance_critical: "/slow",
  error_rate_critical: "/error",
};

const target = endpoints[SCENARIO] || endpoints.normal;

let thresholds;

if (SCENARIO === "performance_warning") {
  thresholds = {
    http_req_duration: ["p(95)<200"],
  };
} else if (SCENARIO === "error_rate_critical") {
  thresholds = {
    http_req_failed: ["rate<0.01"],
  };
} else {
  thresholds = {
    http_req_duration: ["p(95)<500"],
    http_req_failed: ["rate<0.01"],
  };
}

export const options = {
  stages: [
    { duration: "30s", target: 10 },
    { duration: "1m", target: 20 },
    { duration: "30s", target: 0 },
  ],
  thresholds,
};

export default function () {
  const response = http.get(`${BASE_URL}${target}`);

  check(response, {
    "expected HTTP status": (r) =>
      SCENARIO === "error_rate_critical" ? r.status === 500 : r.status === 200,
  });

  sleep(1);
}
