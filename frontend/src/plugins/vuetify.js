import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { md3 } from 'vuetify/blueprints'
import { createVuetify } from 'vuetify'

const lightTheme = {
  dark: false,
  colors: {
    background: '#FCFCFF',
    surface: '#F8F9FC',
    'surface-bright': '#FAF9FF',
    'surface-light': '#D7DAE2',
    'surface-variant': '#DCE3F0',
    'on-surface-variant': '#3C434E',
    primary: '#00447A',
    'primary-darken-1': '#005EA4', 
    secondary: '#344459',
    'secondary-darken-1': '#4D5D73', 
    tertiary: '#681f85',
    'tertiary-darken-1': '#9f56bb',
    error: '#8C0009',
    info: '#2196F3', // Could not find a direct match.
    success: '#4CAF50', // Could not find a direct match.
    warning: '#FB8C00', // Could not find a direct match.
  },
  variables: {
    'border-color': '#585F6B',
    'border-opacity': 0.12,
    'high-emphasis-opacity': 0.87,
    'medium-emphasis-opacity': 0.60,
    'disabled-opacity': 0.38,
    'idle-opacity': 0.04,
    'hover-opacity': 0.04,
    'focus-opacity': 0.12,
    'selected-opacity': 0.08,
    'activated-opacity': 0.12,
    'pressed-opacity': 0.12,
    'dragged-opacity': 0.08,
    'theme-kbd': '#212529',
    'theme-on-kbd': '#FFFFFF',
    'theme-code': '#F5F5F5',
    'theme-on-code': '#000000',
  }
};

const darkTheme = {
  dark: true,
  colors: {
    background: '#101419',
    surface: '#142025',
    'surface-bright': '#363940',
    'surface-light': '#1C2026',
    'surface-variant': '#404752',
    'on-surface-variant': '#C4CBD8',
    primary: '#A9CDFF',
    'primary-darken-1': '#003765', // mapped from onPrimaryFixedVariant
    secondary: '#BCCCE6',
    'secondary-darken-1': '#27374B', // mapped from onSecondaryFixedVariant
    tertiary: '#efb7ff',
    'tertiary-darken-1': '#be72da',
    error: '#FFBAB1',
    info: '#2196F3', // Could not find a direct match.
    success: '#4CAF50', // Could not find a direct match.
    warning: '#FB8C00', // Could not find a direct match.
  },
  variables: {
    'border-color': '#9CA3B0',
    'border-opacity': 0.12,
    'high-emphasis-opacity': 0.87,
    'medium-emphasis-opacity': 0.60,
    'disabled-opacity': 0.38,
    'idle-opacity': 0.04,
    'hover-opacity': 0.04,
    'focus-opacity': 0.12,
    'selected-opacity': 0.08,
    'activated-opacity': 0.12,
    'pressed-opacity': 0.12,
    'dragged-opacity': 0.08,
    'theme-kbd': '#FAFAFF',
    'theme-on-kbd': '#101419',
    'theme-code': '#1C2026',
    'theme-on-code': '#FAFAFF',
  }
};

export default createVuetify({
  blueprint: md3,
  theme: {
    defaultTheme: 'lightTheme',
    themes: {
      lightTheme,
      darkTheme,
    },
  },
})