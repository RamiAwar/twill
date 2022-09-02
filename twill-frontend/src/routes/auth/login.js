import * as api from '$lib/api.js';
import { routes } from '$lib/routes.js';
import { respond } from '../_respond';

export async function GET(request) {
	const body = await api.get(routes.twitter_login, request.locals.session);
	return respond(body);
}
