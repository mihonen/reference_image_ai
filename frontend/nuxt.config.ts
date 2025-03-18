// https://nuxt.com/docs/api/configuration/nuxt-config

import tailwindcss from "@tailwindcss/vite";


export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },

  modules: ['@nuxt/icon', '@nuxt/image', '@nuxt/ui'],

  vite: {
    plugins: [
      tailwindcss(),
    ],
  },

  components: [
    {
      path: '~/components',
      pathPrefix: false, // [!code ++]
    },
  ],

  css: [
    '@/assets/css/main.css',
  ],

  fontMetrics: {
    fonts: ['DM Sans']
  },
  googleFonts: {
    display: 'swap',
    download: true,
    families: {
      'DM+Sans': [400, 500, 600, 700]
    }
  },
  ui: {
    icons: ['heroicons', 'simple-icons'],
    stragedy: 'override',
    carousel: {
      default: {
        prevButton: {
          color: 'white',
          class: 'bg-black'
        }
      },
      indicators: {
        active: 'bg-white'
      }
    }

  },


})