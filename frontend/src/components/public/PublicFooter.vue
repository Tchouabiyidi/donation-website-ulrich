<template>
  <footer class="relative bg-gray-900 text-white">
    <!-- Main Footer Content -->
    <div class="container mx-auto px-4 sm:px-6 py-16">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        
        <!-- Organization Info -->
        <div class="lg:col-span-1">
          <div class="flex items-center space-x-3 mb-6">
            <div class="w-12 h-12 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center shadow-lg">
              <svg class="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <div>
              <h3 class="text-xl font-bold">Hope Foundation</h3>
              <p class="text-sm text-yellow-400">Changing Lives Together</p>
            </div>
          </div>
          <p class="text-gray-400 mb-6 leading-relaxed">
            We're dedicated to creating lasting change through clean water access, education, and healthcare programs in communities worldwide.
          </p>
          
          <!-- Social Links -->
          <div class="flex space-x-4">
            <a 
              v-for="social in socialLinks"
              :key="social.name"
              :href="social.url"
              :aria-label="social.name"
              class="w-10 h-10 bg-gray-800 hover:bg-gradient-to-br hover:from-yellow-500 hover:to-orange-500 rounded-full flex items-center justify-center transition-all duration-300 transform hover:scale-110"
            >
              <component :is="social.icon" class="w-5 h-5" />
            </a>
          </div>
        </div>

        <!-- Quick Links -->
        <div>
          <h4 class="text-lg font-semibold mb-6 text-yellow-400">Quick Links</h4>
          <ul class="space-y-3">
            <li v-for="link in quickLinks" :key="link.path">
              <router-link 
                :to="link.path"
                class="text-gray-400 hover:text-white transition-colors duration-200 flex items-center group"
              >
                <span class="group-hover:translate-x-1 transition-transform duration-200">{{ link.label }}</span>
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Programs & Services -->
        <div>
          <h4 class="text-lg font-semibold mb-6 text-yellow-400">Our Programs</h4>
          <ul class="space-y-3">
            <li v-for="program in programs" :key="program.path">
              <router-link 
                :to="program.path"
                class="text-gray-400 hover:text-white transition-colors duration-200 flex items-center group"
              >
                <span class="group-hover:translate-x-1 transition-transform duration-200">{{ program.label }}</span>
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Contact & Newsletter -->
        <div>
          <h4 class="text-lg font-semibold mb-6 text-yellow-400">Stay Connected</h4>
          
          <!-- Contact Info -->
          <div class="space-y-4 mb-6">
            <div class="flex items-start space-x-3">
              <svg class="w-5 h-5 text-yellow-400 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <div class="text-gray-400 text-sm">
                <p>Rue 123, Bastos</p>
                <p>Yaoundé, Centre Region</p>
              </div>
            </div>
            
            <div class="flex items-center space-x-3">
              <svg class="w-5 h-5 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <a href="mailto:info@hopefoundation.cm" class="text-gray-400 hover:text-white text-sm transition-colors">
                info@hopefoundation.cm
              </a>
            </div>
            
            <div class="flex items-center space-x-3">
              <svg class="w-5 h-5 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              <a href="tel:+237650000000" class="text-gray-400 hover:text-white text-sm transition-colors">
                +237 650 000 000
              </a>
            </div>
          </div>

          <!-- Newsletter Signup -->
          <div class="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
            <h5 class="text-sm font-semibold mb-3">Get Updates</h5>
            <form @submit.prevent="subscribeNewsletter" class="space-y-3">
              <input
                v-model="email"
                type="email"
                placeholder="Enter your email"
                class="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-sm"
                required
              />
              <button 
                type="submit"
                class="w-full px-3 py-2 bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 text-white text-sm font-medium rounded transition-all duration-200 transform hover:scale-105"
              >
                Subscribe
              </button>
            </form>
            <p class="text-xs text-gray-500 mt-2">Get monthly updates on our impact and programs.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Trust Indicators -->
    <div class="border-t border-gray-800">
      <div class="container mx-auto px-4 sm:px-6 py-8">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          <div v-for="indicator in trustIndicators" :key="indicator.label" class="group">
            <div class="text-2xl font-bold text-yellow-400 group-hover:scale-110 transition-transform duration-200">
              {{ indicator.value }}
            </div>
            <div class="text-sm text-gray-400">{{ indicator.label }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Bar -->
    <div class="border-t border-gray-800 bg-gray-900/50">
      <div class="container mx-auto px-4 sm:px-6 py-6">
        <div class="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <div class="text-sm text-gray-400">
            © {{ currentYear }} Hope Foundation. All rights reserved. 
            <span class="text-yellow-400">501(c)(3) Non-Profit Organization</span>
          </div>
          
          <div class="flex flex-wrap justify-center md:justify-end space-x-6 text-sm">
            <router-link 
              v-for="legal in legalLinks"
              :key="legal.path"
              :to="legal.path"
              class="text-gray-400 hover:text-white transition-colors duration-200"
            >
              {{ legal.label }}
            </router-link>
          </div>
        </div>
        
        <!-- Certifications -->
        <div class="flex justify-center md:justify-end mt-4 space-x-4">
          <div class="flex items-center space-x-2 text-xs text-gray-500">
            <svg class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>GuideStar Gold Seal</span>
          </div>
          <div class="flex items-center space-x-2 text-xs text-gray-500">
            <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>Charity Navigator 4-Star</span>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref, computed } from 'vue';

const email = ref('');

const currentYear = computed(() => new Date().getFullYear());

// Social media icons
const socialIcons = {
  facebook: {
    template: `<svg fill="currentColor" viewBox="0 0 24 24">
      <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
    </svg>`
  },
  twitter: {
    template: `<svg fill="currentColor" viewBox="0 0 24 24">
      <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
    </svg>`
  },
  instagram: {
    template: `<svg fill="currentColor" viewBox="0 0 24 24">
      <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 6.62 5.367 11.987 11.988 11.987 6.62 0 11.987-5.367 11.987-11.987C24.014 5.367 18.637.001 12.017.001zM8.449 16.988c-1.297 0-2.448-.73-3.016-1.789L4.659 7.73c.751-1.257 2.12-2.101 3.69-2.101h7.605c1.569 0 2.939.844 3.69 2.101l-.774 7.469c-.568 1.059-1.719 1.789-3.016 1.789H8.449z"/>
    </svg>`
  },
  linkedin: {
    template: `<svg fill="currentColor" viewBox="0 0 24 24">
      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
    </svg>`
  }
};

const socialLinks = ref([
  { name: 'Facebook', url: 'https://facebook.com/hopefoundation', icon: socialIcons.facebook },
  { name: 'Twitter', url: 'https://twitter.com/hopefoundation', icon: socialIcons.twitter },
  { name: 'Instagram', url: 'https://instagram.com/hopefoundation', icon: socialIcons.instagram },
  { name: 'LinkedIn', url: 'https://linkedin.com/company/hopefoundation', icon: socialIcons.linkedin }
]);

const quickLinks = ref([
  { path: '/donate', label: 'Make a Donation' },
  { path: '/volunteer', label: 'Volunteer' },
  { path: '/impact', label: 'Our Impact' },
  { path: '/news', label: 'Latest News' },
  { path: '/events', label: 'Upcoming Events' },
  { path: '/careers', label: 'Join Our Team' }
]);

const programs = ref([
  { path: '/programs/water', label: 'Clean Water Initiative' },
  { path: '/programs/education', label: 'Education for All' },
  { path: '/programs/healthcare', label: 'Healthcare Access' },
  { path: '/programs/emergency', label: 'Emergency Relief' },
  { path: '/programs/community', label: 'Community Development' }
]);

const legalLinks = ref([
  { path: '/privacy', label: 'Privacy Policy' },
  { path: '/terms', label: 'Terms of Service' },
  { path: '/financials', label: 'Financial Reports' },
  { path: '/transparency', label: 'Transparency' }
]);

const trustIndicators = ref([
  { value: '95%', label: 'Funds to Programs' },
  { value: '25K+', label: 'Lives Impacted' },
  { value: '4★', label: 'Charity Navigator' },
  { value: '15+', label: 'Years Serving' }
]);

const subscribeNewsletter = () => {
  // Handle newsletter subscription
  console.log('Subscribing email:', email.value);
  // Add your newsletter subscription logic here
  email.value = '';
  // Show success message
};
</script>

<style scoped>
/* Custom animations and enhancements */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.group:hover svg {
  animation: slideIn 0.3s ease-out;
}

/* Ensure proper spacing and alignment */
.container {
  max-width: 1200px;
}

/* Custom focus styles for accessibility */
/* input:focus, button:focus {
  outline: 2px solid theme('colors.yellow.400');
  outline-offset: 2px;
} */
</style>