import axios from "axios";
import cookieParser from "set-cookie-parser";

const { API_URL } = useRuntimeConfig();
import { APIError } from "@/models/api";

interface APIResponse {
  body: any;
  cookies: Map<string, any>;
  error: APIError;
}

async function send(method: string, path: string, data: any, session_id: string): Promise<APIResponse> {
  let headers = {};
  if (data) {
    headers["Content-Type"] = "application/json";
    data = JSON.stringify(data);
  }

  if (session_id) {
    headers["Cookie"] = `session=${session_id}`;
  }

  return await axios({
    method,
    url: `${API_URL}${path}`,
    data,
    headers,
  })
    .then((r) => {
      const cookies = cookieParser.parse(r.headers["set-cookie"], {
        decodeValues: true,
        map: true,
      });

      try {
        const json = JSON.parse(r.data);
        if (json?.status === "error") {
          console.log(`API response error from ${API_URL}${path}: ${r.data}`);
          return {
            body: {},
            cookies: new Map(),
            error: { message: "Something went wrong! Please try again later.", code: 500 },
          };
        }
        return { body: json, cookies: cookies, error: null };
      } catch (err) {
        return { body: r.data, cookies, error: null };
      }
    })
    .catch((error) => {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        const message = error.response.data.detail;
        const code = error.response.status;
        console.log(`API response error from ${API_URL}${path}: ${JSON.stringify(error.response.data.detail)}`);
        return { body: {}, cookies: new Map(), error: { message, code } };
      } else if (error.request) {
        // The request was made but no response was received
        // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
        // http.ClientRequest in node.js
        console.log("No response received for request ", error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log("Error setting up request", error.message);
      }
      return {
        body: {},
        cookies: new Map(),
        error: { message: "Something went wrong! Please try again later.", code: 500 },
      };
    });
}

export function get(path, session_id) {
  return send("GET", path, null, session_id);
}

export function post(path, body, session_id) {
  return send("POST", path, body, session_id);
}
