import { writable } from 'svelte/store';
import { browser } from '$app/env';

const storedUser = browser ? window.localStorage.getItem('userStore') ?? '{}' : '{}';
console.log('stored user: ', storedUser);
export const userStore = writable(JSON.parse(storedUser));

userStore.subscribe((user) => {
	if (browser) {
		console.log('saving: ', user);
		window.localStorage.setItem('userStore', user ? JSON.stringify(user) : JSON.stringify({}));
	}
});
