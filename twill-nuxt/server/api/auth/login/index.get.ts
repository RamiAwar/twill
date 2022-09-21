import { get } from "@/api";
import routes from "@/routes";
import useResponse from "@/composables/useResponse";

export default defineEventHandler(async (event) => {
  // Fetch client side session_id cookie
  let session_id = getCookie(event, "session_id") || null;

  // Fetch login twitter redirect URL
  const { body, cookies, error } = await get(routes.twitter_login, session_id);

  // Return response with cookie headers
  return useResponse(event, body, cookies, error);
});
