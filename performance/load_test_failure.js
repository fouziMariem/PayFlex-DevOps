import http from "k6/http";
import { check } from "k6";

export const options = {
  vus: 20,
  duration: "30s",

  thresholds: {
    http_req_duration: ["p(95)<1"],
  },
};

export default function () {
  const response = http.get("http://localhost:8000/health");

  check(response, {
    "status is 200": (r) => r.status === 200,
  });
}
