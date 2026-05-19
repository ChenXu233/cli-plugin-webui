<script setup lang="ts">
import OperationBar from "@/views/Operation/OperationBar.vue";
import BotDetails from "@/views/Operation/BotDetails.vue";
import TerminalItem from "@/views/Operation/TerminalItem.vue";
import EmptyState from "@/components/EmptyState.vue";
import { useNoneBotStore } from "@/stores";

const nonebotStore = useNoneBotStore();
</script>

<template>
  <EmptyState
    v-if="!nonebotStore.selectedBot"
    icon="deployed_code"
    message="请先选择一个实例"
    action-label="返回首页选择"
    @action="$router.push('/')"
  />

  <div v-else class="flex flex-col gap-4">
    <OperationBar />

    <BotDetails />

    <TerminalItem />
  </div>
</template>
