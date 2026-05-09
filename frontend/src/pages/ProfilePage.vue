<template>
  <div class="page-container pt-8 px-4">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-black text-text-main">我的 🌸</h1>
      <button @click="editing = !editing"
        class="text-xs font-bold px-3 py-1.5 rounded-xl transition-colors"
        :class="editing ? 'bg-pink-heart text-white' : 'bg-pink-pale text-pink-heart'">
        {{ editing ? '保存' : '编辑' }}
      </button>
    </div>

    <div v-if="!user" class="flex justify-center pt-20">
      <div class="w-12 h-12 rounded-full bg-gradient-heart animate-pulse-heart flex items-center justify-center">
        <span class="text-xl">💝</span>
      </div>
    </div>

    <div v-else class="space-y-4 animate-slide-up">
      <!-- Avatar & basic info card -->
      <div class="card text-center relative overflow-hidden">
        <div class="absolute top-0 left-0 right-0 h-24 bg-gradient-heart opacity-10 rounded-t-3xl"></div>
        <div class="relative pt-2">
          <div class="relative inline-block mb-3">
            <div class="w-24 h-24 rounded-full overflow-hidden border-4 border-white shadow-card bg-gradient-soft mx-auto flex items-center justify-center text-3xl">
              <img v-if="user.avatar_url" :src="user.avatar_url" class="w-full h-full object-cover" />
              <span v-else>{{ user.gender === 'male' ? '🙋‍♂️' : '🙋‍♀️' }}</span>
            </div>
            <label v-if="editing" class="absolute bottom-0 right-0 w-7 h-7 bg-gradient-heart rounded-full flex items-center justify-center cursor-pointer shadow-md">
              <CameraIcon class="w-3.5 h-3.5 text-white" />
              <input type="file" accept="image/*" class="hidden" @change="uploadAvatar" />
            </label>
          </div>

          <div v-if="!editing">
            <h2 class="text-xl font-black text-text-main">{{ user.nickname }}</h2>
            <p class="text-text-sub text-sm mt-0.5">{{ user.bio || '这个人很懒，什么都没写～' }}</p>
          </div>
          <div v-else class="space-y-2 text-left">
            <input v-model="form.nickname" class="input-field text-sm" placeholder="昵称" maxlength="30" />
            <input v-model="form.bio" class="input-field text-sm" placeholder="个性签名（最多50字）" maxlength="50" />
          </div>
        </div>
      </div>

      <!-- Questionnaire progress -->
      <div class="card">
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center gap-2">
            <span class="text-lg">✨</span>
            <span class="font-bold text-text-main text-sm">灵魂问卷完成度</span>
          </div>
          <span class="text-sm font-black text-gradient">{{ user.questionnaire_completion }}%</span>
        </div>
        <div class="h-2.5 bg-lilac-pale rounded-full overflow-hidden">
          <div class="h-full bg-gradient-heart rounded-full transition-all duration-700"
            :style="{ width: user.questionnaire_completion + '%' }" />
        </div>
        <p v-if="user.questionnaire_completion < 70" class="text-xs text-text-sub mt-2">
          完成度达到 70% 才能参与每周匹配 ·
          <router-link to="/app/questionnaire" class="text-pink-heart font-bold">去完善 →</router-link>
        </p>
      </div>

      <!-- Info card -->
      <div class="card space-y-3">
        <h3 class="font-black text-text-main text-sm mb-1">基本信息</h3>

        <div v-if="!editing" class="space-y-2.5">
          <InfoRow icon="🎓" label="年级" :value="gradeLabel(user.grade)" />
          <InfoRow icon="📚" label="专业方向" :value="collegeLabel(user.college_direction)" />
          <InfoRow icon="💫" label="期望对象" :value="prefLabel(user.gender_preference)" />
          <InfoRow icon="🎂" label="出生年份" :value="user.birth_year ? user.birth_year + '年' : '未填写'" />
        </div>

        <div v-else class="space-y-2">
          <select v-model="form.grade" class="input-field text-sm">
            <option value="">年级</option>
            <option v-for="g in grades" :key="g.value" :value="g.value">{{ g.label }}</option>
          </select>
          <select v-model="form.college_direction" class="input-field text-sm">
            <option value="">专业方向</option>
            <option v-for="c in colleges" :key="c.value" :value="c.value">{{ c.label }}</option>
          </select>
          <select v-model="form.gender_preference" class="input-field text-sm">
            <option value="female">期望女生</option>
            <option value="male">期望男生</option>
            <option value="both">不限</option>
          </select>
        </div>
      </div>

      <!-- Actions -->
      <div class="card space-y-1">
        <router-link to="/app/questionnaire"
          class="flex items-center justify-between py-3 border-b border-lilac-pale/50">
          <div class="flex items-center gap-3">
            <span class="w-8 h-8 rounded-xl bg-gradient-soft flex items-center justify-center text-sm">🧠</span>
            <span class="font-semibold text-text-main text-sm">修改灵魂问卷</span>
          </div>
          <ChevronRightIcon class="w-4 h-4 text-text-sub" />
        </router-link>
        <router-link to="/app/history"
          class="flex items-center justify-between py-3 border-b border-lilac-pale/50">
          <div class="flex items-center gap-3">
            <span class="w-8 h-8 rounded-xl bg-gradient-soft flex items-center justify-center text-sm">💕</span>
            <span class="font-semibold text-text-main text-sm">匹配历史</span>
          </div>
          <ChevronRightIcon class="w-4 h-4 text-text-sub" />
        </router-link>
        <button @click="logout" class="w-full flex items-center justify-between py-3">
          <div class="flex items-center gap-3">
            <span class="w-8 h-8 rounded-xl bg-red-50 flex items-center justify-center text-sm">🚪</span>
            <span class="font-semibold text-red-400 text-sm">退出登录</span>
          </div>
          <ChevronRightIcon class="w-4 h-4 text-text-sub" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { CameraIcon, ChevronRightIcon } from 'lucide-vue-next'
import { toast } from 'vue3-toastify'
import { userApi } from '@/api'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const editing = ref(false)
const user = computed(() => auth.user)

const form = reactive({ nickname: '', bio: '', grade: '', college_direction: '', gender_preference: '', birth_year: '' })

const grades = [
  { value: 'freshman', label: '大一' }, { value: 'sophomore', label: '大二' },
  { value: 'junior', label: '大三' }, { value: 'senior', label: '大四' },
  { value: 'master1', label: '研一' }, { value: 'master2', label: '研二' },
]
const colleges = [
  { value: 'stem', label: '理工' }, { value: 'humanities', label: '文史' },
  { value: 'art', label: '艺术设计' }, { value: 'business', label: '经管' },
  { value: 'medicine', label: '医学' }, { value: 'other', label: '其他' },
]

const gradeLabel = (v: string | null) => grades.find(g => g.value === v)?.label || '未填写'
const collegeLabel = (v: string | null) => colleges.find(c => c.value === v)?.label || '未填写'
const prefLabel = (v: string) => ({ female: '女生', male: '男生', both: '不限' }[v] || '未填写')

watch(editing, async (val) => {
  if (val && user.value) {
    Object.assign(form, { nickname: user.value.nickname, bio: user.value.bio, grade: user.value.grade || '', college_direction: user.value.college_direction || '', gender_preference: user.value.gender_preference })
  } else if (!val) {
    await saveProfile()
  }
})

async function saveProfile() {
  try {
    const fd = new FormData()
    Object.entries(form).forEach(([k, v]) => { if (v) fd.append(k, v) })
    await userApi.updateProfile(fd)
    await auth.fetchProfile()
    toast.success('资料已更新 ✨')
  } catch { toast.error('保存失败') }
}

async function uploadAvatar(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  const fd = new FormData()
  fd.append('avatar', file)
  try {
    await userApi.updateProfile(fd)
    await auth.fetchProfile()
    toast.success('头像已更新 🌸')
  } catch { toast.error('上传失败') }
}

function logout() {
  auth.logout()
  router.push('/')
}

const InfoRow = {
  props: ['icon', 'label', 'value'],
  template: `<div class="flex items-center gap-3"><span class="text-base w-6 text-center">{{icon}}</span><span class="text-xs text-text-sub flex-1">{{label}}</span><span class="text-sm font-semibold text-text-main">{{value}}</span></div>`
}
</script>
