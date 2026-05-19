<script setup lang="ts">
import { computed, ref } from "vue";
import { useNoneBotStore } from "@/stores";
import OnboardingHero from "./OnboardingHero.vue";
import OnboardingIndex from "@/components/Modals/InstanceOnboarding/OnboardingIndex.vue";

const nonebotStore = useNoneBotStore();
const onboardingModal = ref<InstanceType<typeof OnboardingIndex> | null>(null);

const hasBots = computed(() => nonebotStore.getExtendedBotsList().length > 0);
const getBotIsRunning = computed(() => {
  return nonebotStore.getExtendedBotsList().filter((bot) => bot.is_running).length;
});
</script>

<template>
  <OnboardingIndex ref="onboardingModal" />

  <!-- 无实例时：显示引导英雄区 -->
  <OnboardingHero v-if="!hasBots" @open-onboarding="onboardingModal?.openModal()" />

  <!-- 有实例时：显示仪表盘 -->
  <div v-else class="grid gap-4">
    <!-- 欢迎区域和统计 -->
    <div class="grid gap-4 grid-cols-1 xl:grid-cols-3">
      <div
        class="col-span-1 xl:col-span-2 card bg-primary/[.2] card-body justify-center gap-4"
      >
        <h2 class="card-title">欢迎 👋</h2>
        <div class="text-sm">
          <p>这是 NoneBot CLI 图形化控制端</p>
          <p>创建并同时管理多个 NoneBot 实例</p>
        </div>
        <div class="card-actions justify-start">
          <button
            class="btn btn-primary btn-sm font-normal text-base-100"
            @click="onboardingModal?.openModal()"
          >
            新建实例
          </button>
        </div>
      </div>

      <div class="grid gap-4 grid-cols-2 xl:grid-cols-none">
        <div class="stats stats-vertical lg:stats-horizontal">
          <div class="stat">
            <div class="stat-title">已有实例</div>
            <div class="stat-value">{{ nonebotStore.getExtendedBotsList().length }}</div>
          </div>

          <div class="stat">
            <div class="stat-title">正在运行</div>
            <div class="stat-value">{{ getBotIsRunning }}</div>
          </div>
        </div>

        <div class="card bg-base-200">
          <div class="card-body items-center">
            <p>实例操作</p>
            <div class="card-actions justify-center gap-4">
              <button
                class="btn btn-sm btn-primary font-normal text-base-100"
                @click="onboardingModal?.openModal()"
              >
                新建实例
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 实例列表 -->
    <div class="p-4 rounded-box bg-base-200">
      <div class="overflow-x-auto">
        <table class="table">
          <thead>
            <tr>
              <th>实例名称</th>
              <th>适配器</th>
              <th>状态</th>
            </tr>
          </thead>

          <tbody>
            <tr
              role="button"
              v-for="bot in nonebotStore.getExtendedBotsList()"
              :key="bot.project_id"
              class="hover:bg-base-300 transition-colors"
              @click="nonebotStore.selectBot(bot)"
            >
              <td>
                {{ bot.project_name }}
                <span
                  v-if="nonebotStore.selectedBot?.project_id === bot.project_id"
                  class="ml-2 badge badge-outline text-base-content"
                >
                  选择中
                </span>
              </td>
              <td class="flex flex-wrap gap-2">
                <span v-for="(adapter, index) in bot.adapters" :key="index" class="badge">
                  {{ adapter.name }}
                </span>
              </td>
              <td>
                <span
                  :class="{
                    'badge badge-sm': true,
                    'badge-success': bot.is_running,
                    'badge-ghost': !bot.is_running,
                  }"
                >
                  {{ bot.is_running ? "运行中" : "已停止" }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
