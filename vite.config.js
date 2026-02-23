import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  base: "/codespaces-react/",
  plugins: [react()],
  server: {
    proxy: {
      '/analyze': 'http://localhost:5000'
    }
  },
  test: {
    globals: true,
    environment: 'jsdom',
  },
})
