<script setup lang="ts">
defineProps<{
  icon?: string;
  message: string;
  actionLabel?: string;
}>();

const emit = defineEmits<{
  action: [];
}>();
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-4 py-20">
    <span class="material-symbols-outlined text-6xl opacity-30">
      {{ icon || "deployed_code" }}
    </span>
    <p class="text-lg opacity-50">{{ message }}</p>
    <button
      v-if="actionLabel"
      class="btn btn-primary btn-sm text-base-100"
      @click="emit('action')"
    >
      {{ actionLabel }}
    </button>
  </div>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    "FILL" 0,
    "wght" 300,
    "GRAD" -25,
    "opsz" 48;
}
</style>
