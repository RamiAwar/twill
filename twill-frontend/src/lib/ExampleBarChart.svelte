<script lang="ts">
	import { browser } from '$app/env';
	import { onMount } from 'svelte';
	import '@fontsource/merriweather';

	import { Chart, registerables } from 'chart.js';

	let barChartElement: HTMLCanvasElement;

	const data = [
		{ framework: 'SvelteKit', score: 96 },
		{ framework: 'Astro', score: 91 },
		{ framework: 'Fastify', score: 91 },
		{ framework: 'Next.js', score: 91 },
		{ framework: 'Remix', score: 91 },
		{ framework: 'Express', score: 88 },
		{ framework: 'Nest', score: 85 },
		{ framework: 'Eleventy', score: 82 },
		{ framework: 'Nuxt', score: 82 },
		{ framework: 'Strapi', score: 76 },
		{ framework: 'Blitz', score: 67 },
		{ framework: 'Redwood', score: 67 },
		{ framework: 'Gatsby', score: 51 }
	];

	const chartData = {
		labels: data.map(({ framework }) => framework),
		datasets: [
			{
				label: 'Satisfaction (%)',
				data: data.map(({ score }) => score),
				backgroundColor: [
					'hsl(347 38% 49%)',
					'hsl(346 65% 63%)',
					'hsl(346 49% 56%)',
					'hsl(346 89% 70%)',
					'hsl(346 90% 76%)',
					'hsl(346 90% 73%)',
					'hsl(346 89% 79%)',
					'hsl(346 89% 85%)',
					'hsl(347 89% 82%)',
					'hsl(346 90% 88%)',
					'hsl(347 87% 94%)',
					'hsl(347 91% 91%)',
					'hsl(346 87% 97%)'
				],
				// borderColor: ['hsl(43 100% 52%)'],
				borderRadius: 4
				// borderWidth: 2
			}
		]
	};

	onMount(() => {
		Chart.register(...registerables);

		if (browser) {
			new Chart(barChartElement, {
				type: 'bar',
				data: chartData,
				options: {
					plugins: {
						legend: {
							display: false
						}
					},
					scales: {
						x: {
							grid: {
								display: false
								// color: 'hsl(43 100% 52% / 10%)'
							},
							ticks: { color: 'hsl(43 100% 52% )' }
						},
						y: {
							beginAtZero: false,
							ticks: { color: 'hsl(43 100% 52% )', font: { size: 18 } },
							grid: {
								display: false
								// color: 'hsl(43 100% 52% / 40%)'
							},
							title: {
								display: true,
								text: 'Satisfaction (%)',
								color: 'hsl(43 100% 52% )',
								font: { size: 24, family: 'Merriweather' }
							}
						}
					}
				}
			});
		}
	});
</script>

<canvas bind:this={barChartElement} />
