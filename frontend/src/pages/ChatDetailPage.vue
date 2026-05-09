<template>
  <div class="flex flex-col h-dvh">
    <!-- Header -->
    <div class="glass bg-white/90 px-4 pt-safe pt-10 pb-3 flex items-center gap-3 border-b border-white/60 shadow-sm">
      <router-link to="/app/chat" class="w-9 h-9 rounded-xl bg-cream flex items-center justify-center">
        <ArrowLeftIcon class="w-5 h-5 text-text-main" />
      </router-link>
      <div class="w-10 h-10 rounded-full overflow-hidden bg-gradient-soft flex items-center justify-center text-lg border-2 border-white shadow-sm">
        <img v-if="partnerAvatar" :src="partnerAvatar" class="w-full h-full object-cover" />
        <span v-else>💝</span>
      </div>
      <div class="flex-1">
        <h2 class="font-black text-text-main text-sm leading-tight">{{ partnerName }}</h2>
        <p class="text-[11px] text-mint font-semibold">在线</p>
      </div>
      <button @click="showMenu = !showMenu" class="w-9 h-9 rounded-xl bg-cream flex items-center justify-center">
        <MoreHorizontalIcon class="w-5 h-5 text-text-sub" />
      </button>
    </div>

    <!-- Messages -->
    <div ref="msgContainer" class="flex-1 overflow-y-auto px-4 py-4 space-y-3"
      style="background:linear-gradient(180deg,#FFF8F5 0%,#FFE4EC 100%)">
      <div v-for="msg in messages" :key="msg.id"
        :class="msg.sender_id === myId ? 'flex justify-end' : 'flex justify-start'"
        class="animate-fade-in">
        <div class="max-w-[75%]">
          <div class="px-4 py-2.5 rounded-2xl text-sm font-medium leading-relaxed shadow-sm"
            :class="msg.sender_id === myId
              ? 'bg-gradient-heart text-white rounded-br-md'
              : 'bg-white text-text-main rounded-bl-md'">
            <img v-if="msg.msg_type === 'image'" :src="msg.content" class="rounded-xl max-w-[200px]" />
            <span v-else>{{ msg.content }}</span>
          </div>
          <p class="text-[10px] text-text-sub mt-1"
            :class="msg.sender_id === myId ? 'text-right' : 'text-left'">
            {{ formatMsgTime(msg.created_at) }}
          </p>
        </div>
      </div>

      <!-- Typing indicator -->
      <div v-if="partnerTyping" class="flex justify-start">
        <div class="bg-white rounded-2xl rounded-bl-md px-4 py-3 shadow-sm flex gap-1 items-center">
          <span v-for="i in 3" :key="i" class="w-1.5 h-1.5 rounded-full bg-text-sub animate-bounce"
            :style="{ animationDelay: (i * 0.15) + 's' }"></span>
        </div>
      </div>
    </div>

    <!-- Input area -->
    <div class="glass bg-white/95 border-t border-white/60 px-4 pt-3 pb-safe safe-bottom"
      style="padding-bottom: max(12px, env(safe-area-inset-bottom))">
      <div class="flex items-end gap-2 max-w-lg mx-auto">
        <label class="w-10 h-10 rounded-xl bg-lilac-pale flex items-center justify-center cursor-pointer shrink-0 active:scale-95 transition-transform">
          <ImageIcon class="w-5 h-5 text-lilac-deep" />
          <input type="file" accept="image/*" class="hidden" @change="sendImage" />
        </label>
        <div class="flex-1 relative">
          <textarea v-model="inputText" @keydown.enter.prevent="sendMessage"
            placeholder="说点什么…" rows="1"
            class="w-full px-4 py-2.5 rounded-2xl bg-cream border-2 border-lilac-pale text-text-main placeholder-text-sub outline-none focus:border-lilac resize-none text-sm font-medium"
            style="max-height:120px;overflow-y:auto" />
        </div>
        <button @click="sendMessage" :disabled="!inputText.trim() || sending"
          class="w-10 h-10 rounded-xl flex items-center justify-center shrink-0 transition-all active:scale-95 disabled:opacity-40"
          :class="inputText.trim() ? 'bg-gradient-heart shadow-card' : 'bg-lilac-pale'">
          <SendIcon class="w-4 h-4" :class="inputText.trim() ? 'text-white' : 'text-text-sub'" />
        </button>
      </div>
    </div>

    <!-- Report/Block menu -->
    <div v-if="showMenu" @click.self="showMenu=false"
      class="fixed inset-0 z-40 bg-black/30 backdrop-blur-sm flex items-end">
      <div class="w-full bg-white rounded-t-3xl p-5 space-y-3 animate-slide-up">
        <div class="w-10 h-1 bg-gray-200 rounded-full mx-auto mb-4"></div>
        <button @click="reportUser" class="w-full py-3.5 rounded-2xl bg-amber/10 text-amber font-bold text-sm flex items-center justify-center gap-2">
          <FlagIcon class="w-4 h-4" /> 举报该用户
        </button>
        <button @click="blockUser" class="w-full py-3.5 rounded-2xl bg-red-50 text-red-500 font-bold text-sm flex items-center justify-center gap-2">
          <BanIcon class="w-4 h-4" /> 拉黑并屏蔽
        </button>
        <button @click="showMenu=false" class="w-full py-3 text-text-sub font-semibold text-sm">取消</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeftIcon, MoreHorizontalIcon, ImageIcon, SendIcon, FlagIcon, BanIcon } from 'lucide-vue-next'
import { toast } from 'vue3-toastify'
import { chatApi } from '@/api'
import { useAuthStore } from '@/stores/auth'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const roomId = route.params.id as string
const messages = ref<any[]>([])
const inputText = ref('')
const sending = ref(false)
const showMenu = ref(false)
const msgContainer = ref<HTMLElement>()
const partnerTyping = ref(false)
const partnerName = ref('...')
const partnerAvatar = ref('')

const myId = computed(() => auth.user?.id)
let ws: WebSocket | null = null

function formatMsgTime(t: string) { return dayjs(t).format('HH:mm') }

async function sendMessage() {
  const text = inputText.value.trim()
  if (!text || sending.value) return
  sending.value = true
  ws?.send(JSON.stringify({ type: 'text', content: text }))
  inputText.value = ''
  sending.value = false
}

async function sendImage(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  const fd = new FormData()
  fd.append('image', file)
  try {
    const res = await chatApi.uploadImage(parseInt(roomId), fd)
    messages.value.push(res.data)
    scrollBottom()
  } catch { toast.error('图片发送失败') }
}

function scrollBottom() {
  nextTick(() => { if (msgContainer.value) msgContainer.value.scrollTop = msgContainer.value.scrollHeight })
}

function connectWS() {
  const token = localStorage.getItem('access_token')
  ws = new WebSocket(`ws://localhost:8000/ws/chat/${roomId}/`)
  ws.onmessage = (e) => {
    const data = JSON.parse(e.data)
    if (data.type === 'chat_message') {
      messages.value.push(data)
      scrollBottom()
    }
  }
  ws.onclose = () => setTimeout(connectWS, 3000)
}

async function reportUser() {
  showMenu.value = false
  toast.info('举报功能开发中')
}

async function blockUser() {
  showMenu.value = false
  toast.success('已屏蔽该用户')
  router.push('/app/chat')
}

onMounted(async () => {
  try {
    const res = await chatApi.messages(parseInt(roomId))
    messages.value = res.data
    scrollBottom()
  } catch {}
  connectWS()
})

onUnmounted(() => { ws?.close() })
</script>
