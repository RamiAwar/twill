import { post } from "@/api";
import routes from "@/routes";
import useResponse from "@/composables/useResponse";

export default defineEventHandler(async (event) => {
  const session_id = getCookie(event, "session_id") || null;
  const b = await useBody(event);

  // Fetch login twitter redirect URL
  const { body, cookies, error } = await post(routes.beta_signup, b, session_id);

  // Return response with cookie headers
  return useResponse(event, body, cookies, error);
});
