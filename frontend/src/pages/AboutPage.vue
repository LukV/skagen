<template>
    <v-main>
      <v-container class="py-6" max-width="lg">
        <v-row justify="center">
          <v-col cols="12" class="text-center">
            <h1 style="color: var(--clr-header-text);">Responsive Grid System</h1>
            <p style="color: var(--clr-subtext);">Explore grid layouts and design system components below.</p>
          </v-col>
        </v-row>
        <v-row class="mb-6">
          <v-col cols="12" sm="6" md="4" lg="3">
            <div class="bg-primary text-white pa-4 text-center">1 Column</div>
          </v-col>
          <v-col cols="12" sm="6" md="8" lg="6">
            <div class="bg-primary text-white pa-4 text-center">2 Columns</div>
          </v-col>
          <v-col cols="12" sm="12" md="12" lg="3">
            <div class="bg-primary text-white pa-4 text-center">4 Columns</div>
          </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-col cols="12" class="text-center">
            <h1 style="color: var(--clr-header-text);">Typography</h1>
            <p style="color: var(--clr-subtext);">Headers, paragraphs, bold text, links, bulleted lists, numbered lists </p>
          </v-col>


        <!-- Design System Showcase -->
<!-- Headers in Flexboxes -->
<v-row class="mb-6">
        <v-col cols="12">
          <v-row justify="space-around">
            <v-col cols="auto">
              <h1 style="color: var(--clr-header-text);">H1 Header</h1>
            </v-col>
            <v-col cols="auto">
              <h1 style="color: var(--clr-header-text);">H1 Header</h1>
            </v-col>
            <v-col cols="auto">
              <h1 style="color: var(--clr-header-text);">H1 Header</h1>
            </v-col>
          </v-row>
          <v-row justify="space-between">
            <v-col cols="auto">
              <h2 style="color: var(--clr-header-text);">H2 Header</h2>
            </v-col>
            <v-col cols="auto">
              <h2 style="color: var(--clr-header-text);">H2 Header</h2>
            </v-col>
            <v-col cols="auto">
              <h2 style="color: var(--clr-header-text);">H2 Header</h2>
            </v-col>
          </v-row>
          <v-row justify="center">
            <v-col cols="auto">
              <h3 style="color: var(--clr-header-text);">H3 Header</h3>
            </v-col>
            <v-col cols="auto">
              <h3 style="color: var(--clr-header-text);">H3 Header</h3>
            </v-col>
            <v-col cols="auto">
              <h3 style="color: var(--clr-header-text);">H3 Header</h3>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <!-- Paragraphs with Enhanced Elements -->
      <v-row class="mb-6">
        <v-col cols="12" md="6">
          <p>
            This is a sample paragraph that includes <em>emphasized text</em>, 
            <code>inline code</code>, and a link to 
            <a href="#">another resource</a>.
          </p>
          <p>
            You can also add <span class="text-muted">muted text</span> for less important information. 
            Here is an unordered list:
          </p>
          <ul>
            <li>First item</li>
            <li>Second item</li>
            <li>Third item</li>
          </ul>
        </v-col>
        <v-col cols="12" md="6">
          <p>
            Numbered lists are equally easy to include:
          </p>
          <ol>
            <li>Step one</li>
            <li>Step two</li>
            <li>Step three</li>
          </ol>
          <p>
            Adding longer paragraphs helps demonstrate the layout responsiveness. 
            This is especially useful when testing a grid system. 
            Breakpoints like <code>md</code> or <code>lg</code> allow you to adapt your layout seamlessly.
          </p>
        </v-col>
      </v-row>
  
        <!-- Buttons and Links -->
        <v-row>
          <v-col cols="12">
            <h2>Interactive Elements</h2>
            <v-btn color="primary" class="mr-2">Primary Button</v-btn>
            <v-btn color="secondary" class="mr-2">Secondary Button</v-btn>
            <v-btn color="accent" class="mr-2">Accent Button</v-btn>
            <a href="#" style="color: var(--clr-primary);">This is a link</a>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </template>
  
  <script>
  export default {
    name: 'AboutPage',
  };
  </script>
  
  <style scoped>
  .text-muted {
    color: var(--clr-subtext);
  }
  </style>
  
  