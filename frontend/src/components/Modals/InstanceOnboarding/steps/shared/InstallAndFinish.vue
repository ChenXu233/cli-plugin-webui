<script setup lang="ts">
import { ProjectService, type ProcessLog } from "@/client/api";
import { useWebSocket } from "@vueuse/core";
import { computed, onUnmounted, ref, watch } from "vue";
import { generateURLForWebUI } from "@/client/utils";
import { useOnboardingStore } from "../../index";
import { useNoneBotStore, useToastStore } from "@/stores";

const IS_FINISHED = "✨ Done!";
const IS_FAILED = "❌ Failed!";

const store = useOnboardingStore();
const toast = useToastStore();
const nonebotStore = useNoneBotStore();

const logKey = ref("");
const isFailed = ref(false);
const logContainer = ref<HTMLElement>();
const logData = ref<ProcessLog[]>([]);

const startInstall = async () => {
  if (isFailed.value) {
    isFailed.value = false;
    store.warningMessage = "";
    logData.value = [{ message: "Retrying..." }];
  }

  if (store.isCreateMode) {
    const { data, error } = await ProjectService.createProjectV1ProjectCreatePost({
      body: {
        is_bootstrap: store.template === "bootstrap",
        use_src: store.useSrc,
        project_name: store.projectName,
        project_dir: store.projectPath,
        mirror_url: store.pythonMirror,
        drivers: store.drivers,
        adapters: store.adapters,
      },
    });

    if (error) {
      store.warningMessage = error.detail?.toString() ?? "";
      isFailed.value = true;
    }

    if (data) {
      logKey.value = data.detail;
      open();
    }
  } else if (store.isImportMode) {
    const { data, error } = await ProjectService.addProjectV1ProjectAddPost({
      body: {
        project_name: store.projectName,
        project_dir: store.projectPath,
        mirror_url: store.pythonMirror,
        adapters: store.adapters.map((obj) => obj.module_name) ?? [],
        plugins: store.plugins,
        plugin_dirs: store.pluginDirs,
      },
    });

    if (error) {
      store.warningMessage = error.detail?.toString() ?? "";
      isFailed.value = true;
    }

    if (data) {
      logKey.value = data.detail;
      open();
    }
  }
};

const finish = async () => {
  await nonebotStore.loadBots();
  const action = store.isCreateMode ? "创建" : "添加";
  toast.add("success", `${action}实例 ${store.projectName} 成功`, "", 5000);
};

const { status, data, close, open } = useWebSocket<ProcessLog>(
  generateURLForWebUI("/v1/process/log/ws", true),
  {
    immediate: false,
    autoReconnect: {
      retries: 10,
      delay: 3000,
    },
    onConnected(ws) {
      const token = localStorage.getItem("token") ?? "";
      ws.send(token);
      ws.send(JSON.stringify({ type: "log", log_key: logKey.value }));
    },
  },
);

watch(
  () => data.value,
  (rawData) => {
    if (!rawData) return;

    const parsed: ProcessLog = JSON.parse(rawData.toString());
    logData.value.push(parsed);

    if (parsed.message === IS_FINISHED) {
      close();
      store.isSuccess = true;
    } else if (parsed.message === IS_FAILED) {
      close();
      isFailed.value = true;
    }
  },
);

watch(
  () => status.value,
  (s) => {
    store.isInstalling = s === "OPEN";
  },
);

const getLogData = computed(() => [...logData.value].reverse());

onUnmounted(() => {
  close();
});
</script>

<template>
  <div class="overflow-hidden flex flex-col gap-4">
    <div class="overflow-auto bg-base-200 rounded-lg p-4">
      <!-- 安装前：显示配置摘要 -->
      <table v-if="!logKey" class="table table-sm w-full">
        <tbody>
          <tr>
            <th class="font-semibold text-base">实例名称</th>
            <td>{{ store.projectName }}</td>
          </tr>
          <tr v-if="store.isCreateMode">
            <th class="font-semibold text-base">实例类型</th>
            <td>{{ store.template === "bootstrap" ? "初学者 / 普通用户" : "开发者" }}</td>
          </tr>
          <tr v-if="store.isCreateMode && store.template === 'simple'">
            <th class="font-semibold text-base">实例插件加载位置</th>
            <td>{{ store.useSrc ? "/src" : `/${store.projectName}` }}</td>
          </tr>
          <tr>
            <th class="font-semibold text-base">实例路径</th>
            <td>
              {{
                store.isCreateMode ? `(Base Dir)/${store.projectPath}` : store.projectPath
              }}
            </td>
          </tr>
          <tr>
            <th class="font-semibold text-base">Python 镜像</th>
            <td>{{ store.pythonMirror }}</td>
          </tr>
          <tr v-if="store.isCreateMode">
            <th class="font-semibold text-base">驱动器</th>
            <td class="flex flex-wrap items-center gap-2">
              <span v-for="driver in store.drivers" class="badge" :key="driver.name">
                {{ driver.name }}
              </span>
            </td>
          </tr>
          <tr>
            <th class="font-semibold text-base">适配器</th>
            <td class="flex flex-wrap items-center gap-2">
              <span v-for="adapter in store.adapters" :key="adapter.name" class="badge">
                {{ adapter.name }}
              </span>
              <span v-if="!store.adapters.length" class="text-base-content/50">
                {{ store.isImportMode ? "未找到适配器" : "未选择" }}
              </span>
            </td>
          </tr>
          <tr v-if="store.isImportMode">
            <th class="font-semibold text-base">插件</th>
            <td class="flex flex-wrap items-center gap-2">
              <span v-for="plugin in store.plugins" :key="plugin" class="badge">
                {{ plugin }}
              </span>
              <span v-if="!store.plugins.length" class="text-base-content/50"
                >未找到插件</span
              >
            </td>
          </tr>
          <tr v-if="store.isImportMode">
            <th class="font-semibold text-base">插件目录</th>
            <td class="flex flex-wrap items-center gap-2">
              <span v-for="dir in store.pluginDirs" :key="dir" class="badge">
                {{ dir }}
              </span>
              <span v-if="!store.pluginDirs.length" class="text-base-content/50"
                >未找到插件目录</span
              >
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 安装中：显示日志 -->
      <table v-else class="overflow-auto h-80 !flex table table-xs">
        <tbody ref="logContainer">
          <tr
            v-for="(item, index) in getLogData"
            :key="index"
            :class="{
              'flex font-mono': true,
              'bg-error/50': item.level === 'ERROR',
              'bg-warning/50': item.level === 'WARNING',
            }"
          >
            <th class="sticky left-0 right-0 bg-base-200 text-gray-500">
              {{ item.time }}
            </th>
            <td class="flex">{{ item.level }}</td>
            <td class="flex whitespace-pre-wrap">{{ item.message }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="flex items-center justify-between">
      <button
        :class="{
          'btn btn-sm btn-primary text-base-100': true,
          'btn-disabled': store.isInstalling || store.isSuccess,
        }"
        @click="store.step--"
      >
        上一步
      </button>

      <div class="flex items-center gap-2">
        <form method="dialog">
          <button
            :class="{
              'btn btn-sm': true,
              'btn-disabled': store.isInstalling || store.isSuccess,
            }"
          >
            取消
          </button>
        </form>

        <form v-if="store.isSuccess" method="dialog">
          <button class="btn btn-sm btn-primary text-base-100" @click="finish()">
            完成
          </button>
        </form>
        <button
          v-else
          :class="{
            'btn btn-sm btn-primary text-base-100': true,
            'btn-disabled': store.isInstalling,
          }"
          @click="startInstall()"
        >
          {{ isFailed ? "重试" : "安装" }}
        </button>
      </div>
    </div>
  </div>
</template>
