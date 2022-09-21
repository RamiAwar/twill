import { get } from "@/api";
import routes from "@/routes";
import useResponse from "@/composables/useResponse";

export default defineEventHandler(async (event) => {
  const session_id = getCookie(event, "session_id") || null;
  const url = new URL(event.req.url, "http://whatever");

  // Fetch login twitter redirect URL
  const { body, cookies, error } = await get(routes.twitter_auth + url.search, session_id);

  // Return response with cookie headers
  return useResponse(event, body, cookies, error);
});
