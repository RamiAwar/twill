export default function (event, body, cookies) {
  if (cookies && cookies["session"]) {
    const session_id = cookies["session"].value;
    setCookie(event, "session_id", session_id);
  }
  return body;
}