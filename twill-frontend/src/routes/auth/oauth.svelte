<script>
	import { userStore } from '$lib/store.js';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { session } from '$app/stores';

	export let user;

	onMount(async () => {
		if (user) {
			// Set user_id here to refresh session store
			$session.user_id = user.id;
			userStore.set(user);
			goto('/dashboard');
		} else {
			// TODO: Show error
		}
	});
</script>
