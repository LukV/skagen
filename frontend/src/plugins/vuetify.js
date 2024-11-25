// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Vuetify
import { createVuetify } from 'vuetify'

export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#4b26d0',       // Main purple
          secondary: '#abd026',     // Complementary green
          accent: '#f88d6e',        // Button highlight
          background: '#efe7fb',    // Background
          surface: '#ffffff',       // Cards and modals
          textPrimary: '#212121',   // Headers
          textSecondary: '#424242', // Body text
          textMuted: '#757575',     // Subtext
        },
      },
    },
  },
  typography: {
    defaultFontFamily: 'Inter',
  },
});
