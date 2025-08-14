import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    outDir: '../static/dist',
    manifest: true,
    rollupOptions: {
      input: {
        main: './src/js/main.js',
      },
    },
  },
})