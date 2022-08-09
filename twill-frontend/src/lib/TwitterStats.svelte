<script>
	import Stats from '$lib/Stats.svelte';
</script>

<div>
	<h3 class="text-lg leading-6 font-bold text-gray-900">
		Today <span class="text-sm text-gray-500 ml-4 font-normal">Compared to 14 day averages</span>
	</h3>

	<dl
		class="mt-5 grid grid-cols-1 rounded-lg bg-white overflow-hidden shadow divide-y divide-gray-200 md:grid-cols-4 md:divide-y-0 md:divide-x"
	>
		<Stats title="Followers" previousValue="1255" />
		<Stats title="Followers" />
		<Stats title="Followers" />
		<Stats title="Followers" />
	</dl>
</div>
