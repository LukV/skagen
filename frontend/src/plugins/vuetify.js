import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'

export default createVuetify({
  defaults: {
    VBtn: {
      style: 'text-transform: none;',
    },
  },
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#4b26d0',       // Main purple
          secondary: '#2668c8',     // Complementary green
          accent: '#c02694',        // Button highlight
          background: '#fafafa',    // Background
          surface: '#ffffff',       // Cards and modals
          textPrimary: '#1a1a1a',   // Headers
          textSecondary: '#383838', // Body text
          textMuted: '#757575',     // Subtext
        },
      },
    },
  },
  typography: {
    defaultFontFamily: 'Inter, sans-serif',
  },
});
