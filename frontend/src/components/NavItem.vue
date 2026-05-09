<template>
  <router-link :to="to" class="flex flex-col items-center gap-0.5 px-4 py-1.5 rounded-2xl transition-all duration-200 min-w-[56px]"
    :class="active ? 'bg-pink-pale' : 'bg-transparent'">
    <span :class="active ? 'text-pink-heart' : 'text-text-sub'">
      <slot name="icon" />
    </span>
    <span class="text-[10px] font-bold" :class="active ? 'text-pink-heart' : 'text-text-sub'">
      <slot name="label" />
    </span>
  </router-link>
</template>

<script setup lang="ts">
defineProps<{ to: string; active: boolean }>()
</script>
