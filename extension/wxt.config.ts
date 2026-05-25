import { defineConfig } from "wxt";
import react from "@vitejs/plugin-react";

export default defineConfig({
  srcDir: "src",
  manifest: {
    name: "Chrome Wrapped",
    description: "Transform your browsing history into beautiful insights",
    version: "0.1.0",
    permissions: ["history", "storage"],
    host_permissions: ["http://localhost:8000/*", "http://127.0.0.1:8000/*"],
  },
  vite: () => ({
    plugins: [react()],
  }),
});
