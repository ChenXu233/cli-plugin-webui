import type { Adapter, Driver } from "@/client/api";
import { defineStore } from "pinia";
import { ref, computed } from "vue";

export type OnboardingMode = "create" | "import";

export const useOnboardingStore = defineStore("onboardingStore", () => {
  // === 共享状态 ===
  const step = ref(0);
  const warningMessage = ref("");
  const mode = ref<OnboardingMode | null>(null);
  const projectName = ref("");
  const projectPath = ref("");
  const pythonMirror = ref("");
  const adapters = ref<Adapter[]>([]);
  const isInstalling = ref(false);
  const isSuccess = ref(false);

  // === Create 专用 ===
  const template = ref<"bootstrap" | "simple" | "">("");
  const useSrc = ref(false);
  const drivers = ref<Driver[]>([]);

  // === Import 专用 ===
  const searchSuccess = ref(false);
  const plugins = ref<string[]>([]);
  const pluginDirs = ref<string[]>([]);

  // === 计算属性 ===
  const isCreateMode = computed(() => mode.value === "create");
  const isImportMode = computed(() => mode.value === "import");

  // === 步骤定义 ===
  const createSteps = [
    { title: "模板选择", pass: () => true },
    {
      title: "基础信息",
      pass: () => projectName.value !== "" && projectPath.value !== "",
    },
    { title: "镜像选择", pass: () => pythonMirror.value !== "" },
    { title: "驱动器选择", pass: () => drivers.value.length > 0 },
    { title: "适配器选择", pass: () => adapters.value.length > 0 },
    { title: "安装依赖", pass: () => false },
  ];

  const importSteps = [
    { title: "信息获取", pass: () => true },
    { title: "镜像选择", pass: () => searchSuccess.value },
    { title: "确认&安装依赖", pass: () => pythonMirror.value !== "" },
  ];

  const steps = computed(() => {
    if (mode.value === "create") return createSteps;
    if (mode.value === "import") return importSteps;
    return [];
  });

  // === 方法 ===
  const reset = () => {
    step.value = 0;
    warningMessage.value = "";
    mode.value = null;
    projectName.value = "";
    projectPath.value = "";
    pythonMirror.value = "";
    adapters.value = [];
    isInstalling.value = false;
    isSuccess.value = false;
    template.value = "";
    useSrc.value = false;
    drivers.value = [];
    searchSuccess.value = false;
    plugins.value = [];
    pluginDirs.value = [];
  };

  return {
    // 共享
    step,
    warningMessage,
    mode,
    projectName,
    projectPath,
    pythonMirror,
    adapters,
    isInstalling,
    isSuccess,
    // Create
    template,
    useSrc,
    drivers,
    // Import
    searchSuccess,
    plugins,
    pluginDirs,
    // 计算
    isCreateMode,
    isImportMode,
    steps,
    // 方法
    reset,
  };
});
