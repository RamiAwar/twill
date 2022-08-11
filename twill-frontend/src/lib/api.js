import * as cookie from 'cookie';
import { env } from '$lib/config';

const getType = (obj) => Object.prototype.toString.call(obj).slice(8, -1);
const isObject = (obj) => getType(obj) === 'Object';

const base = env.basePath;

async function send({ method, path, data, session }) {
	const opts = { method, headers: {} };

	if (data) {
		opts.headers['Content-Type'] = 'application/json';
		opts.body = JSON.stringify(data);
	}

	if (session) {
		// console.log('session in pre-send server side: ', session);
		opts.headers['Cookie'] = `session=${session}`;
	}

	return fetch(`${base}${path}`, opts)
		.then(async (r) => {
			const data = await r.text();
			const cookies = r.headers.get('set-cookie');
			return { body: data, cookies: cookies };
		})
		.then(({ body, cookies }) => {
			try {
				var resParsed = JSON.parse(body);

				if (resParsed?.status === 'error') {
					console.log(`API response error from ${base}/${path}: ${body}`);
				}

				if (isObject(resParsed)) {
					return { ...resParsed, cookies: cookies };
				} else {
					return { body: resParsed, cookies: cookies };
				}
			} catch (err) {
				if (isObject(body)) {
					return { ...body, cookies: cookies };
				} else {
					return { body: body, cookies: cookies };
				}
			}
		});
}

export function get(path, session) {
	return send({ method: 'GET', path, session });
}

export function del(path, session) {
	return send({ method: 'DELETE', path, session });
}

export function post(path, data, session) {
	return send({ method: 'POST', path, data, session });
}

export function put(path, data, session) {
	return send({ method: 'PUT', path, data, session });
}
