import * as api from '$lib/api.js';
import { respond } from '../_respond';
import { routes } from '$lib/routes.js';

export async function GET(request) {
	const params = request.url.search;
	const user = await api.get(`${routes.twitter_auth}${params}`, request.locals.session);
	return respond(user, 'user');
}
