<script setup lang="ts">
import { ref, computed } from "vue";
import ModeSelect from "./ModeSelect.vue";
import TemplateSelect from "./steps/create/TemplateSelect.vue";
import BotBasic from "./steps/create/BotBasic.vue";
import DriverSelect from "./steps/create/DriverSelect.vue";
import AdapterSelect from "./steps/create/AdapterSelect.vue";
import ScanProject from "./steps/import/ScanProject.vue";
import MirrorSelect from "./steps/shared/MirrorSelect.vue";
import InstallAndFinish from "./steps/shared/InstallAndFinish.vue";
import { useOnboardingStore } from "./index";

const store = useOnboardingStore();

const modalRef = ref<HTMLDialogElement>();

defineExpose({
  openModal: () => {
    store.reset();
    modalRef.value?.showModal();
  },
  closeModal: () => modalRef.value?.close(),
});

const createStepComponents = [
  TemplateSelect,
  BotBasic,
  MirrorSelect,
  DriverSelect,
  AdapterSelect,
  InstallAndFinish,
];

const importStepComponents = [ScanProject, MirrorSelect, InstallAndFinish];

const currentComponent = computed(() => {
  if (!store.mode) return ModeSelect;

  const stepIndex = store.step - 1;
  if (store.mode === "create") return createStepComponents[stepIndex];
  if (store.mode === "import") return importStepComponents[stepIndex];
  return ModeSelect;
});

const stepTitle = computed(() => {
  if (!store.mode) return "选择操作";
  if (store.mode === "create") return "创建 NoneBot 实例";
  return "导入 NoneBot 实例";
});
</script>

<template>
  <dialog ref="modalRef" class="modal" @close="store.reset()">
    <div
      class="overflow-hidden modal-box w-11/12 max-w-5xl rounded-xl flex flex-col gap-4"
    >
      <h3 class="font-semibold text-lg">{{ stepTitle }}</h3>

      <div v-if="store.mode" class="w-full flex justify-center">
        <ul class="steps w-full xl:w-3/4 gap-4">
          <li
            v-for="(s, index) in store.steps"
            :key="s.title"
            :role="
              s.pass() && !store.isInstalling && !store.isSuccess ? 'button' : undefined
            "
            :data-content="index < store.step - 1 ? '✓' : index + 1"
            :class="{
              step: true,
              'step-primary': index <= store.step - 1,
            }"
            @click="
              s.pass() && !store.isInstalling && !store.isSuccess
                ? (store.step = index + 1)
                : null
            "
          >
            <div :class="{ 'opacity-20': index < store.step - 1 }">{{ s.title }}</div>
          </li>
        </ul>
      </div>

      <div v-show="store.warningMessage" class="flex justify-center">
        <div role="alert" class="alert alert-warning w-full max-w-xs">
          <span class="material-symbols-outlined"> warning </span>
          {{ store.warningMessage }}
        </div>
      </div>

      <div class="overflow-auto h-full w-full">
        <component :is="currentComponent" />
      </div>
    </div>
  </dialog>
</template>

<style scoped>
.steps .step-primary + .step-primary:before,
.steps .step-primary:after {
  @apply !text-base-100;
}
</style>
