<template>
  <div class="min-h-dvh bg-gradient-page">

    <!-- Top Navigation -->
    <nav class="fixed top-0 left-0 right-0 z-50">
      <div class="mx-auto max-w-md">
        <div class="bg-white/90 backdrop-blur-md border-b border-white/60 shadow-sm px-3 py-2">
          <div class="flex items-center justify-between">

            <!-- Brand -->
            <span class="text-base font-black text-gradient select-none">💝 TryDate</span>

            <!-- Tabs -->
            <div class="flex items-center gap-0.5">
              <TopNavItem to="/app/match" :active="route.path === '/app/match'" emoji="💘" label="心动" />
              <TopNavItem to="/app/chat" :active="route.path.startsWith('/app/chat')" emoji="💬" label="聊天" />
              <TopNavItem to="/app/posts" :active="route.path === '/app/posts'" emoji="🌸" label="动态" />
              <TopNavItem to="/app/profile" :active="route.path === '/app/profile'" emoji="👤" label="我的" />
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Page content — offset by nav height -->
    <div class="pt-14">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { defineComponent, h } from 'vue'
import { RouterLink } from 'vue-router'

const route = useRoute()

const TopNavItem = defineComponent({
  props: { to: String, active: Boolean, emoji: String, label: String },
  setup(props) {
    return () => h(RouterLink, { to: props.to! },
      () => h('div', {
        class: [
          'flex items-center gap-1 px-2.5 py-1.5 rounded-xl transition-all duration-200 cursor-pointer',
          props.active ? 'bg-pink-pale' : 'hover:bg-gray-50'
        ]
      }, [
        h('span', { class: 'text-base leading-none' }, props.emoji),
        h('span', {
          class: ['text-xs font-bold', props.active ? 'text-pink-heart' : 'text-text-sub']
        }, props.label)
      ])
    )
  }
})
</script>

<style scoped>
.page-enter-active, .page-leave-active { transition: all 0.22s ease; }
.page-enter-from { opacity: 0; transform: translateY(10px); }
.page-leave-to   { opacity: 0; transform: translateY(-6px); }
</style>
