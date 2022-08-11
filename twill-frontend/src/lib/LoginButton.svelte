<script>
	import { goto } from '$app/navigation';
	import { session } from '$app/stores';

	async function login() {
		// Get twitter redirect URL
		const res = await fetch('/auth/login', { method: 'GET', session: $session });

		// Redirect to twitter login
		if (res.ok) {
			const data = await res.json();
			if (data.redirect_url) {
				goto(data.redirect_url);
			} else {
				// TODO: Show error
				console.log('error getting twitter redirect');
			}
		}
	}
</script>

<button
	on:click={login}
	class="ml-8 inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-blue-400 hover:bg-blue-500 transition-colors duration-250"
>
	Login with Twitter
</button>
