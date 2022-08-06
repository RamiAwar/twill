<script>
	import { userStore } from '$lib/store.js';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { session } from '$app/stores';

	userStore.set({});

	onMount(async () => {
		// Set user_id here to clear session store
		$session.user_id = null;
		goto('/');
	});
</script>
