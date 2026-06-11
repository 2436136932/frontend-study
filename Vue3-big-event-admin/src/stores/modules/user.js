import { ref,computed } from 'vue'
import { defineStore } from 'pinia'
import { userGetInfoService } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  const token = ref('')
  const user = ref({})

  const setToken = (newToken) => {
    token.value = newToken
  }
  const removeToken = () => {
    token.value = ''
  }

  const setUser = (obj) => {
    user.value = obj
  }

  const getUser = async () => {
    const res = await userGetInfoService()
    user.value = res.data.data
  }

  return { token, user, setToken, removeToken, setUser, getUser }
}, {
  persist: true,
})
