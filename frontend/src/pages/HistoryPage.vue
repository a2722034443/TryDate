<template>
  <div class="page-container pt-8 px-4">
    <div class="flex items-center gap-3 mb-6">
      <router-link to="/app/match" class="w-9 h-9 rounded-xl bg-white/70 flex items-center justify-center shadow-sm">
        <ArrowLeftIcon class="w-5 h-5 text-text-main" />
      </router-link>
      <h1 class="text-xl font-black text-text-main">匹配历史 💕</h1>
    </div>

    <div v-if="loading" class="space-y-3">
      <div v-for="i in 5" :key="i" class="card flex items-center gap-3 animate-pulse">
        <div class="w-12 h-12 rounded-full bg-lilac-pale shrink-0"></div>
        <div class="flex-1 space-y-2">
          <div class="h-4 bg-lilac-pale rounded-xl w-1/3"></div>
          <div class="h-3 bg-lilac-pale rounded-xl w-1/2"></div>
        </div>
      </div>
    </div>

    <div v-else-if="history.length === 0" class="flex flex-col items-center justify-center min-h-[50vh] gap-4 text-center">
      <div class="w-20 h-20 rounded-full bg-gradient-soft flex items-center justify-center text-3xl shadow-card animate-float">💫</div>
      <p class="text-text-sub text-sm">还没有匹配记录</p>
    </div>

    <div v-else class="space-y-3">
      <div v-for="match in history" :key="match.id"
        class="card flex items-center gap-3 animate-fade-in">
        <!-- Avatar -->
        <div class="w-12 h-12 rounded-full overflow-hidden bg-gradient-soft flex items-center justify-center text-xl shrink-0 border-2 border-white shadow-sm"
          :class="match.status !== 'matched' ? 'filter blur-sm' : ''">
          <img v-if="match.partner.avatar_url && match.status === 'matched'" :src="match.partner.avatar_url" class="w-full h-full object-cover" />
          <span v-else>{{ match.partner.gender === 'male' ? '🙋‍♂️' : '🙋‍♀️' }}</span>
        </div>

        <!-- Info -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2">
            <span class="font-bold text-text-main text-sm">
              {{ match.status === 'matched' ? match.partner.nickname : '神秘 TA' }}
            </span>
            <span class="text-xs font-black text-gradient">{{ match.compatibility_score }}%</span>
          </div>
          <p class="text-[11px] text-text-sub">{{ match.week_number }}</p>
        </div>

        <!-- Status badge -->
        <div class="shrink-0">
          <span class="text-xs font-bold px-2.5 py-1 rounded-xl"
            :class="{
              'bg-mint/20 text-mint': match.status === 'matched',
              'bg-gray-100 text-gray-400': match.status === 'missed',
              'bg-amber/20 text-amber': match.status === 'pending',
            }">
            {{ { matched: '💝 心动', missed: '已错过', pending: '等待中' }[match.status] }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ArrowLeftIcon } from 'lucide-vue-next'
import { matchApi } from '@/api'

const loading = ref(true)
const history = ref<any[]>([])

onMounted(async () => {
  try {
    const res = await matchApi.history()
    history.value = res.data
  } catch {} finally { loading.value = false }
})
</script>
