<script setup lang="ts">
import { ref } from "vue";
import StoreTab from "./StoreTab.vue";
import InstalledTab from "./InstalledTab.vue";
import EmptyState from "@/components/EmptyState.vue";
import { useNoneBotStore } from "@/stores";

const nonebotStore = useNoneBotStore();
const activeTab = ref<"store" | "installed">("store");
</script>

<template>
  <EmptyState
    v-if="!nonebotStore.selectedBot"
    icon="extension"
    message="请先选择一个实例"
    action-label="返回首页选择"
    @action="$router.push('/')"
  />

  <div v-else class="flex flex-col gap-4">
    <!-- 标签页切换 -->
    <div class="tabs tabs-boxed bg-base-200 p-1">
      <a
        :class="{
          'tab flex-1': true,
          'tab-active': activeTab === 'store',
        }"
        @click="activeTab = 'store'"
      >
        <span class="material-symbols-outlined mr-2 text-lg"> storefront </span>
        商店
      </a>
      <a
        :class="{
          'tab flex-1': true,
          'tab-active': activeTab === 'installed',
        }"
        @click="activeTab = 'installed'"
      >
        <span class="material-symbols-outlined mr-2 text-lg"> inventory_2 </span>
        已安装
      </a>
    </div>

    <!-- 标签页内容 -->
    <StoreTab v-if="activeTab === 'store'" />
    <InstalledTab v-else />
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
