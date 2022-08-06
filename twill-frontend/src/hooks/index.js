import * as cookie from 'cookie';

export async function handle({ event, resolve }) {
	const cookies = cookie.parse(event.request.headers.get('cookie') || '');

	event.locals.session = cookies.session ? cookies.session : null;
	event.locals.user_id = cookies.user_id ? cookies.user_id : null;

	return await resolve(event);
}

export function getSession(event) {
	const session = event?.locals?.session;
	if (session) {
		return {
			user_id: event?.locals?.user_id,
			cookie: event.locals.session
		};
	}

	return {};
}
