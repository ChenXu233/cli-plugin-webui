<script setup lang="ts">
import { useCustomStore } from "@/stores";
import { useRouter } from "vue-router";
import NotificationItem from "@/components/header/NotificationItem.vue";
import LanguageSwitch from "@/components/header/LanguageSwitch.vue";
import WebUISettings from "@/components/header/WebUISettings.vue";
import { useToastStore } from "@/stores";

const store = useCustomStore();
const toast = useToastStore();
const router = useRouter();

const logout = () => {
  localStorage.clear();
  router.push("/login");
  toast.add("success", "已登出", "", 5000);
};
</script>

<template>
  <div class="relative h-16 px-4 xl:px-8 py-2 flex justify-end items-center bg-base-100">
    <div class="w-full">
      <button
        class="btn btn-sm btn-ghost btn-square lg:hidden"
        @click="store.toggleMenuShow()"
      >
        <span class="material-symbols-outlined"> menu </span>
      </button>
    </div>

    <div class="h-full flex justify-end items-center gap-2">
      <!-- 主题切换 -->
      <button class="btn btn-sm btn-ghost btn-square">
        <label class="swap swap-rotate">
          <input type="checkbox" />

          <span
            class="swap-on fill-current material-symbols-outlined"
            @click="store.toggleTheme('dark')"
          >
            dark_mode
          </span>
          <span
            class="swap-off fill-current material-symbols-outlined"
            @click="store.toggleTheme('light')"
          >
            light_mode
          </span>
        </label>
      </button>

      <!-- 语言切换 -->
      <LanguageSwitch />

      <!-- 通知 -->
      <NotificationItem />

      <!-- WebUI 设置 -->
      <WebUISettings />

      <!-- 登出 -->
      <button class="btn btn-sm btn-ghost btn-square">
        <span class="material-symbols-outlined text-primary" @click="logout()">
          logout
        </span>
      </button>
    </div>
  </div>
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
