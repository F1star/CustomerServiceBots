import { defineStore } from 'pinia';

export const mainStore = defineStore('main', {
  state: () => ({
    username: '',
  }),
  getters: {},
  actions: {
    setUser(username) {
      this.username = username;
    }
  }
});
