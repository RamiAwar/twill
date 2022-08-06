import * as api from '$lib/api.js';
import { respond } from '../_respond';

export async function GET(request) {
	const body = await api.post('/logout', request.locals.session);
	return respond(body);
}
