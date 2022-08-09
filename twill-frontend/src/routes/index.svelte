<script context="module">
	export function load({ session }) {
		if (session.user_id) {
			return {
				status: 302,
				redirect: `/dashboard`
			};
		}

		return {};
	}
</script>
