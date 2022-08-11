import { TWILL_API_URL } from '$env/static/private';

export const env = {
	basePath: TWILL_API_URL
};

function checkEnv(val, name = 'unspecified var') {
	if (val === undefined || val === null) {
		throw 'missing env var for ' + name;
	}
	return val;
}

checkEnv(TWILL_API_URL, 'TWILL_API_URL');
