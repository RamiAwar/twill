<script>
	import { userStore } from '$lib/store.js';
	import { page } from '$app/stores';
	import { clickOutside } from '$lib/actions.js';

	export let showDropdown = false;

	const toggleProfileDropdown = () => {
		showDropdown = !showDropdown;
	};

	$: pageName = $page.url.pathname.substring($page.url.pathname.lastIndexOf('/') + 1);
	$: console.log(pageName);
</script>

<div class="ml-3 relative" use:clickOutside={() => (showDropdown = false)}>
	<div>
		<button
			type="button"
			class="bg-white rounded-full flex text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
			id="user-menu-button"
			aria-expanded="false"
			aria-haspopup="true"
			on:click={toggleProfileDropdown}
		>
			<span class="sr-only">Open user menu</span>
			<img class="h-10 w-10 rounded-full" src={$userStore.profile_image_url} alt="" />
		</button>
	</div>

	<!-- Dropdown menu, show/hide based on menu state.

    Entering: "transition ease-out duration-200"
        From: "transform opacity-0 scale-95"
        To: "transform opacity-100 scale-100"
    Leaving: "transition ease-in duration-75"
        From: "transform opacity-100 scale-100"
        To: "transform opacity-0 scale-95"
    -->
	<div
		class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
		role="menu"
		aria-orientation="vertical"
		aria-labelledby="user-menu-button"
		tabindex="-1"
		class:hidden={!showDropdown}
	>
		<!-- Active: "bg-gray-100", Not Active: "" -->
		<a
			href="/profile"
			class="block px-4 py-2 text-sm text-gray-700"
			class:active={pageName === 'profile'}
			role="menuitem"
			tabindex="-1"
			id="user-menu-item-0">Your Profile</a
		>
		<a
			href="/settings"
			class="block px-4 py-2 text-sm text-gray-700"
			class:active={pageName === 'settings'}
			role="menuitem"
			tabindex="-1"
			id="user-menu-item-1">Settings</a
		>
		<a
			href="/auth/logout"
			class="block px-4 py-2 text-sm text-gray-700"
			class:active={pageName === 'logout'}
			role="menuitem"
			tabindex="-1"
			id="user-menu-item-2">Sign out</a
		>
	</div>
</div>

<style>
	.active {
		@apply bg-gray-100;
	}
</style>
