<template>
  <aside
    class="fixed top-0 left-0 h-screen bg-black text-white flex flex-col shadow-xl transition-all duration-300 z-50 "
    :class="{
      'w-72': isOpen,
      'w-0 overflow-hidden': !isOpen,
      'md:w-72': !isMobile,
    }" role="navigation" aria-label="Charity Donation Sidebar">
    <!-- Logo Section with Status Indicator -->
    <div class="p-5 " v-if="isOpen || !isMobile">
      <div class="flex items-center space-x-3">
        <div class="relative">
          <div
            class="w-10 h-10 rounded-lg bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center shadow-lg">
            <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </div>
          <span class="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-gray-900"></span>
        </div>
        <div>
          <h1 class="text-xl font-bold bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent">
            Hope Foundation</h1>
          <p class="text-xs text-gray-400">Changing Lives Together</p>
        </div>
      </div>
    </div>

    <!-- Navigation Menu -->
    <nav class="flex-1 overflow-y-auto py-3" v-if="isOpen || !isMobile">
      <ul class="space-y-1 px-3">
        <li v-for="(link, index) in links.main" :key="index">
          <router-link :to="link.path"
            class="flex items-center p-3 rounded-lg hover:bg-gray-800/50 transition-all group"
            :class="{ 'bg-yellow-900/30 border-l-4 border-yellow-400': activeLink === link.path }"
            @click="closeSidebar">
            <div class="relative">
              <svg class="w-5 h-5 mr-3 text-gray-400 group-hover:text-yellow-300" fill="none" stroke="currentColor"
                viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="link.icon" />
              </svg>
            </div>
            <span class="text-gray-300 group-hover:text-white">{{ link.name }}</span>
          </router-link>
        </li>

        <!-- Donor Section -->
        <li class="mt-4" v-if="userRole === 'donor'">
          <p class="text-xs font-semibold text-gray-400 px-3 py-2 uppercase tracking-wider">Donor Actions</p>
          <ul class="mt-1 space-y-1">
            <li v-for="(link, index) in links.donor" :key="index">
              <router-link :to="link.path"
                class="flex items-center p-3 rounded-lg hover:bg-gray-800/50 transition-all group"
                :class="{ 'bg-yellow-900/30 border-l-4 border-yellow-400': activeLink === link.path }"
                @click="closeSidebar">
                <svg class="w-5 h-5 mr-3 text-gray-400 group-hover:text-yellow-300" fill="none" stroke="currentColor"
                  viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="link.icon" />
                </svg>
                <span class="text-gray-300 group-hover:text-white">{{ link.name }}</span>
              </router-link>
            </li>
          </ul>
        </li>

        <!-- Campaign Manager Section -->
        <li class="mt-4" v-if="userRole === 'campaign_manager'">
          <p class="text-xs font-semibold text-gray-400 px-3 py-2 uppercase tracking-wider">Campaign Actions</p>
          <ul class="mt-1 space-y-1">
            <li v-for="(link, index) in links.campaignOrganizer" :key="index">
              <router-link :to="link.path"
                class="flex items-center p-3 rounded-lg hover:bg-gray-800/50 transition-all group"
                :class="{ 'bg-yellow-900/30 border-l-4 border-yellow-400': activeLink === link.path }"
                @click="closeSidebar">
                <svg class="w-5 h-5 mr-3 text-gray-400 group-hover:text-yellow-300" fill="none" stroke="currentColor"
                  viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="link.icon" />
                </svg>
                <span class="text-gray-300 group-hover:text-white">{{ link.name }}</span>
              </router-link>
            </li>
          </ul>
        </li>

        <!-- Super Admin Section -->
        <li class="mt-4" v-if="userRole === 'superadmin'">
          <p class="text-xs font-semibold text-gray-400 px-3 py-2 uppercase tracking-wider">Super Admin Tools</p>
          <ul class="mt-1 space-y-1">
            <li v-for="(link, index) in links.admin" :key="index">
              <router-link :to="link.path"
                class="flex items-center p-3 rounded-lg hover:bg-gray-800/50 transition-all group"
                :class="{ 'bg-yellow-900/30 border-l-4 border-yellow-400': activeLink === link.path }"
                @click="closeSidebar">
                <svg class="w-5 h-5 mr-3 text-gray-400 group-hover:text-yellow-300" fill="none" stroke="currentColor"
                  viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="link.icon" />
                </svg>
                <span class="text-gray-300 group-hover:text-white">{{ link.name }}</span>
              </router-link>
            </li>
          </ul>
        </li>

        <!-- Notifications Section -->
        <li class="mt-4">
          <p class="text-xs font-semibold text-gray-400 px-3 py-2 uppercase tracking-wider">Notifications</p>
          <ul class="mt-1 space-y-1">
            <li v-for="(link, index) in links.notifications" :key="index">
              <router-link :to="link.path"
                class="flex items-center p-3 rounded-lg hover:bg-gray-800/50 transition-all group"
                :class="{ 'bg-yellow-900/30 border-l-4 border-yellow-400': activeLink === link.path }"
                @click="closeSidebar">
                <div class="relative">
                  <svg class="w-5 h-5 mr-3 text-gray-400 group-hover:text-yellow-300" fill="none" stroke="currentColor"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="link.icon" />
                  </svg>
                  <span v-if="link.alertCount"
                    class="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
                </div>
                <span class="text-gray-300 group-hover:text-white">{{ link.name }}</span>
                <span v-if="link.alertCount"
                  class="ml-auto px-2 py-0.5 text-xs rounded-full bg-red-900/50 text-red-300">{{ link.alertCount
                  }}</span>
              </router-link>
            </li>
          </ul>
        </li>

        <!-- Configuration Section -->
        <li class="mt-4">
          <p class="text-xs font-semibold text-gray-400 px-3 py-2 uppercase tracking-wider">Configuration</p>
          <ul class="mt-1 space-y-1">
            <li v-for="(link, index) in links.configuration" :key="index">
              <router-link :to="link.path"
                class="flex items-center p-3 rounded-lg hover:bg-gray-800/50 transition-all group"
                :class="{ 'bg-yellow-900/30 border-l-4 border-yellow-400': activeLink === link.path }"
                @click="closeSidebar">
                <svg class="w-5 h-5 mr-3 text-gray-400 group-hover:text-yellow-300" fill="none" stroke="currentColor"
                  viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="link.icon" />
                </svg>
                <span class="text-gray-300 group-hover:text-white">{{ link.name }}</span>
              </router-link>
            </li>
          </ul>
        </li>
      </ul>
    </nav>

    <!-- Bottom Section - User & Logout -->
    <div class="p-4  bg-black mt-auto" v-if="isOpen || !isMobile">
      <div class="flex items-center space-x-3 mb-4">
        <div class="relative">
          <div
            class="w-10 h-10 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center shadow-lg">
            <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <span class="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-gray-900"></span>
        </div>
        <div>
          <p class="font-medium text-gray-200">{{ userName }}</p>
          <p class="text-xs text-gray-400 capitalize">{{ userRole }}</p>
        </div>
      </div>
      <button @click="logout"
        class="w-full flex items-center justify-center p-2 rounded-lg bg-gray-800 hover:bg-gray-700/70 text-gray-300 hover:text-white transition-colors">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
        Logout
      </button>
    </div>
  </aside>
</template>

<script setup>
import { defineEmits, defineProps, onMounted, ref, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from '../../stores/user'

// Define props
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  isMobile: {
    type: Boolean,
    default: false,
  },
});

// Define emits
const emit = defineEmits(['close-sidebar']);

// Get router and route instances
const router = useRouter();
const route = useRoute();

// Track active link
const activeLink = ref('');

// Pinia user store
const userStore = useUserStore()

// Ensure we have session on mount and fetch profile if needed
onMounted(async () => {
  userStore.loadFromStorage()
  if (userStore.token && !userStore.user) {
    try { await userStore.fetchMe() } catch (_) {}
  }
})

// Derive user role and name from store
const userRole = computed(() => {
  const u = userStore.user || {}
  // Prefer explicit role if present; otherwise infer from Django flags
  if (u.role) return u.role
  if (u.is_superuser) return 'superadmin'
  if (u.is_staff) return 'campaign_organizer'
  return 'donor'
})

const userName = computed(() => {
  const u = userStore.user || {}
  const name = [u.first_name, u.last_name].filter(Boolean).join(' ').trim()
  return name || u.email || 'User'
})

// Organized links by section with custom icons
const links = {
  main: [
    {
      name: "Dashboard",
      path: "/admin",
      icon: "M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
    },
  ],
  donor: [
    {
      name: "Search Campaign",
      path: "/admin/campaigns/search",
      icon: "M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
    },
    {
      name: "Make Financial Donation",
      path: "/admin/donate",
      icon: "M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"
    },
    {
      name: "View Donation History",
      path: "/admin/donations/history",
      icon: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 000 4h-2a2 2 0 01-2-2"
    },

  ],
  campaignOrganizer: [
    {
      name: "Create Fundraising Campaign",
      path: "/admin/campaigns/create",
      icon: "M12 4v16m8-8H4"
    },
    {
      name: "Manage Campaign",
      path: "/admin/campaigns/manage",
      icon: "M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z"
    },
    {
      name: "Track Donation",
      path: "/admin/donations/track",
      icon: "M7 12l3-3 3 3 4-4M5 10l3-3 3 3 4-4"
    },
    {
      name: "Manage Notification",
      path: "/admin/notifications/manage",
      icon: "M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15.828a2 2 0 01-2.828 0l-4.414-4.414"
    },
    {
      name: "Generate Report",
      path: "/admin/reports/generate",
      icon: "M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
    },
  ],
  admin: [
    {
      name: "Manage Account",
      path: "/admin/accounts",
      icon: "M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"
    },
    {
      name: "Campaign Verification",
      path: "/admin/campaigns/verify",
      icon: "M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"
    },
    {
      name: "View Statistic",
      path: "/admin/statistics",
      icon: "M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
    },
  ],
  notifications: [
    {
      name: "View Notifications",
      path: "/admin/notifications",
      icon: "M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9",
      alertCount: 3
    },
  ],
};

// Update active link when route changes
watch(
  () => route.path,
  (newPath) => {
    activeLink.value = newPath;
  },
  { immediate: true }
);

// Set initial active link on component mount
onMounted(() => {
  activeLink.value = route.path;
});

// Methods
const closeSidebar = () => {
  if (props.isMobile) {
    emit('close-sidebar');
  }
};

const logout = async () => {
  await userStore.logout()
  router.push('/login')
};
</script>

<style scoped>
/* Custom scrollbar for sidebar */
nav::-webkit-scrollbar {
  width: 4px;
}

nav::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}

nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

nav::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Smooth transitions for active states */
.router-link-active {
  transition: all 0.2s ease;
}

/* Gradient border effect for active items */
.border-l-4 {
  border-image: linear-gradient(to bottom, #fbbf24, #f97316) 1;
}

/* Pulse animation for active items */
@keyframes pulse-glow {

  0%,
  100% {
    box-shadow: 0 0 5px rgba(251, 191, 36, 0.5);
  }

  50% {
    box-shadow: 0 0 20px rgba(251, 191, 36, 0.8);
  }
}

.bg-yellow-900\/30 {
  animation: pulse-glow 2s infinite;
}
</style>