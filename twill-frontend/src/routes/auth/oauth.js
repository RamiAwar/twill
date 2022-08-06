import * as api from '$lib/api.js';
import { respond } from '../_respond';

export async function GET(request) {
	const params = request.url.search;
	const user = await api.get(`/oauth${params}`, request.locals.session);
	return respond(user, 'user');
}
