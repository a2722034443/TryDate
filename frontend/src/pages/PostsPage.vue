<template>
  <div class="page-container pt-8 px-4">
    <!-- Header -->
    <div class="flex items-center justify-between mb-5">
      <h1 class="text-2xl font-black text-text-main">话题动态 🌸</h1>
      <button @click="showCompose = true"
        class="w-10 h-10 rounded-xl bg-gradient-heart flex items-center justify-center shadow-card active:scale-95 transition-transform">
        <PlusIcon class="w-5 h-5 text-white" />
      </button>
    </div>

    <!-- Posts list -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 5" :key="i" class="card space-y-2 animate-pulse">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-full bg-lilac-pale"></div>
          <div class="h-3 bg-lilac-pale rounded-xl w-20"></div>
        </div>
        <div class="h-4 bg-lilac-pale rounded-xl"></div>
        <div class="h-4 bg-lilac-pale rounded-xl w-3/4"></div>
      </div>
    </div>

    <div v-else-if="posts.length === 0" class="flex flex-col items-center justify-center min-h-[50vh] gap-4 text-center">
      <div class="w-20 h-20 rounded-full bg-gradient-soft flex items-center justify-center text-3xl shadow-card animate-float">📭</div>
      <p class="text-text-sub text-sm">还没有动态，来发第一条吧！</p>
      <button @click="showCompose=true" class="btn-primary px-6 py-3">发布动态 🌸</button>
    </div>

    <div v-else class="space-y-3 pb-4">
      <transition-group name="list">
        <div v-for="post in posts" :key="post.id" class="card">
          <!-- Author row -->
          <div class="flex items-center gap-2.5 mb-3">
            <div class="w-9 h-9 rounded-full bg-gradient-soft flex items-center justify-center text-sm shadow-sm">
              {{ post.is_anonymous ? '🎭' : '🌸' }}
            </div>
            <div>
              <p class="text-sm font-bold text-text-main">{{ post.author_display }}</p>
              <p class="text-[11px] text-text-sub">{{ formatTime(post.created_at) }}</p>
            </div>
            <div v-if="post.is_anonymous" class="ml-auto">
              <span class="text-[10px] bg-lilac-pale text-lilac-deep px-2 py-0.5 rounded-full font-semibold">匿名</span>
            </div>
          </div>

          <!-- Content -->
          <p class="text-sm text-text-main leading-relaxed mb-3 font-medium">{{ post.content }}</p>

          <!-- Actions -->
          <div class="flex items-center gap-4 pt-2 border-t border-lilac-pale/50">
            <button @click="toggleLike(post)"
              class="flex items-center gap-1.5 transition-transform active:scale-110"
              :class="post.is_liked ? 'text-pink-heart' : 'text-text-sub'">
              <HeartIcon class="w-4 h-4" :class="post.is_liked ? 'fill-pink-heart' : ''" />
              <span class="text-xs font-bold">{{ post.like_count }}</span>
            </button>
          </div>
        </div>
      </transition-group>
    </div>

    <!-- Compose sheet -->
    <div v-if="showCompose" @click.self="showCompose=false"
      class="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-end">
      <div class="w-full bg-white rounded-t-3xl p-5 animate-slide-up shadow-2xl">
        <div class="w-10 h-1 bg-gray-200 rounded-full mx-auto mb-5"></div>
        <h3 class="text-lg font-black text-text-main mb-4">发布动态 🌸</h3>

        <textarea v-model="newContent" placeholder="说说你的校园故事…（最多200字）"
          maxlength="200" rows="4"
          class="input-field resize-none mb-3 text-sm" />

        <div class="flex items-center justify-between mb-4">
          <label class="flex items-center gap-2 cursor-pointer">
            <div @click="isAnonymous=!isAnonymous"
              class="w-10 h-6 rounded-full transition-colors duration-200 relative"
              :class="isAnonymous ? 'bg-gradient-heart' : 'bg-gray-200'">
              <div class="w-4 h-4 bg-white rounded-full absolute top-1 transition-transform duration-200 shadow"
                :class="isAnonymous ? 'translate-x-5' : 'translate-x-1'"></div>
            </div>
            <span class="text-sm font-semibold text-text-sub">匿名发布</span>
          </label>
          <span class="text-xs text-text-sub">{{ newContent.length }}/200</span>
        </div>

        <button @click="publishPost" :disabled="!newContent.trim() || publishing"
          class="btn-primary w-full py-3.5 disabled:opacity-40">
          {{ publishing ? '发布中…' : '发布 🌸' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { PlusIcon, HeartIcon } from 'lucide-vue-next'
import { toast } from 'vue3-toastify'
import { postsApi } from '@/api'
import dayjs from 'dayjs'

const loading = ref(true)
const posts = ref<any[]>([])
const showCompose = ref(false)
const newContent = ref('')
const isAnonymous = ref(false)
const publishing = ref(false)

function formatTime(t: string) {
  const d = dayjs(t)
  if (d.isToday()) return '今天 ' + d.format('HH:mm')
  return d.format('M月D日')
}

async function toggleLike(post: any) {
  try {
    const res = await postsApi.like(post.id)
    post.is_liked = res.data.liked
    post.like_count = res.data.like_count
  } catch {}
}

async function publishPost() {
  if (!newContent.value.trim()) return
  publishing.value = true
  try {
    const res = await postsApi.create({ content: newContent.value.trim(), is_anonymous: isAnonymous.value })
    posts.value.unshift(res.data)
    newContent.value = ''
    showCompose.value = false
    toast.success('发布成功 🌸')
  } catch {} finally { publishing.value = false }
}

onMounted(async () => {
  try {
    const res = await postsApi.list()
    posts.value = res.data.results || res.data
  } catch {} finally { loading.value = false }
})
</script>

<style scoped>
.list-enter-active { animation: slideUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.list-leave-active { animation: fadeOut 0.2s ease; }
@keyframes fadeOut { to { opacity: 0; transform: scale(0.95); } }
</style>
