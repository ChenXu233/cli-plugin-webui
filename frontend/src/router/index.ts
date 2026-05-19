import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";
import { defaultRoutes } from "./client";

const routes: RouteRecordRaw[] = [
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/Login/LoginIndex.vue"),
  },
  {
    path: "/",
    name: "WebUI",
    component: () => import("@/views/ViewIndex.vue"),
    children: [
      {
        path: "/",
        name: "Home",
        component: () => import("@/views/Home/HomeIndex.vue"),
      },
    ],
  },
  // 旧路由重定向
  {
    path: "/store",
    redirect: "/extensions",
  },
  {
    path: "/extension",
    redirect: "/extensions",
  },
  {
    path: "/dashboard",
    redirect: "/",
  },
  {
    path: "/:pathMatched(.*)*",
    name: "Not Found",
    props: (route: { params: { pathMatched: string } }) => ({
      pathMatched: `/${route.params.pathMatched}`,
    }),
    component: () => import("@/views/NotFound.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
});

defaultRoutes
  .map((route) => route.routeData)
  .forEach((route) => {
    router.addRoute("WebUI", route);
  });

export default router;
