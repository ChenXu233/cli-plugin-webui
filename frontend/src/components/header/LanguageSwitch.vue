<script setup lang="ts">
import { ref } from "vue";
import DrawerItem from "@/components/DrawerItem.vue";

interface LanguageItem {
  code: string;
  name: string;
}

const languages: LanguageItem[] = [
  { code: "zh-CN", name: "中文" },
  { code: "en", name: "English" },
];

const currentLang = ref(localStorage.getItem("language") || "zh-CN");
const drawerRef = ref<InstanceType<typeof DrawerItem> | null>(null);

const switchLang = (lang: LanguageItem) => {
  currentLang.value = lang.code;
  localStorage.setItem("language", lang.code);
  drawerRef.value?.closeDrawer();
  // TODO: 实际切换语言的逻辑
};
</script>

<template>
  <DrawerItem ref="drawerRef">
    <template v-slot:button>
      <button class="btn btn-sm btn-ghost btn-square" @click="drawerRef?.showDrawer()">
        <span class="material-symbols-outlined"> language </span>
      </button>
    </template>

    <template v-slot:drawer-title>语言设置</template>

    <template v-slot:drawer-body>
      <div class="flex flex-col gap-2">
        <button
          v-for="lang in languages"
          :key="lang.code"
          :class="{
            'btn btn-ghost justify-start font-normal': true,
            'btn-active': currentLang === lang.code,
          }"
          @click="switchLang(lang)"
        >
          <span
            v-if="currentLang === lang.code"
            class="material-symbols-outlined text-primary"
          >
            check
          </span>
          {{ lang.name }}
        </button>
      </div>
    </template>
  </DrawerItem>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    "FILL" 0,
    "wght" 400,
    "GRAD" -25,
    "opsz" 48;
}
</style>
