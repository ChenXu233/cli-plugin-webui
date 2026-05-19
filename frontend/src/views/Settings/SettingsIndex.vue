<script setup lang="ts">
import SettingCard from "./SettingCard.vue";
import SearchBar from "./SearchBar.vue";
import { useSettingsStore } from "./client";
import EmptyState from "@/components/EmptyState.vue";
import { useNoneBotStore } from "@/stores";

const nonebotStore = useNoneBotStore();
const settingsStore = useSettingsStore();

if (nonebotStore.selectedBot) {
  settingsStore.init();
}
</script>

<template>
  <EmptyState
    v-if="!nonebotStore.selectedBot"
    icon="settings"
    message="请先选择一个实例"
    action-label="返回首页选择"
    @action="$router.push('/')"
  />

  <div v-else class="flex flex-col gap-6">
    <SearchBar />

    <div v-if="settingsStore.viewData.length" class="flex flex-col items-center gap-4">
      <div v-for="i in settingsStore.viewData" :key="i.title" class="w-full">
        <SettingCard :data="i" />
      </div>
      <span class="badge">共 {{ settingsStore.viewData.length }} 项</span>
    </div>
    <div v-else class="text-center">没有结果。</div>
  </div>
</template>
