import axios from "axios";
import cookieParser from "set-cookie-parser";

const { API_URL } = useRuntimeConfig();

interface APIResponse {
  body: any;
  cookies: Map<string, any>;
}

const getType = (obj) => Object.prototype.toString.call(obj).slice(8, -1);
const isObject = (obj) => getType(obj) === "Object";

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
  }).then((r) => {
    const cookies = cookieParser.parse(r.headers["set-cookie"], {
      decodeValues: true,
      map: true,
    });

    try {
      const json = JSON.parse(r.data);
      if (json?.status === "error") {
        console.log(`API response error from ${API_URL}${path}: ${r.data}`);
      }
      return { body: json, cookies: cookies };
    } catch (err) {
      return { body: r.data, cookies };
    }
  });
}

export function get(path, session_id) {
  return send("GET", path, null, session_id);
}

export function post(path, body, session_id) {
  return send("POST", path, body, session_id);
}

//   async getMe(token: string) {
//     return axios.get<IUserProfile>(
//       `${apiUrl}/api/v1/users/me`,
//       authHeaders(token)
//     );
//   },
//   async updateMe(token: string, data: IUserProfileUpdate) {
//     return axios.put<IUserProfile>(
//       `${apiUrl}/api/v1/users/me`,
//       data,
//       authHeaders(token)
//     );
//   },
//   async getUsers(token: string) {
//     return axios.get<IUserProfile[]>(
//       `${apiUrl}/api/v1/users/`,
//       authHeaders(token)
//     );
//   },
//   async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
//     return axios.put(
//       `${apiUrl}/api/v1/users/${userId}`,
//       data,
//       authHeaders(token)
//     );
//   },
//   async createUser(token: string, data: IUserProfileCreate) {
//     return axios.post(`${apiUrl}/api/v1/users/`, data, authHeaders(token));
//   },
//   async passwordRecovery(email: string) {
//     return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
//   },
//   async resetPassword(password: string, token: string) {
//     return axios.post(`${apiUrl}/api/v1/reset-password/`, {
//       new_password: password,
//       token,
//     });
//   },
// };
