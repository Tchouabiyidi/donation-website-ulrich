<template>
    <header class="fixed top-0 left-0 right-0 bg-gray-900/  border-b border-gray-800 h-30 ">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <router-link 
            to="/" 
            class="flex items-center space-x-2 group ml"
            aria-label="Home"
          >
            <div class="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <span class="text-xl font-bold text-white hidden sm:inline-block">GasMonitor</span>
          </router-link>
  
          <!-- Desktop Navigation -->
          <nav class="hidden md:flex items-center space-x-8">
            <router-link 
              v-for="link in navLinks" 
              :key="link.path"
              :to="link.path"
              class="text-gray-300 hover:text-white px-1 py-2 text-sm font-medium transition-colors"
              active-class="text-blue-400 border-b-2 border-blue-400"
            >
              {{ link.label }}
            </router-link>
          </nav>
  
          <!-- Auth Buttons - Desktop -->
          <div class="hidden md:flex items-center space-x-4">
            <router-link 
              to="/login" 
              class="text-gray-300 hover:text-white px-3 py-2 text-sm font-medium transition-colors"
            >
              Sign In
            </router-link>
            <router-link 
              to="/register" 
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Get Started
            </router-link>
          </div>
  
          <!-- Mobile menu button -->
          <button 
            @click="isMobileMenuOpen = !isMobileMenuOpen"
            class="md:hidden text-gray-400 hover:text-white focus:outline-none"
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
        enter-active-class="transition ease-out duration-100"
        enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100"
        leave-active-class="transition ease-in duration-75"
        leave-from-class="transform opacity-100 scale-100"
        leave-to-class="transform opacity-0 scale-95"
      >
        <div 
          v-show="isMobileMenuOpen"
          class="md:hidden absolute top-16 inset-x-0 bg-gray-900 border-t border-gray-800 shadow-lg"
        >
          <div class="px-2 pt-2 pb-3 space-y-1">
            <router-link
              v-for="link in navLinks"
              :key="link.path"
              :to="link.path"
              @click="isMobileMenuOpen = false"
              class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-gray-800"
              active-class="text-blue-400 bg-gray-800"
            >
              {{ link.label }}
            </router-link>
            <div class="border-t border-gray-800 pt-2">
              <router-link
                to="/login"
                @click="isMobileMenuOpen = false"
                class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-gray-800"
              >
                Sign In
              </router-link>
              <router-link
                to="/register"
                @click="isMobileMenuOpen = false"
                class="block px-3 py-2 rounded-md text-base font-medium text-white bg-blue-600 hover:bg-blue-700"
              >
                Get Started
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
    { path: '/features', label: 'Features' },
    { path: '/pricing', label: 'Pricing' },
    { path: '/about', label: 'About' },
    { path: '/contact', label: 'Contact' }
  ];
  </script>
  
  <style scoped>
  /* .router-link-active:not(.router-link-exact-active) {
    @apply text-gray-300;
  } */
  </style>