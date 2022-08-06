// eslint-disable-next-line @typescript-eslint/no-empty-function
const noop = () => {};

export function ajax(node, { onsubmit = noop, onresponse = noop } = {}) {
	const handler = async (event) => {
		event.preventDefault();
		const body = node.method === 'post' || node.method === 'put' ? new FormData(node) : null;

		onsubmit(body);

		const response = await fetch(node.action, {
			method: node.method,
			body,
			headers: {
				accept: 'application/json'
			}
		});

		onresponse(response);
	};

	node.addEventListener('submit', handler);

	return {
		destroy() {
			node.removeEventListener('submit', handler);
		}
	};
}

export function clickOutside(node, onEventFunction) {
	const handleClick = (event) => {
		var path = event.composedPath();

		if (!path.includes(node)) {
			onEventFunction();
		}
	};

	document.addEventListener('click', handleClick);

	return {
		destroy() {
			document.removeEventListener('click', handleClick);
		}
	};
}
