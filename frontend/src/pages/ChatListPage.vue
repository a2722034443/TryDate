<template>
  <div class="page-container pt-8 px-4">
    <h1 class="text-2xl font-black text-text-main mb-6">聊天 💬</h1>

    <div v-if="loading" class="space-y-3">
      <div v-for="i in 4" :key="i" class="card flex items-center gap-3 animate-pulse">
        <div class="w-12 h-12 rounded-full bg-lilac-pale"></div>
        <div class="flex-1 space-y-2">
          <div class="h-4 bg-lilac-pale rounded-xl w-1/3"></div>
          <div class="h-3 bg-lilac-pale rounded-xl w-2/3"></div>
        </div>
      </div>
    </div>

    <div v-else-if="rooms.length === 0" class="flex flex-col items-center justify-center min-h-[50vh] gap-4 text-center">
      <div class="w-24 h-24 rounded-full bg-gradient-soft flex items-center justify-center text-4xl shadow-card animate-float">
        💌
      </div>
      <div>
        <h3 class="text-lg font-black text-text-main mb-1">还没有对话</h3>
        <p class="text-text-sub text-sm">双方都选择心动后，才能解锁聊天</p>
      </div>
    </div>

    <div v-else class="space-y-2">
      <router-link v-for="room in rooms" :key="room.id" :to="`/app/chat/${room.id}`"
        class="card flex items-center gap-3 cursor-pointer hover:shadow-card-hover transition-shadow duration-200 active:scale-[0.98]">
        <!-- Avatar -->
        <div class="relative shrink-0">
          <div class="w-13 h-13 rounded-full overflow-hidden border-2 border-white shadow-sm bg-gradient-soft flex items-center justify-center text-xl"
            style="width:52px;height:52px">
            <img v-if="room.partner.avatar_url" :src="room.partner.avatar_url" class="w-full h-full object-cover" />
            <span v-else>{{ room.partner.gender === 'male' ? '🙋‍♂️' : '🙋‍♀️' }}</span>
          </div>
          <div v-if="room.unread_count > 0"
            class="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-pink-heart text-white text-[10px] font-bold flex items-center justify-center">
            {{ room.unread_count }}
          </div>
        </div>

        <!-- Info -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between">
            <span class="font-bold text-text-main text-sm">{{ room.partner.nickname }}</span>
            <span class="text-[11px] text-text-sub">{{ formatTime(room.last_message_at) }}</span>
          </div>
          <p class="text-xs text-text-sub truncate mt-0.5">
            {{ room.last_message?.content || '说点什么吧…' }}
          </p>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { chatApi } from '@/api'
import dayjs from 'dayjs'

const loading = ref(true)
const rooms = ref<any[]>([])

function formatTime(t: string) {
  if (!t) return ''
  const d = dayjs(t)
  if (d.isToday()) return d.format('HH:mm')
  if (d.isYesterday()) return '昨天'
  return d.format('M/D')
}

onMounted(async () => {
  try {
    const res = await chatApi.rooms()
    rooms.value = res.data
  } catch {} finally { loading.value = false }
})
</script>
