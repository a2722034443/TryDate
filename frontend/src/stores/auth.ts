import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userApi } from '@/api'

interface User {
  id: string
  nickname: string
  gender: string
  gender_preference: string
  grade: string | null
  college_direction: string | null
  avatar_url: string | null
  bio: string
  questionnaire_completion: number
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref(localStorage.getItem('access_token'))

  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const needsQuestionnaire = computed(() =>
    user.value ? user.value.questionnaire_completion < 70 : false
  )

  async function fetchProfile() {
    try {
      const { data } = await userApi.getProfile()
      user.value = data
    } catch {
      logout()
    }
  }

  function setTokens(access: string, refresh: string, userData: User) {
    token.value = access
    user.value = userData
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  if (token.value) fetchProfile()

  return { user, token, isLoggedIn, needsQuestionnaire, fetchProfile, setTokens, logout }
})
