<template>
  <div class="page-container px-4 pt-8">

    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-black text-text-main">本周心动 💘</h1>
        <p class="text-sm text-text-sub">{{ weekLabel }}</p>
      </div>
      <router-link to="/app/history"
        class="text-xs font-bold text-pink-heart bg-pink-pale px-3 py-1.5 rounded-xl">
        历史记录
      </router-link>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center justify-center min-h-[60vh] gap-4">
      <div class="w-16 h-16 rounded-full bg-gradient-heart animate-pulse-heart flex items-center justify-center">
        <span class="text-2xl">💝</span>
      </div>
      <p class="text-text-sub font-semibold">缘分正在撮合中…</p>
    </div>

    <!-- No questionnaire -->
    <div v-else-if="needsQuestionnaire" class="flex flex-col items-center justify-center min-h-[60vh] gap-5 text-center px-4">
      <div class="w-24 h-24 rounded-full bg-gradient-soft flex items-center justify-center text-4xl shadow-card">📋</div>
      <div>
        <h3 class="text-xl font-black text-text-main mb-2">先完成灵魂问卷</h3>
        <p class="text-text-sub text-sm">完成问卷才能参与每周心动匹配哦～</p>
      </div>
      <router-link to="/app/questionnaire" class="btn-primary px-8 py-3.5">
        去完成问卷 ✨
      </router-link>
    </div>

    <!-- No match this week -->
    <div v-else-if="!matched" class="flex flex-col items-center justify-center min-h-[60vh] gap-5 text-center">
      <div class="relative">
        <div class="w-28 h-28 rounded-full bg-gradient-soft flex items-center justify-center text-5xl shadow-card animate-float">
          🔮
        </div>
        <div class="absolute -bottom-1 -right-1 w-8 h-8 rounded-full bg-lilac flex items-center justify-center text-sm shadow">⏳</div>
      </div>
      <div>
        <h3 class="text-xl font-black text-text-main mb-2">本周缘分还在路上</h3>
        <p class="text-text-sub text-sm max-w-xs">每周日 20:00 推送心动匹配<br/>先去聊聊天、刷动态吧 🌸</p>
      </div>
      <div class="flex gap-3">
        <router-link to="/app/posts" class="btn-outline px-5 py-3">逛逛动态</router-link>
        <router-link to="/app/questionnaire" class="btn-primary px-5 py-3">完善问卷</router-link>
      </div>
    </div>

    <!-- Match card -->
    <div v-else-if="matchData" class="animate-slide-up">

      <!-- Status badge -->
      <div class="flex justify-center mb-4">
        <div class="glass px-4 py-2 rounded-2xl border border-white/80 shadow-sm flex items-center gap-2">
          <div class="w-2 h-2 rounded-full" :class="statusColor"></div>
          <span class="text-sm font-bold text-text-main">{{ statusLabel }}</span>
        </div>
      </div>

      <!-- Match card with flip effect -->
      <div class="relative mx-auto max-w-sm">
        <div class="card overflow-hidden p-0">

          <!-- Avatar area -->
          <div class="relative bg-gradient-soft h-56 flex items-center justify-center">
            <div class="relative">
              <div class="w-28 h-28 rounded-full shadow-card overflow-hidden border-4 border-white"
                :class="matchData.status === 'matched' ? '' : 'filter blur-md scale-90'">
                <img v-if="matchData.partner.avatar_url && matchData.status === 'matched'"
                  :src="matchData.partner.avatar_url" class="w-full h-full object-cover" />
                <div v-else class="w-full h-full bg-gradient-heart flex items-center justify-center text-3xl">
                  {{ matchData.partner.gender === 'male' ? '🙋‍♂️' : '🙋‍♀️' }}
                </div>
              </div>
              <!-- Blur hint -->
              <div v-if="matchData.status !== 'matched'" class="absolute inset-0 flex items-center justify-center">
                <div class="bg-white/90 rounded-2xl px-3 py-1.5 text-xs font-bold text-pink-heart shadow">
                  双向心动后解锁头像 💝
                </div>
              </div>
            </div>

            <!-- Compatibility score badge -->
            <div class="absolute top-4 right-4 bg-white rounded-2xl px-3 py-2 shadow-card text-center">
              <div class="text-2xl font-black text-gradient">{{ matchData.compatibility_score }}%</div>
              <div class="text-[10px] text-text-sub font-semibold">契合度</div>
            </div>
          </div>

          <!-- Info -->
          <div class="p-5">
            <div class="flex items-center gap-2 mb-1">
              <h3 class="text-xl font-black text-text-main">{{ matchData.partner.nickname }}</h3>
              <span class="text-sm">{{ matchData.partner.gender === 'male' ? '♂️' : '♀️' }}</span>
            </div>
            <p class="text-text-sub text-sm mb-4">
              {{ matchData.partner.grade || '在校生' }}
              {{ matchData.partner.college_direction ? '· ' + matchData.partner.college_direction : '' }}
            </p>

            <!-- Compatibility highlights -->
            <div v-if="matchData.compatibility_highlights?.length" class="space-y-2 mb-4">
              <p v-for="(h, i) in matchData.compatibility_highlights" :key="i"
                class="text-xs bg-pink-pale rounded-xl px-3 py-2 text-pink-heart font-semibold flex items-start gap-1.5">
                <span class="mt-0.5">✨</span>{{ h }}
              </p>
            </div>

            <!-- Radar chart placeholder -->
            <div class="bg-gradient-soft rounded-2xl p-3 mb-4">
              <p class="text-xs font-bold text-text-sub mb-2">五维契合度</p>
              <div class="space-y-1.5">
                <div v-for="(score, dim) in matchData.dimension_scores" :key="dim" class="flex items-center gap-2">
                  <span class="text-xs text-text-sub w-16 shrink-0">{{ dimLabel(String(dim)) }}</span>
                  <div class="flex-1 h-1.5 bg-white/70 rounded-full overflow-hidden">
                    <div class="h-full bg-gradient-heart rounded-full transition-all duration-700"
                      :style="{ width: score + '%' }" />
                  </div>
                  <span class="text-xs font-bold text-pink-heart w-8 text-right">{{ score }}%</span>
                </div>
              </div>
            </div>

            <!-- Action buttons -->
            <div v-if="matchData.status === 'pending' && matchData.my_action === 'pending'" class="flex gap-3">
              <button @click="respond('passed')" :disabled="responding"
                class="flex-1 py-3.5 rounded-2xl border-2 border-lilac-pale bg-white font-bold text-text-sub active:scale-95 transition-all">
                再想想 🤔
              </button>
              <button @click="respond('liked')" :disabled="responding"
                class="flex-1 py-3.5 rounded-2xl bg-gradient-heart text-white font-bold shadow-card active:scale-95 transition-all animate-pulse-heart">
                心动 ❤️
              </button>
            </div>

            <!-- Already acted -->
            <div v-else-if="matchData.my_action !== 'pending'" class="text-center py-3">
              <span v-if="matchData.my_action === 'liked'" class="text-sm font-bold text-pink-heart">
                💌 你已发出心动，等待对方回应…
              </span>
              <span v-else class="text-sm font-semibold text-text-sub">你选择了再想想</span>
            </div>

            <!-- Matched! Go chat -->
            <div v-if="matchData.status === 'matched'" class="mt-3">
              <router-link to="/app/chat" class="btn-primary w-full py-3.5 text-center block">
                💬 开始聊天吧！
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Deadline hint -->
      <p v-if="matchData.status === 'pending'" class="text-center text-xs text-text-sub mt-3">
        ⏰ 截止时间：{{ deadline }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { matchApi } from '@/api'
import dayjs from 'dayjs'

const auth = useAuthStore()
const loading = ref(true)
const matched = ref(false)
const matchData = ref<any>(null)
const responding = ref(false)

const needsQuestionnaire = computed(() => auth.needsQuestionnaire)
const weekLabel = computed(() => `第 ${dayjs().week()} 周 · ${dayjs().format('YYYY年M月')}`)
const deadline = computed(() => matchData.value ? dayjs(matchData.value.action_deadline).format('M月D日 HH:mm') : '')
const statusColor = computed(() => {
  if (!matchData.value) return 'bg-gray-400'
  if (matchData.value.status === 'matched') return 'bg-mint animate-pulse'
  if (matchData.value.status === 'missed') return 'bg-gray-400'
  return 'bg-amber'
})
const statusLabel = computed(() => {
  if (!matchData.value) return ''
  const map: Record<string, string> = { matched: '双向心动 💝 已解锁聊天', missed: '已错过', pending: '等待双方确认' }
  return map[matchData.value.status] || ''
})

function dimLabel(dim: string) {
  const map: Record<string, string> = { basic:'基础偏好', values:'爱情观', lifestyle:'生活习惯', interests:'兴趣', date_pref:'约会偏好' }
  return map[dim] || dim
}

async function respond(action: 'liked' | 'passed') {
  if (!matchData.value) return
  responding.value = true
  try {
    const res = await matchApi.respond(matchData.value.id, action)
    matchData.value = res.data
  } catch {} finally { responding.value = false }
}

onMounted(async () => {
  try {
    const res = await matchApi.current()
    matched.value = res.data.matched
    if (res.data.matched) matchData.value = res.data.match
  } catch {} finally { loading.value = false }
})
</script>
