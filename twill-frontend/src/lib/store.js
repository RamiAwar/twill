import { writable } from 'svelte/store';
import { browser } from '$app/env';

const storedUser = browser ? window.localStorage.getItem('userStore') ?? '{}' : '{}';
export const userStore = writable(JSON.parse(storedUser));

userStore.subscribe((user) => {
	if (browser) {
		window.localStorage.setItem('userStore', user ? JSON.stringify(user) : JSON.stringify({}));
	}
});
