import { defineConfig } from "vite";
import reactRefresh from "@vitejs/plugin-react-refresh";
import react from '@vitejs/plugin-react';


// https://vitejs.dev/config/
export default defineConfig({
  build: { manifest: true },
  base: process.env.mode === "production" ? "/static/" : "/",
  root: "./src",
  plugins: [react()],
});