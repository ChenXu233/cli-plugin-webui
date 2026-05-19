<script setup lang="ts">
import { useNoneBotStore, useCustomStore } from "@/stores";
import { useRouter } from "vue-router";

const nonebotStore = useNoneBotStore();
const customStore = useCustomStore();
const router = useRouter();

const emit = defineEmits<{
  openOnboarding: [];
}>();

const selectBot = (bot: any) => {
  nonebotStore.selectBot(bot);
  router.push("/operation");
  customStore.toggleMenuShow();
};
</script>

<template>
  <div class="border-t border-base-content/10 pt-2">
    <!-- 有实例时 -->
    <div v-if="nonebotStore.getExtendedBotsList().length">
      <!-- 展开状态：横向排列 -->
      <div
        v-if="!customStore.menuMinify"
        class="flex items-center gap-2 flex-wrap pb-2 pt-8 -mt-8 px-1"
      >
        <div
          v-for="bot in nonebotStore.getExtendedBotsList()"
          :key="bot.project_id"
          class="tooltip tooltip-top"
          :data-tip="bot.project_name"
        >
          <button
            :class="{
              'w-9 h-9 rounded-full flex items-center justify-center transition-all flex-shrink-0': true,
              'bg-primary text-primary-content ring-2 ring-primary ring-offset-1 ring-offset-base-200':
                nonebotStore.selectedBot?.project_id === bot.project_id,
              'bg-base-300 hover:bg-base-content/20':
                nonebotStore.selectedBot?.project_id !== bot.project_id,
            }"
            @click="selectBot(bot)"
          >
            <span class="material-symbols-outlined text-lg"> smart_toy </span>
          </button>
        </div>

        <!-- 新建/导入按钮 -->
        <div class="tooltip tooltip-top" data-tip="新建/导入实例">
          <button
            class="w-9 h-9 rounded-full flex items-center justify-center bg-base-300 hover:bg-base-content/20 transition-all flex-shrink-0"
            @click="emit('openOnboarding')"
          >
            <span class="material-symbols-outlined text-lg"> add </span>
          </button>
        </div>
      </div>

      <!-- 收起状态：纵向排列 -->
      <div v-else class="flex flex-col items-center gap-2 pb-2 pt-2 px-1">
        <div
          class="tooltip tooltip-right"
          :data-tip="nonebotStore.selectedBot?.project_name || '未选择'"
        >
          <button
            class="w-9 h-9 rounded-full flex items-center justify-center bg-primary text-primary-content ring-2 ring-primary ring-offset-1 ring-offset-base-200"
          >
            <span class="material-symbols-outlined text-lg"> smart_toy </span>
          </button>
        </div>

        <div class="tooltip tooltip-right" data-tip="新建/导入实例">
          <button
            class="w-7 h-7 rounded-full flex items-center justify-center bg-base-300 hover:bg-base-content/20 transition-all"
            @click="emit('openOnboarding')"
          >
            <span class="material-symbols-outlined text-sm"> add </span>
          </button>
        </div>
      </div>
    </div>

    <!-- 无实例时 -->
    <div v-else>
      <!-- 展开状态 -->
      <div
        v-if="!customStore.menuMinify"
        class="flex flex-col gap-2 p-3 rounded-lg bg-base-300/50"
      >
        <span class="text-xs opacity-70">🎉 创建你的第一个实例</span>
        <button
          class="btn btn-xs btn-primary text-base-100 w-full"
          @click="emit('openOnboarding')"
        >
          <span class="material-symbols-outlined text-sm"> add </span>
          新建
        </button>
      </div>

      <!-- 收起状态 -->
      <div v-else class="flex justify-center">
        <div class="tooltip tooltip-right" data-tip="新建实例">
          <button
            class="w-7 h-7 rounded-full flex items-center justify-center bg-primary text-primary-content"
            @click="emit('openOnboarding')"
          >
            <span class="material-symbols-outlined text-sm"> add </span>
          </button>
        </div>
      </div>
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
