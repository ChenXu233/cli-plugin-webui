<script setup lang="ts">
import { useOnboardingStore } from "./index";

const store = useOnboardingStore();

const selectMode = (mode: "create" | "import") => {
  store.mode = mode;
  store.step = 1;
};
</script>

<template>
  <div class="flex flex-col items-center gap-8">
    <div class="text-center text-lg font-semibold">请选择操作</div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-lg">
      <button
        class="btn btn-outline btn-primary h-auto py-8 flex flex-col gap-2"
        @click="selectMode('create')"
      >
        <span class="material-symbols-outlined text-4xl"> add_circle </span>
        <span class="text-base font-semibold">新建实例</span>
        <span class="text-xs opacity-70">从零开始创建一个新的 NoneBot 实例</span>
      </button>

      <button
        class="btn btn-outline btn-primary h-auto py-8 flex flex-col gap-2"
        @click="selectMode('import')"
      >
        <span class="material-symbols-outlined text-4xl"> folder_open </span>
        <span class="text-base font-semibold">导入已有项目</span>
        <span class="text-xs opacity-70">导入一个已存在的 NoneBot 项目</span>
      </button>
    </div>

    <div class="w-full flex justify-end">
      <form method="dialog">
        <button class="btn btn-sm">取消</button>
      </form>
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
