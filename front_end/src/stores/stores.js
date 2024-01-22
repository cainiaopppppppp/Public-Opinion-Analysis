// /src/stores/stores.js
import { defineStore } from 'pinia'
export const useUserStore = defineStore('user', {
  state: () => {
    return {
      isLoggedIn: false,
      id: '',
      uid: '',
      username: ''
    }
  }
})
