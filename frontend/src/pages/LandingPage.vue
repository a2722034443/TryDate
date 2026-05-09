<template>
  <div class="min-h-dvh relative overflow-hidden flex flex-col" style="background: linear-gradient(160deg,#FFF8F5 0%,#FFE4EC 45%,#EDE8FF 100%)">

    <!-- Floating decorative elements -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
      <div v-for="h in hearts" :key="h.id"
        class="absolute text-2xl select-none"
        :style="{ left: h.x+'%', top: h.y+'%', animationDelay: h.delay+'s', animationDuration: h.duration+'s', opacity: h.opacity, fontSize: h.size+'px' }"
        :class="['animate-float']">
        {{ h.emoji }}
      </div>
    </div>

    <!-- Header -->
    <header class="relative z-10 pt-safe flex items-center justify-between px-6 pt-8 pb-2">
      <div class="flex items-center gap-2">
        <span class="text-2xl">💝</span>
        <span class="text-xl font-black text-gradient">TryDate</span>
      </div>
      <router-link to="/login"
        class="text-sm font-bold text-pink-heart border-2 border-pink-heart/30 px-4 py-1.5 rounded-xl hover:bg-pink-pale transition-colors">
        登录
      </router-link>
    </header>

    <!-- Hero -->
    <main class="relative z-10 flex-1 flex flex-col items-center justify-center px-6 text-center pb-8">

      <!-- Big heart with pulse -->
      <div class="relative mb-6 animate-bounce-in">
        <div class="w-32 h-32 rounded-full bg-gradient-heart shadow-glow flex items-center justify-center animate-pulse-heart">
          <span class="text-5xl">💝</span>
        </div>
        <div class="absolute -top-2 -right-2 w-8 h-8 rounded-full bg-lilac flex items-center justify-center text-sm shadow-md animate-float-delayed">✨</div>
        <div class="absolute -bottom-1 -left-3 w-7 h-7 rounded-full bg-mint flex items-center justify-center text-xs shadow-md animate-float-slow">💫</div>
      </div>

      <h1 class="text-4xl font-black leading-tight mb-3">
        <span class="text-gradient">在最好的年纪</span><br/>
        <span class="text-text-main">遇见刚刚好的你</span>
      </h1>
      <p class="text-text-sub text-base font-medium mb-10 max-w-xs leading-relaxed">
        不靠颜值滤镜，灵魂问卷 + 双向稳定匹配<br/>帮你找到那个「感觉刚刚好」的人 🌸
      </p>

      <!-- CTA -->
      <div class="w-full max-w-xs space-y-3">
        <router-link to="/login" class="btn-primary w-full text-base py-4 shadow-glow">
          开始心动之旅 💘
        </router-link>
        <p class="text-xs text-text-sub">已有 2000+ 同学在寻找 ta</p>
      </div>

      <!-- Feature chips -->
      <div class="flex flex-wrap gap-2 justify-center mt-10">
        <span v-for="f in features" :key="f" class="glass px-3 py-1.5 rounded-full text-xs font-semibold text-text-main border border-white/80 shadow-sm">
          {{ f }}
        </span>
      </div>
    </main>

    <!-- Decorative bottom blob -->
    <div class="absolute bottom-0 left-0 right-0 h-32 pointer-events-none">
      <svg viewBox="0 0 400 100" preserveAspectRatio="none" class="w-full h-full opacity-20">
        <path d="M0,60 Q100,0 200,60 Q300,120 400,40 L400,100 L0,100 Z" fill="#FF6B8A"/>
      </svg>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const hearts = ref(
  Array.from({ length: 12 }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    delay: Math.random() * 4,
    duration: 5 + Math.random() * 5,
    opacity: 0.15 + Math.random() * 0.25,
    size: 16 + Math.random() * 24,
    emoji: ['💕','💗','✨','🌸','💫','🩷','💝'][Math.floor(Math.random() * 7)],
  }))
)

const features = ['灵魂问卷测试', '每周心动推送', '双向确认机制', '匿名话题广场', '实时聊天']
</script>
