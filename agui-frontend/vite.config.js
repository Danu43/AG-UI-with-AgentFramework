import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  server: {
    fs: {
      allow: [
        // Allow project root
        path.resolve(__dirname),
        // Allow node_modules (needed for CopilotKit / KaTeX)
        path.resolve(__dirname, ".."),
      ],
    },
  },
});