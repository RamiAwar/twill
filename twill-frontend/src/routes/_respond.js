export function respond(body, prefix) {
	if (body.errors) {
		return { status: 401, body };
	}

	let headers = {};
	const cookies = body.cookies;

	if (cookies) {
		headers = {
			'set-cookie': cookies
		};
	}

	if (prefix) {
		return {
			headers: headers,
			body: { [prefix]: body }
		};
	}

	return {
		headers: headers,
		body
	};
}
