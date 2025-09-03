<template>
  <header
    :class="[
      'fixed top-0 right-0 h-16 bg-black backdrop-blur-sm shadow-lg flex items-center justify-between px-4 sm:px-6 z-30 transition-all duration-300',
      sidebarCollapsed ? 'left-0' : 'left-72',
      isMobile ? 'left-0' : ''
    ]"
  >
    <!-- Mobile menu button -->
    <button 
      v-if="isMobile" 
      @click="$emit('toggle-sidebar', !sidebarCollapsed)" 
      class="text-gray-400 hover:text-yellow-400 focus:outline-none transition-colors p-2 rounded-lg hover:bg-gray-800/50"
      aria-label="Toggle sidebar"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
      </svg>
    </button>

    <!-- Logo for mobile -->
    <router-link 
      v-if="isMobile" 
      to="/" 
      class="flex items-center space-x-2 ml-2 md:hidden"
      aria-label="Home"
    >
      <div class="w-8 h-8 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center shadow-lg">
        <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
        </svg>
      </div>
      <h1 class="text-xl font-bold bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent">
        Care Cameroon</h1>
    </router-link>

    <!-- User controls -->
    <div class="flex items-center space-x-3">
      <!-- Quick Donate Button -->
      <router-link
        to="/donate"
        class="hidden sm:flex items-center px-3 py-2 bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 text-white rounded-lg text-sm font-medium transition-all duration-200 transform hover:scale-105 shadow-lg"
      >
        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Donate
      </router-link>

      <!-- Notification button with critical alerts indicator -->
      <div class="relative">
        <button 
          class="text-gray-400 hover:text-yellow-400 focus:outline-none transition-colors relative p-2 rounded-lg hover:bg-gray-800/50"
          @click="$emit('show-notifications')"
          aria-label="Show notifications"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
          </svg>
          <span
            v-if="unreadNotifications > 0"
            class="absolute top-1 right-1 h-2.5 w-2.5 rounded-full bg-red-500 border border-gray-900"
          >
            <span class="absolute top-0 right-0 h-full w-full rounded-full bg-red-500 animate-ping opacity-75"></span>
          </span>
        </button>
      </div>

      <!-- User profile dropdown -->
      <div class="relative group">
        <button
          class="flex items-center space-x-2 focus:outline-none p-1 rounded-lg hover:bg-gray-200/50 transition-colors"
          @click.stop="toggleDropdown"
          aria-label="Toggle user dropdown"
        >
          <div class="relative">
            <div class="w-8 h-8 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center shadow-lg">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <span class="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-green-500 border border-gray-900"></span>
          </div>
          <div class="hidden md:block text-left">
            <p class="text-xs font-medium text-gray-200 truncate max-w-[120px]">{{ userName }}</p>
            <p class="text-xs text-gray-400 capitalize">{{ userRole }}</p>
          </div>
          <svg
            class="hidden md:block w-4 h-4 text-gray-500 transform transition-transform duration-200"
            :class="{ 'rotate-180': dropdownOpen }"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>

        <!-- Dropdown menu -->
        <transition
          enter-active-class="transition ease-out duration-100"
          enter-from-class="transform opacity-0 scale-95"
          enter-to-class="transform opacity-100 scale-100"
          leave-active-class="transition ease-in duration-75"
          leave-from-class="transform opacity-100 scale-100"
          leave-to-class="transform opacity-0 scale-95"
        >
          <div
            v-show="dropdownOpen"
            class="absolute right-0 mt-2 w-48 bg-black backdrop-blur-sm rounded-md shadow-xl py-1 z-40 border"
            @click.stop
          >
            <router-link 
              to="/profile" 
              class="flex items-center px-4 py-2 text-sm text-gray-300 hover:bg-gray-700/50 hover:text-white transition-colors"
              @click="closeDropdown"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              Profile
            </router-link>
            <router-link 
              to="/settings" 
              class="flex items-center px-4 py-2 text-sm text-gray-300 hover:bg-gray-700/50 hover:text-white transition-colors"
              @click="closeDropdown"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              Settings
            </router-link>
            <div class="border-t my-1"></div>
            <a
              href="#"
              class="flex items-center px-4 py-2 text-sm text-gray-300 hover:bg-gray-700/50 hover:text-red-400 transition-colors"
              @click.prevent="logout"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
              </svg>
              Logout
            </a>
          </div>
        </transition>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'

// Define props
const props = defineProps({
  sidebarCollapsed: {
    type: Boolean,
    default: false,
  },
  unreadNotifications: {
    type: Number,
    default: 0,
  },
})

// Define emits
const emit = defineEmits(['toggle-sidebar', 'show-notifications'])

// Get router instance
const router = useRouter()

// Reactive data
const dropdownOpen = ref(false)
const isMobile = ref(window.innerWidth < 768)

// User store
const userStore = useUserStore()

// Derive display name and role from store
const userName = computed(() => {
  const u = userStore.user || {}
  const name = [u.first_name, u.last_name].filter(Boolean).join(' ').trim()
  return name || u.name || u.username || u.email || 'User'
})
const userRole = computed(() => {
  const role = userStore.user?.role || ''
  return String(role).replaceAll('_', ' ') || 'member'
})

// Methods
const checkMobile = () => {
  isMobile.value = window.innerWidth < 768
}

const logout = async () => {
  try { await userStore.logout() } finally {
    router.push('/login')
    closeDropdown()
  }
}

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const closeDropdown = () => {
  dropdownOpen.value = false
}

// Event listeners
onMounted(() => {
  // Ensure session is loaded when page refreshes
  if (!userStore.user) userStore.loadFromStorage()
  document.addEventListener('click', closeDropdown)
  window.addEventListener('resize', checkMobile)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', closeDropdown)
  window.removeEventListener('resize', checkMobile)
})
</script>

<style scoped>
/* Custom transition for dropdown */
.transition-all {
  transition: all 0.3s ease-in-out;
}

/* Pulse animation for active items */
@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 5px rgba(251, 191, 36, 0.5);
  }
  50% {
    box-shadow: 0 0 20px rgba(251, 191, 36, 0.8);
  }
}

/* Apply pulse animation to donate button */
.router-link[href="/donate"] {
  animation: pulse-glow 2s infinite;
}
</style>