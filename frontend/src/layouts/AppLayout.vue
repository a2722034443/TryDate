<template>
  <div class="min-h-dvh bg-gradient-page">
    <router-view v-slot="{ Component }">
      <transition name="page" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>

    <!-- Bottom Navigation -->
    <nav class="fixed bottom-0 left-0 right-0 z-50 safe-bottom">
      <div class="mx-auto max-w-md">
        <div class="glass bg-white/90 border-t border-white/60 rounded-t-3xl shadow-lg px-2 py-2">
          <div class="flex items-center justify-around">
            <NavItem to="/app/match" :active="route.path === '/app/match'">
              <template #icon>
                <HeartIcon class="w-6 h-6" :class="route.path === '/app/match' ? 'fill-pink-heart text-pink-heart' : 'text-text-sub'" />
              </template>
              <template #label>心动</template>
            </NavItem>
            <NavItem to="/app/chat" :active="route.path.startsWith('/app/chat')">
              <template #icon>
                <MessageCircleIcon class="w-6 h-6" />
              </template>
              <template #label>聊天</template>
            </NavItem>
            <NavItem to="/app/posts" :active="route.path === '/app/posts'">
              <template #icon>
                <FeatherIcon class="w-6 h-6" />
              </template>
              <template #label>动态</template>
            </NavItem>
            <NavItem to="/app/profile" :active="route.path === '/app/profile'">
              <template #icon>
                <UserIcon class="w-6 h-6" />
              </template>
              <template #label>我的</template>
            </NavItem>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { HeartIcon, MessageCircleIcon, FeatherIcon, UserIcon } from 'lucide-vue-next'
import NavItem from '@/components/NavItem.vue'

const route = useRoute()
</script>

<style scoped>
.page-enter-active, .page-leave-active {
  transition: all 0.25s ease;
}
.page-enter-from {
  opacity: 0;
  transform: translateY(12px);
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
