<template>
  <div class="min-h-dvh page-container" style="background:linear-gradient(160deg,#FFF8F5 0%,#FFE4EC 45%,#EDE8FF 100%)">
    <!-- Header -->
    <div class="px-5 pt-8 pb-4">
      <div class="flex items-center gap-3 mb-4">
        <router-link to="/app/match" class="w-9 h-9 rounded-xl bg-white/70 flex items-center justify-center shadow-sm">
          <ArrowLeftIcon class="w-5 h-5 text-text-main" />
        </router-link>
        <div>
          <h1 class="text-lg font-black text-text-main">灵魂测试 ✨</h1>
          <p class="text-xs text-text-sub">第 {{ currentStep + 1 }} / {{ questions.length }} 题</p>
        </div>
      </div>
      <!-- Progress bar -->
      <div class="h-2 bg-white/60 rounded-full overflow-hidden shadow-inner">
        <div class="h-full bg-gradient-heart rounded-full transition-all duration-500"
          :style="{ width: ((currentStep + 1) / questions.length * 100) + '%' }" />
      </div>
    </div>

    <!-- Question card -->
    <div class="px-5 py-2">
      <transition name="q-slide" mode="out-in">
        <div :key="currentStep" class="card animate-slide-up">

          <!-- Dimension badge -->
          <div class="inline-flex items-center gap-1.5 bg-gradient-soft px-3 py-1 rounded-full mb-4">
            <span class="text-sm">{{ questions[currentStep].emoji }}</span>
            <span class="text-xs font-bold text-pink-heart">{{ questions[currentStep].dimension }}</span>
          </div>

          <h3 class="text-lg font-black text-text-main mb-5 leading-snug">
            {{ questions[currentStep].text }}
          </h3>

          <!-- Options -->
          <div class="space-y-2.5">
            <button v-for="(opt, oi) in questions[currentStep].options" :key="oi"
              @click="selectAnswer(opt.value)"
              class="w-full text-left px-4 py-3.5 rounded-2xl border-2 font-semibold text-sm transition-all duration-200 active:scale-98"
              :class="answers[questions[currentStep].key] === opt.value
                ? 'border-pink-heart bg-pink-pale text-pink-heart shadow-card'
                : 'border-lilac-pale bg-white/70 text-text-main hover:border-lilac'">
              <span class="mr-2">{{ opt.emoji }}</span>{{ opt.label }}
            </button>
          </div>
        </div>
      </transition>
    </div>

    <!-- Navigation buttons -->
    <div class="fixed bottom-0 left-0 right-0 p-5 safe-bottom bg-gradient-to-t from-cream/90 to-transparent">
      <div class="max-w-sm mx-auto flex gap-3">
        <button v-if="currentStep > 0" @click="prev"
          class="btn-outline flex-1 py-3.5">
          ← 上一题
        </button>
        <button @click="next" :disabled="!answers[questions[currentStep].key] && !questions[currentStep].optional"
          class="btn-primary flex-1 py-3.5 disabled:opacity-40">
          {{ currentStep === questions.length - 1 ? '完成测试 🎉' : '下一题 →' }}
        </button>
      </div>
    </div>

    <!-- Completion overlay -->
    <div v-if="completed" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
      <div class="card max-w-xs w-full mx-4 text-center animate-bounce-in">
        <div class="text-6xl mb-4">🎉</div>
        <h3 class="text-xl font-black text-text-main mb-2">灵魂问卷完成！</h3>
        <p class="text-text-sub text-sm mb-5">完成度 {{ completion }}%，可以参与每周心动匹配了</p>
        <button @click="goToMatch" class="btn-primary w-full py-3.5">去看本周心动 💘</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeftIcon } from 'lucide-vue-next'
import { toast } from 'vue3-toastify'
import { questionnaireApi } from '@/api'

const router = useRouter()
const currentStep = ref(0)
const completed = ref(false)
const completion = ref(0)
const answers = reactive<Record<string, string | string[]>>({})

const questions = [
  { key:'sleep_schedule', dimension:'生活习惯', emoji:'🌙', text:'你是什么类型的人？', options:[{value:'early_bird',emoji:'🌅',label:'早鸟型，7点前起床'},{value:'normal',emoji:'☀️',label:'普通作息，8-10点'},{value:'night_owl',emoji:'🌙',label:'夜猫子，12点后睡'}] },
  { key:'personality_type', dimension:'性格特质', emoji:'✨', text:'你更接近哪种性格？', options:[{value:'extrovert',emoji:'🎉',label:'外向，喜欢热闹'},{value:'ambivert',emoji:'🌿',label:'随心所欲，两者皆可'},{value:'introvert',emoji:'📚',label:'内向，享受独处'}] },
  { key:'love_priorities', dimension:'爱情观', emoji:'💕', text:'恋爱中你最看重什么？', options:[{value:'understanding',emoji:'🤝',label:'理解与陪伴'},{value:'growth',emoji:'🌱',label:'共同成长进步'},{value:'fun',emoji:'🎊',label:'快乐与浪漫'},{value:'stability',emoji:'🏠',label:'稳定与安全感'}] },
  { key:'conflict_style', dimension:'爱情观', emoji:'💬', text:'吵架了你倾向于怎么做？', options:[{value:'talk_now',emoji:'🗣️',label:'立刻沟通，不隔夜'},{value:'cool_down',emoji:'❄️',label:'先冷静，再聊'},{value:'hug_first',emoji:'🤗',label:'抱一抱，用行动说话'}] },
  { key:'ideal_weekend', dimension:'生活习惯', emoji:'🎡', text:'理想的周末是？', options:[{value:'outdoor',emoji:'🏕️',label:'户外探险、运动'},{value:'social',emoji:'☕',label:'逛街、咖啡、看展'},{value:'homebody',emoji:'🛋️',label:'宅家追剧、打游戏'},{value:'learning',emoji:'📖',label:'读书、学习充电'}] },
  { key:'space_need', dimension:'爱情观', emoji:'🌊', text:'你在恋爱中需要多少私人空间？', options:[{value:'1',emoji:'🔥',label:'黏糊糊最好，24小时在一起'},{value:'2',emoji:'🌸',label:'大部分时间在一起'},{value:'3',emoji:'⚖️',label:'各自有自己的时间'},{value:'4',emoji:'🌙',label:'需要较多独处时间'}] },
  { key:'future_plan', dimension:'爱情观', emoji:'🌟', text:'毕业后你打算？', options:[{value:'local',emoji:'🏡',label:'留在本城市'},{value:'return_home',emoji:'🏘️',label:'回老家发展'},{value:'open',emoji:'🌍',label:'哪里好就去哪里'},{value:'abroad',emoji:'✈️',label:'出国深造或工作'}] },
  { key:'hobbies', dimension:'兴趣爱好', emoji:'🎨', text:'业余时间最常做什么？（可多选思维）', options:[{value:'music',emoji:'🎵',label:'听音乐/演奏'},{value:'movies',emoji:'🎬',label:'看电影/追剧'},{value:'sports',emoji:'⚽',label:'运动健身'},{value:'games',emoji:'🎮',label:'游戏'}] },
  { key:'ideal_first_date', dimension:'约会偏好', emoji:'🌹', text:'第一次约会，你更想去？', options:[{value:'cafe',emoji:'☕',label:'安静的咖啡馆'},{value:'walk',emoji:'🚶',label:'边走边聊、逛街'},{value:'activity',emoji:'🎳',label:'一起做个小活动'},{value:'meal',emoji:'🍜',label:'吃一顿好吃的'}] },
  { key:'mbti', dimension:'性格特质', emoji:'🔮', text:'你的 MBTI 是？', optional: true, options:[{value:'INFP',emoji:'🌙',label:'INFP'},{value:'ENFP',emoji:'🌟',label:'ENFP'},{value:'INTJ',emoji:'🔭',label:'INTJ'},{value:'ENTJ',emoji:'⚡',label:'ENTJ'},{value:'INFJ',emoji:'💫',label:'INFJ'},{value:'ENFJ',emoji:'☀️',label:'ENFJ'},{value:'other',emoji:'🎭',label:'其他/不清楚'}] },
]

function selectAnswer(value: string) {
  answers[questions[currentStep.value].key] = value
}

function next() {
  if (currentStep.value < questions.length - 1) {
    currentStep.value++
  } else {
    submit()
  }
}

function prev() {
  if (currentStep.value > 0) currentStep.value--
}

async function submit() {
  try {
    const res = await questionnaireApi.patch(answers)
    completion.value = res.data.completion_rate
    completed.value = true
  } catch { toast.error('提交失败，请重试') }
}

async function goToMatch() {
  await router.push('/app/match')
}

onMounted(async () => {
  try {
    const res = await questionnaireApi.get()
    if (res.data.answers) Object.assign(answers, res.data.answers)
  } catch {}
})
</script>

<style scoped>
.q-slide-enter-active, .q-slide-leave-active { transition: all 0.3s ease; }
.q-slide-enter-from { opacity: 0; transform: translateX(30px); }
.q-slide-leave-to { opacity: 0; transform: translateX(-30px); }
</style>
