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
			status: 200,
			headers: headers,
			body: { [prefix]: body }
		};
	}

	return {
		status: 200,
		headers: headers,
		body
	};
}
