<script context="module">
	export function load({ session }) {
		if (!session.user_id) {
			return {
				status: 302,
				redirect: `/`
			};
		}

		return {};
	}
</script>

<script>
	import ExampleBarChart from '$lib/ExampleBarChart.svelte';
	import TwitterStats from '$lib/TwitterStats.svelte';
</script>

<div class="py-10">
	<header>
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<h1 class="text-3xl font-bold leading-tight text-gray-900">Dashboard</h1>
		</div>
	</header>
	<main>
		<div class="max-w-5xl mx-auto sm:px-6 lg:px-8">
			<!-- Replace with your content -->
			<div class="px-4 py-8 sm:px-0">
				<TwitterStats />
			</div>
			<!-- /End replace -->
		</div>

		<div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
			<!-- Replace with your content -->
			<div class="px-4 py-8 sm:px-0">
				<ExampleBarChart />
			</div>
			<!-- /End replace -->
		</div>

		<div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
			<!-- Replace with your content -->
			<div class="px-4 py-8 sm:px-0">
				<ExampleBarChart />
			</div>
			<!-- /End replace -->
		</div>
	</main>
</div>
