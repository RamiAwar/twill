import * as api from '$lib/api.js';
import { respond } from '../_respond';
import { routes } from '$lib/routes.js';

export async function GET(request) {
	const body = await api.post(routes.logout, request.locals.session);
	return respond(body);
}
