<template>
    <div class="min-h-screen flex flex-col relative">
      <!-- Header -->
      <Header
        :sidebar-collapsed="sidebarCollapsed"
        :unread-notifications="unreadNotifications"
        @toggle-sidebar="handleSidebarToggle"
        @show-notifications="handleNotifications"
      />
      
      <div class="flex flex-1 flex-col md:flex-row">
        <!-- Sidebar -->
        <Sidebar
          :is-open="!sidebarCollapsed"
          :is-mobile="isMobile"
          @close-sidebar="handleSidebarToggle(true)"
        />
        
        <!-- Main content area (Body) -->
        <Body
          :is-sidebar-collapsed="sidebarCollapsed"
          :is-mobile="isMobile"
        />
        
        <!-- Backdrop for mobile sidebar -->
        <div
          v-if="isMobile && !sidebarCollapsed"
          class="fixed inset-0 bg-black/50 z-40 md:hidden"
          @click="handleSidebarToggle(true)"
        ></div>
      </div>
    </div>
  </template>
  
  <script>
  import Header from '../components/private/Header.vue';
  import Sidebar from '../components/private/Sidebar.vue';
  import Body from '../components/private/Body.vue';
  
  export default {
    name: 'DefaultLayout',
    components: {
      Header,
      Sidebar,
      Body,
    },
    data() {
      return {
        sidebarCollapsed: window.innerWidth < 768,
        isMobile: window.innerWidth < 768,
        unreadNotifications: 3, // Example value for notifications
      };
    },
    methods: {
      handleSidebarToggle(isCollapsed) {
        this.sidebarCollapsed = isCollapsed;
      },
      handleNotifications() {
        // Handle notification logic here
        console.log('Notifications clicked');
      },
      checkMobile() {
        this.isMobile = window.innerWidth < 768;
        // Collapse sidebar on mobile by default
        if (this.isMobile) {
          this.sidebarCollapsed = true;
        } else {
          this.sidebarCollapsed = false; // Expand on desktop
        }
      },
    },
    mounted() {
      window.addEventListener('resize', this.checkMobile);
    },
    beforeDestroy() {
      window.removeEventListener('resize', this.checkMobile);
    },
  };
  </script>
  
  <style scoped>
  /* Ensure smooth transitions for the layout */
  .transition-all {
    transition: all 0.3s ease-in-out;
  }
  </style>