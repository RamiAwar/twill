<script>
	import LoginButton from '$lib/LoginButton.svelte';
	import { page } from '$app/stores';
	import { slide } from 'svelte/transition';
	import ProfileMenu from '$lib/ProfileMenu.svelte';
	import { session } from '$app/stores';
	import { cubicInOut } from 'svelte/easing';

	// Toggle mobile menu
	let is_mobile_menu_open = false;
	let showProfileDropdown = false;

	const toggleMobileMenuDropdown = () => {
		is_mobile_menu_open = !is_mobile_menu_open;
	};

	$: pageName = $page.url.pathname.substring($page.url.pathname.lastIndexOf('/') + 1);
</script>

<nav class="bg-white shadow">
	<div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
		<div class="relative flex justify-between h-16">
			<div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
				<!-- Mobile menu button -->
				<button
					type="button"
					class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-pink-500"
					aria-controls="mobile-menu"
					aria-expanded="false"
					on:click={toggleMobileMenuDropdown}
				>
					<span class="sr-only">Open main menu</span>
					<!--
                        Icon when menu is closed.
                        Heroicon name: outline/menu
                        Menu open: "hidden", Menu closed: "block"
                    -->
					<svg
						class="h-6 w-6"
						class:block={!is_mobile_menu_open}
						class:hidden={is_mobile_menu_open}
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="2"
						stroke="currentColor"
						aria-hidden="true"
					>
						<path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
					</svg>

					<!--Icon when menu is open.
                        Heroicon name: outline/x
                        Menu open: "block", Menu closed: "hidden"
                    -->
					<svg
						class="h-6 w-6"
						class:hidden={!is_mobile_menu_open}
						class:block={is_mobile_menu_open}
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="2"
						stroke="currentColor"
						aria-hidden="true"
					>
						<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
					</svg>
				</button>
			</div>

			<div class="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start">
				<a class="flex-shrink-0 flex items-center" href="/">
					<img class="block lg:hidden h-12 w-auto" src="logo.png" alt="Workflow" />
					<img class="hidden lg:block h-12 w-auto" src="logo.png" alt="Workflow" />
				</a>

				<!-- Nav links -->
				{#if $session.user_id}
					<div class="hidden sm:ml-6 sm:flex sm:space-x-8">
						<!-- Current: "border-pink-500", Default: "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700" -->
						<a
							href="/dashboard"
							class="text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
							class:border-pink-500={pageName == 'dashboard'}
							class:border-transparent={pageName != 'dashboard'}
						>
							Dashboard
						</a>
					</div>
				{/if}
			</div>

			<!-- Notifications and Profile if logged in -->
			{#if $session.user_id}
				<div
					class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0"
				>
					<ProfileMenu bind:showDropdown={showProfileDropdown} />
				</div>
			{:else}
				<div class="flex items-center md:ml-12">
					<LoginButton />
				</div>
			{/if}
		</div>
	</div>

	<!-- Mobile menu, show/hide based on menu state. -->
	{#if is_mobile_menu_open}
		<div
			class="sm:hidden"
			id="mobile-menu"
			transition:slide={{ y: -100, duration: 200, easing: cubicInOut }}
		>
			<div class="pt-2 pb-4 space-y-1">
				<!-- Current: "bg-pink-50 border-pink-500 text-pink-700", Default: "border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700" -->
				<a
					href="#"
					class="bg-pink-50 border-pink-500 text-pink-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
					>Dashboard</a
				>
				<a
					href="#"
					class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
					>Team</a
				>
				<a
					href="#"
					class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
					>Projects</a
				>
				<a
					href="#"
					class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
					>Calendar</a
				>
			</div>
		</div>
	{/if}
</nav>
