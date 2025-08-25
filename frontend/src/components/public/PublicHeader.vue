<template>
    <header class="fixed top-0 left-0 right-0 bg-gray-900/95 backdrop-blur-sm border-b border-gray-800 h-20 z-50">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="flex items-center justify-between h-20">
          <!-- Logo -->
          <router-link 
            to="/" 
            class="flex items-center space-x-3 group"
            aria-label="Home"
          >
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-200">
              <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <div class="hidden sm:block">
              <span class="text-xl font-bold text-white">Hope Foundation</span>
              <div class="text-xs text-yellow-400 -mt-1">Changing Lives Together</div>
            </div>
          </router-link>
  
          <!-- Desktop Navigation -->
          <nav class="hidden md:flex items-center space-x-8">
            <router-link 
              v-for="link in navLinks" 
              :key="link.path"
              :to="link.path"
              class="text-gray-300 hover:text-yellow-400 px-3 py-2 text-sm font-medium transition-colors duration-200 relative group"
              active-class="text-yellow-400"
            >
              {{ link.label }}
              <span class="absolute bottom-0 left-0 w-full h-0.5 bg-yellow-400 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-200"></span>
            </router-link>
          </nav>
  
          <!-- Donation & Auth Buttons - Desktop -->
          <div class="hidden md:flex items-center space-x-4">
            <router-link 
              to="/volunteer" 
              class="text-gray-300 hover:text-white px-3 py-2 text-sm font-medium transition-colors duration-200"
            >
              Volunteer
            </router-link>
            <router-link 
              to="/signup" 
              class="bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 text-white px-6 py-2.5 rounded-full text-sm font-bold transition-all duration-200 transform hover:scale-105 shadow-lg"
            >
              Donate Now
            </router-link>
          </div>
  
          <!-- Mobile menu button -->
          <button 
            @click="isMobileMenuOpen = !isMobileMenuOpen"
            class="md:hidden text-gray-400 hover:text-yellow-400 focus:outline-none p-2"
            aria-label="Toggle menu"
          >
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path 
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="2" 
                :d="isMobileMenuOpen ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16M4 18h16'" 
              />
            </svg>
          </button>
        </div>
      </div>
  
      <!-- Mobile menu -->
      <transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="transform opacity-100 scale-100"
        leave-to-class="transform opacity-0 scale-95"
      >
        <div 
          v-show="isMobileMenuOpen"
          class="md:hidden absolute top-20 inset-x-0 bg-gray-900/98 backdrop-blur-sm border-t border-gray-800 shadow-xl"
        >
          <div class="px-4 pt-4 pb-6 space-y-2">
            <router-link
              v-for="link in navLinks"
              :key="link.path"
              :to="link.path"
              @click="isMobileMenuOpen = false"
              class="block px-4 py-3 rounded-lg text-base font-medium text-gray-300 hover:text-yellow-400 hover:bg-gray-800/50 transition-all duration-200"
              active-class="text-yellow-400 bg-gray-800/50"
            >
              {{ link.label }}
            </router-link>
            
            <div class="border-t border-gray-800 pt-4 mt-4">
              <router-link
                to="/volunteer"
                @click="isMobileMenuOpen = false"
                class="block px-4 py-3 rounded-lg text-base font-medium text-gray-300 hover:text-white hover:bg-gray-800/50 transition-all duration-200"
              >
                Become a Volunteer
              </router-link>
              <router-link
                to="/donate"
                @click="isMobileMenuOpen = false"
                class="block px-4 py-3 mt-2 rounded-lg text-base font-bold text-center text-white bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 transition-all duration-200 transform hover:scale-105 shadow-lg"
              >
                Make a Donation
              </router-link>
            </div>

            <!-- Emergency Support Banner -->
            <div class="mt-4 p-3 bg-red-900/30 border border-red-700/30 rounded-lg">
              <div class="text-sm text-red-400 font-medium mb-1">Emergency Response</div>
              <div class="text-xs text-gray-400">Help families affected by recent disasters</div>
              <router-link 
                to="/emergency"
                @click="isMobileMenuOpen = false"
                class="inline-block mt-2 text-xs text-red-400 hover:text-red-300 underline"
              >
                Learn More →
              </router-link>
            </div>
          </div>
        </div>
      </transition>
    </header>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { RouterLink } from 'vue-router';
  
  const isMobileMenuOpen = ref(false);
  
  const navLinks = [
    { path: '/', label: 'Home' },
    { path: '/causes', label: 'Our Causes' },
    { path: '/impact', label: 'Impact Stories' },
    { path: '/about', label: 'About Us' },
    { path: '/contact', label: 'Contact' }
  ];
  </script>
  
  <style scoped>
  /* Custom animations for charity theme */
  @keyframes pulse-glow {
    0%, 100% {
      box-shadow: 0 0 5px rgba(251, 191, 36, 0.5);
    }
    50% {
      box-shadow: 0 0 20px rgba(251, 191, 36, 0.8);
    }
  }

  .router-link[href="/donate"]:hover {
    animation: pulse-glow 2s infinite;
  }

  /* Ensure proper stacking context */
  header {
    position: relative;
    z-index: 1000;
  }
  </style>