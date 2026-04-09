// @ts-check
import { defineConfig } from "@vivliostyle/cli";

export default defineConfig({
  title: "幻协生存指南",
  author: "探索不了一点宇宙编辑部",
  language: "zh",
  browser: "chrome@143.0.7499.42",
  image: "ghcr.io/vivliostyle/cli:10.3.0",
  theme: ["./theme/custom.css"],
  size: "185mm,260mm",

  cover: { src: "./draft/cover.png" },

  toc: {
    title: "目录",
  },

  entry: [
    {
      rel: "cover",
      path: "./draft/front-cover.html",
      output: "front-cover.html",
      theme: "./theme/cover.css",
    },
    {
      rel: "contents",
      path: "./draft/toc.html",
      output: "toc.html",
      theme: ["./theme/toc.css"],
    },
    "./draft/posts/前言.md",
    "./draft/posts/如何管理社团.md",
    "./draft/posts/如何管理小社团.md",
    "./draft/posts/如何做外联.md",
    "./draft/posts/如何出摊.md",
    "./draft/posts/如何开展观影活动.md",
    "./draft/posts/如何举办主题影展.md",
    "./draft/posts/如何开展征文活动.md",
    "./draft/posts/如何做会刊.md",
    {
      rel: "cover",
      path: "./draft/back-cover.html",
      output: "back-cover.html",
      theme: "./theme/cover.css",
    },
  ],
});
