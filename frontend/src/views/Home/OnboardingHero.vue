<script setup lang="ts">
const emit = defineEmits<{
  openOnboarding: [];
}>();
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-[60vh] gap-8">
    <div class="text-center">
      <h1 class="text-4xl font-bold mb-4">🎉 欢迎使用 NoneBot WebUI</h1>
      <p class="text-lg text-base-content/70">创建你的第一个机器人实例开始使用</p>
    </div>

    <div class="flex flex-col sm:flex-row gap-4">
      <button
        class="btn btn-primary btn-lg text-base-100"
        @click="emit('openOnboarding')"
      >
        <span class="material-symbols-outlined"> add_circle </span>
        创建新实例
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-3xl mt-8">
      <a
        href="https://nonebot.dev"
        target="_blank"
        class="p-4 border border-base-content/20 rounded-box flex flex-col gap-2 transition hover:shadow-lg hover:border-primary/50"
      >
        <div class="flex items-center gap-2">
          <span class="material-symbols-outlined text-primary"> menu_book </span>
          <span class="font-semibold">阅读文档</span>
        </div>
        <div class="text-sm text-base-content/70">
          查看文档以解决有关 NoneBot 的大部分疑问。
        </div>
      </a>

      <a
        href="https://nonebot.dev/docs/community/contact"
        target="_blank"
        class="p-4 border border-base-content/20 rounded-box flex flex-col gap-2 transition hover:shadow-lg hover:border-primary/50"
      >
        <div class="flex items-center gap-2">
          <span class="material-symbols-outlined text-primary"> forum </span>
          <span class="font-semibold">参与讨论</span>
        </div>
        <div class="text-sm text-base-content/70">
          如在安装、开发或使用过程中遇到了任何问题，欢迎参与社区讨论。
        </div>
      </a>

      <a
        href="https://nonebot.dev/docs/quick-start"
        target="_blank"
        class="p-4 border border-base-content/20 rounded-box flex flex-col gap-2 transition hover:shadow-lg hover:border-primary/50"
      >
        <div class="flex items-center gap-2">
          <span class="material-symbols-outlined text-primary"> rocket_launch </span>
          <span class="font-semibold">快速开始</span>
        </div>
        <div class="text-sm text-base-content/70">
          跟随快速开始指南，几分钟内创建你的第一个机器人。
        </div>
      </a>
    </div>
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
