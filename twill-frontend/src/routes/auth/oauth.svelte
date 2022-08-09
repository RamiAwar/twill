<script context="module">
	export function load({ session }) {
		if (session.user_id) {
			return {
				status: 302,
				redirect: `/`
			};
		}

		return {};
	}
</script>

<script>
	import { userStore } from '$lib/store.js';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { session } from '$app/stores';

	export let user;

	console.log('received user: ', user);
	userStore.set(user.user);

	onMount(async () => {
		if (user) {
			// Set user_id here to refresh session store
			$session.user_id = user.user.id;

			// Check if needs onboarding
			if (user.new_user) {
				goto('/onboarding');
			} else {
				goto('/dashboard');
			}
		} else {
			// TODO: Show error
		}
	});
</script>
