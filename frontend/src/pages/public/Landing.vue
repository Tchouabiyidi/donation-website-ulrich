<template>
    <div class="charity-page">
      <!-- Hero Section -->
      <section class="relative  text-white pt-24 pb-20 sm:pt-32 sm:pb-28">
        <div class="container mx-auto px-4 sm:px-6">
          <div class="max-w-4xl mx-auto text-center">
            <h1 class="text-4xl sm:text-5xl md:text-6xl font-bold leading-tight mb-6">
              Making a Difference <br>
              <span class="text-yellow-400">One Life at a Time</span>
            </h1>
            <p class="text-lg sm:text-xl text-blue-100 mb-10 max-w-3xl mx-auto">
              Join our mission to provide clean water, education, and healthcare to communities in need around the world.
            </p>
            <div class="flex flex-col sm:flex-row justify-center gap-4">
              <router-link 
                to="/singup" 
                class="px-8 py-4 bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-bold rounded-lg transition-all duration-200 text-sm sm:text-base transform hover:scale-105 shadow-lg"
              >
                Donate Now
              </router-link>
              <router-link 
                to="/about" 
                class="px-8 py-4 bg-transparent border-2 border-white hover:bg-white hover:text-gray-900 text-white font-medium rounded-lg transition-all duration-200 text-sm sm:text-base"
              >
                Learn Our Story
              </router-link>
            </div>
          </div>
        </div>
        <div class="absolute inset-x-0 bottom-0 h-16 "></div>
      </section>
  
      <!-- Impact Stats -->
      <section class="py-16 sm:py-24 bg-gray-900/0">
        <div class="container mx-auto px-4 sm:px-6">
          <div class="text-center mb-16">
            <h2 class="text-3xl sm:text-4xl font-bold text-white mb-4">
              Our Impact So Far
            </h2>
            <p class="text-lg text-blue-400 max-w-2xl mx-auto">
              Together, we've changed thousands of lives across the globe
            </p>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            <div 
              v-for="(stat, index) in impactStats"
              :key="index"
              class="bg-white/5 backdrop-blur-sm border border-gray-700/30 rounded-xl p-8 text-center hover:border-yellow-500/50 transition-all duration-300"
            >
              <div class="text-4xl font-bold text-yellow-400 mb-2">
                {{ stat.number }}
              </div>
              <div class="text-xl font-semibold text-white mb-2">
                {{ stat.label }}
              </div>
              <p class="text-gray-400">
                {{ stat.description }}
              </p>
            </div>
          </div>

          <!-- Main Causes Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div 
              v-for="(cause, index) in causes"
              :key="index"
              class="bg-white/5 backdrop-blur-sm border border-gray-700/30 rounded-xl p-6 hover:border-yellow-500/50 transition-all duration-300 group"
            >
              <div class="w-16 h-16 bg-gradient-to-br from-yellow-500 to-orange-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                <component 
                  :is="cause.icon" 
                  class="w-8 h-8 text-white"
                />
              </div>
              <h3 class="text-xl font-semibold text-white mb-3">
                {{ cause.title }}
              </h3>
              <p class="text-gray-400 mb-4">
                {{ cause.description }}
              </p>
              <div class="text-yellow-400 font-semibold">
                {{ cause.impact }}
              </div>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Success Story Section -->
      <section class="py-16 sm:py-24 ">
        <div class="container mx-auto px-4 sm:px-6">
          <div class="flex flex-col lg:flex-row items-center gap-12">
            <div class="lg:w-1/2">
              <h2 class="text-3xl sm:text-4xl font-bold text-white mb-6">
                Real Stories of <br>
                <span class="text-yellow-400">Hope and Change</span>
              </h2>
              <p class="text-lg text-gray-300 mb-8">
                Every donation creates ripple effects of positive change. Here's how your contribution makes a difference in real lives.
              </p>
              <ul class="space-y-4">
                <li 
                  v-for="(item, index) in successPoints"
                  :key="index"
                  class="flex items-start"
                >
                  <svg class="w-5 h-5 text-green-400 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span class="text-gray-300">{{ item }}</span>
                </li>
              </ul>
              <div class="mt-8">
                <router-link 
                  to="/stories" 
                  class="inline-block px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-200"
                >
                  Read More Stories
                </router-link>
              </div>
            </div>
            <div class="lg:w-1/2">
              <div class="bg-gradient-to-br from-yellow-400 to-orange-500 p-2 rounded-xl shadow-2xl">
                <div class="bg-white rounded-lg p-8 text-center">
                  <div class="w-24 h-24 bg-gray-200 rounded-full mx-auto mb-4 flex items-center justify-center">
                    <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <h3 class="text-xl font-bold text-gray-900 mb-2">Maria, Age 12</h3>
                  <p class="text-gray-700 italic mb-4">
                    "Thanks to your donations, I can now go to school and dream of becoming a teacher to help other children in my village."
                  </p>
                  <div class="text-sm text-gray-600">Guatemala • Education Program</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
  
      <!-- CTA Section -->
      <section class="py-16 sm:py-24 bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 text-white">
        <div class="container mx-auto px-4 sm:px-6">
          <div class="max-w-4xl mx-auto text-center">
            <h2 class="text-3xl sm:text-4xl font-bold mb-6">
              Your donation can change everything
            </h2>
            <p class="text-lg text-blue-100 mb-10 max-w-3xl mx-auto">
              Every contribution, no matter the size, helps us build a better world. Join thousands of compassionate donors who are making a difference today.
            </p>
            <div class="flex flex-col sm:flex-row justify-center gap-4 mb-8">
              <router-link 
                to="/donate" 
                class="inline-block px-8 py-4 bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-bold rounded-lg transition-all duration-200 text-lg transform hover:scale-105 shadow-lg"
              >
                Make a Donation
              </router-link>
              <router-link 
                to="/volunteer" 
                class="inline-block px-8 py-4 bg-transparent border-2 border-yellow-400 hover:bg-yellow-400 hover:text-gray-900 text-yellow-400 font-medium rounded-lg transition-all duration-200 text-lg"
              >
                Volunteer With Us
              </router-link>
            </div>
            <div class="text-sm text-blue-200">
              100% of your donation goes directly to our programs. We cover operational costs separately.
            </div>
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  // Icons for causes
  const icons = {
    water: {
      template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 8.172V5L8 4z" />
      </svg>`
    },
    education: {
      template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
      </svg>`
    },
    health: {
      template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
      </svg>`
    }
  };
  
  const impactStats = ref([
    {
      number: "25,000+",
      label: "Lives Changed",
      description: "People directly impacted by our programs"
    },
    {
      number: "150+",
      label: "Communities",
      description: "Villages and towns we actively support"
    },
    {
      number: "95%",
      label: "Efficiency Rate",
      description: "Of donations go directly to programs"
    }
  ]);

  const causes = ref([
    {
      title: "Clean Water Access",
      description: "Building wells and water purification systems to provide safe drinking water to remote communities.",
      impact: "$50 provides clean water for 1 person for a year",
      icon: icons.water
    },
    {
      title: "Education for All",
      description: "Supporting schools, training teachers, and providing educational materials to children worldwide.",
      impact: "$100 sponsors a child's education for 3 months",
      icon: icons.education
    },
    {
      title: "Healthcare Support",
      description: "Delivering medical supplies, training healthcare workers, and building clinics in underserved areas.",
      impact: "$75 provides medical care for a family of 5",
      icon: icons.health
    }
  ]);
  
  const successPoints = ref([
    "99% of funded projects are completed successfully",
    "Real-time updates on how your donation is being used",
    "Local partnerships ensure sustainable long-term impact",
    "Transparent reporting with annual impact assessments",
    "Emergency response capabilities for crisis situations"
  ]);
  </script>
  
  <style scoped>
  .charity-page {
    scroll-behavior: smooth;
  }
  
  /* Additional animations for enhanced user experience */
  @keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
  }
  
  .group:hover .w-16 {
    animation: float 2s ease-in-out infinite;
  }
  </style>