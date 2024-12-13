<template>
  <div class="app-container">
    <!-- Sidebar -->
    <transition name="slide-sidebar">
      <AppSidebar
        v-if="!isMobile || sidebarOpen"
        class="app-sidebar"
        :collapsed="isCollapsed"
        :is-logged-in="isLoggedIn"
        :user-name="userName"
        @toggle-collapse="toggleSidebar"
        @sign-up="onSignUp"
        @login="onLogin"
        @logout="onLogout"
        @toggle-user-overlay="toggleUserOverlay"
      />
    </transition>

    <!-- Mobile Menu Overlay -->
    <transition name="fade">
      <div v-if="isMobile && sidebarOpen" class="mobile-overlay">
        <div class="mobile-overlay-header">
          <BaseButton variant="text" @click="sidebarOpen = false">
            <svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 6L18 18M6 18L18 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            </svg>
          </BaseButton>
        </div>

        <div class="mobile-overlay-content">
          <!-- Overlay menu items go here -->
          <div class="mobile-auth">
            <AuthStatus
              :collapsed="false"
              :is-logged-in="isLoggedIn"
              :user-name="userName"
              @sign-up="onSignUp"
              @login="onLogin"
              @logout="onLogout"
              @toggle-user-overlay="toggleUserOverlay"
            />
          </div>
        </div>
      </div>
    </transition>

    <div class="right-col">
      <AppHeader @toggle-sidebar="toggleSidebarOpen" />
      <main class="main-content">
        <router-view />
      </main>
    </div>

    <!-- User overlay (e.g., dropdown or modal) -->
    <div v-if="userOverlayOpen" class="user-overlay" @click.self="toggleUserOverlay(false)">
      <div class="user-overlay-content">
        <!-- Future user overlay content -->
        <p>User: {{ userName }}</p>
        <button @click="toggleUserOverlay(false)">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onBeforeUnmount } from 'vue';
import AppHeader from './components/layout/AppHeader.vue';
import AppSidebar from './components/layout/AppSidebar.vue';
import AuthStatus from './components/shared/AuthStatus.vue';
import BaseButton from './components/base/BaseButton.vue';

export default {
  name: 'App',
  components: { AppHeader, AppSidebar, AuthStatus, BaseButton },
  setup() {
    const sidebarOpen = ref(false);
    const isCollapsed = ref(false);
    const isLoggedIn = ref(false);
    const userName = ref(null);
    const userOverlayOpen = ref(false);

    const isMobile = ref(window.innerWidth <= 600);
    const handleResize = () => {
      isMobile.value = window.innerWidth <= 600;
      if (!isMobile.value) {
        sidebarOpen.value = false;
      }
    };
    window.addEventListener('resize', handleResize);
    onBeforeUnmount(() => {
      window.removeEventListener('resize', handleResize);
    });

    const toggleSidebar = () => {
      isCollapsed.value = !isCollapsed.value;
    };

    const toggleSidebarOpen = () => {
      sidebarOpen.value = !sidebarOpen.value;
    };

    const onSignUp = () => {
      isLoggedIn.value = true;
      userName.value = "John Doe";
    };

    const onLogin = () => {
      isLoggedIn.value = true;
      userName.value = "John Doe";
    };

    const onLogout = () => {
      isLoggedIn.value = false;
      userName.value = null;
    };

    const toggleUserOverlay = (force) => {
      if (typeof force === 'boolean') {
        userOverlayOpen.value = force;
      } else {
        userOverlayOpen.value = !userOverlayOpen.value;
      }
    };

    return {
      sidebarOpen,
      isCollapsed,
      isMobile,
      isLoggedIn,
      userName,
      userOverlayOpen,
      toggleSidebar,
      toggleSidebarOpen,
      onSignUp,
      onLogin,
      onLogout,
      toggleUserOverlay,
    };
  },
};
</script>

<style scoped>
.app-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  position: relative;
}

/* Mobile Overlay */
.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  background-color: var(--color-background-darker, #fff);
}

.mobile-overlay-header {
  display: flex;
  justify-content: right;
  padding: var(--spacing-md);
  position: relative;
  background-color: var(--color-background, #fff);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.mobile-overlay-close {
  position: absolute;
  right: var(--spacing-md);
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-sm);
}

.mobile-overlay-content {
  flex: 1;
  padding: var(--spacing-md);
}

/* Auth section in mobile overlay */
.mobile-auth {
  margin-top: auto; /* Push to the bottom */
  padding: var(--spacing-lg);
}

/* Example styling for user overlay */
.user-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.user-overlay-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
}

.app-sidebar {
  flex: 0 0 auto;
  transition: width 0.3s ease;
  width: 200px;
}

.app-sidebar.collapsed {
  width: 50px;
}

.right-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-md);
}

/* Overlay for mobile */
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
}

/* On mobile hide sidebar by default */
@media (max-width: 600px) {
  .app-sidebar {
    display: none;
  }

  /* When sidebarOpen is true, slide it in */
  .app-sidebar.slide-sidebar-enter-from,
  .app-sidebar.slide-sidebar-leave-to {
    transform: translateX(-100%);
  }
  .app-sidebar.slide-sidebar-enter-to,
  .app-sidebar.slide-sidebar-leave-from {
    transform: translateX(0);
  }
}

/* On desktop, no transform needed. Just collapse/expand width. */
</style>