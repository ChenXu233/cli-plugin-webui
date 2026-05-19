<script setup lang="ts">
import { computed, ref } from "vue";
import SideMenu from "@/components/sidebar/SideMenu.vue";
import InstanceAvatars from "@/components/sidebar/InstanceAvatars.vue";
import OnboardingIndex from "@/components/Modals/InstanceOnboarding/OnboardingIndex.vue";
import router from "@/router";
import { useCustomStore } from "@/stores";

const store = useCustomStore();
const onboardingModal = ref<InstanceType<typeof OnboardingIndex> | null>(null);

const sidebarClasses = computed(() => ({
  "fixed lg:relative top-0 left-0 h-full flex flex-col transition-all overflow-visible": true,
  "bg-base-200 lg:bg-base-200/50 shadow-md": true,
  "lg:!w-20": store.menuMinify,
}));
</script>

<template>
  <OnboardingIndex ref="onboardingModal" />

  <div class="fixed lg:relative z-20 top-0 left-0 flex h-full">
    <Transition>
      <div
        v-show="store.menuShow"
        role="button"
        class="h-screen w-screen bg-gray-500/50 block lg:hidden"
        @click="store.toggleMenuShow()"
      ></div>
    </Transition>

    <div
      :class="sidebarClasses"
      :style="{ transform: store.menuShow ? 'translateX(0)' : 'translateX(-100%)' }"
      class="w-full md:w-1/2 lg:w-72 lg:!transform-none"
    >
      <!-- 顶部 Logo 和收起按钮 -->
      <div class="shrink-0 px-4 pt-2 pb-1">
        <div
          :class="{
            'flex items-center relative': true,
            'justify-between': !store.menuMinify,
            'lg:justify-start lg:gap-5': store.menuMinify,
          }"
        >
          <div
            role="button"
            class="flex items-center gap-2 lg:gap-0.5"
            @click="(router.push('/'), store.toggleMenuShow())"
          >
            <div class="relative flex items-center justify-center">
              <span
                v-if="store.isDebug"
                class="absolute z-10 material-symbols-outlined text-2xl"
              >
                build
              </span>
              <span class="flex-shrink-0 material-symbols-outlined text-primary text-5xl">
                circle
              </span>
            </div>

            <div
              class="shrink-0 text-xl font-semibold leading-7 normal-case"
              :class="{ 'visible lg:hidden': store.menuMinify }"
            >
              NoneBot
            </div>
          </div>

          <div class="flex items-center ml-auto">
            <button
              class="btn btn-sm btn-square btn-ghost flex items-center justify-center lg:hidden"
              @click="store.toggleMenuShow()"
            >
              <span class="material-symbols-outlined text-2xl"> arrow_back_ios_new </span>
            </button>
            <button
              :class="{
                'btn btn-sm btn-square btn-ghost hidden lg:flex items-center justify-center': true,
                '-scale-100': store.menuMinify,
              }"
              @click="store.toggleMenuMinify()"
            >
              <span class="material-symbols-outlined text-2xl"> menu_open </span>
            </button>
          </div>
        </div>
      </div>

      <!-- 中部导航菜单（可滚动） -->
      <div class="flex-1 overflow-y-auto px-4 py-2">
        <SideMenu />
      </div>

      <!-- 底部实例头像列表（固定） -->
      <div class="shrink-0 px-4 pb-2">
        <InstanceAvatars @open-onboarding="onboardingModal?.openModal()" />
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

.v-enter-active,
.v-leave-active {
  transition: opacity 150ms ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
