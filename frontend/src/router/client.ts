interface RouteInfo {
  name: string;
  path: string;
}

export interface RouteRecordRawRebuild extends RouteInfo {
  component: () => Promise<any>;
}

export interface NavItem {
  googleIcon?: string;
  name: string;
  routeData: RouteRecordRawRebuild;
}

// 实例范围菜单项（有实例时显示）
export const instanceRoutes: NavItem[] = [
  {
    googleIcon: "settings_applications",
    name: "操作",
    routeData: {
      path: "/operation",
      name: "Operation",
      component: () => import("@/views/Operation/OperationIndex.vue"),
    },
  },
  {
    googleIcon: "settings",
    name: "设置",
    routeData: {
      path: "/settings",
      name: "Settings",
      component: () => import("@/views/Settings/SettingsIndex.vue"),
    },
  },
  {
    googleIcon: "extension",
    name: "拓展",
    routeData: {
      path: "/extensions",
      name: "Extensions",
      component: () => import("@/views/Extensions/ExtensionsIndex.vue"),
    },
  },
];

// 首页菜单项（无实例时显示）
export const homeRoutes: NavItem[] = [
  {
    googleIcon: "home",
    name: "首页",
    routeData: {
      path: "/",
      name: "Home",
      component: () => import("@/views/Home/HomeIndex.vue"),
    },
  },
];

// 兼容：所有路由的扁平列表
export const defaultRoutes: NavItem[] = [...homeRoutes, ...instanceRoutes];
