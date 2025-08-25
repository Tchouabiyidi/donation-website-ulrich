<template>
  <div class="impact-story-page min-h-screen text-white relative">
    <!-- Background image slideshow with fixed position and persistent overlay -->
    <div v-if="!imagesLoaded" class="fixed inset-0 z-0 flex items-center justify-center bg-gray-900">
      <svg class="animate-spin h-8 w-8 text-yellow-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
    <div class="fixed inset-0 z-0">
      <div class="absolute inset-0 bg-black opacity-40"></div> <!-- Persistent overlay -->
      <transition-group name="fade" tag="div" class="relative w-full h-full">
        <div
          v-for="(image, index) in images"
          :key="image.src"
          v-show="currentImageIndex === index"
          class="absolute inset-0 bg-cover bg-center will-change-opacity"
          :style="{ backgroundImage: `url(${image.src})` }"
        ></div>
      </transition-group>
    </div>
    <!-- Debug message to show current image and transition state -->
    <div class="absolute top-4 left-4 z-50 text-white text-sm">
      Current Image: {{ images[currentImageIndex].src }} (Loaded: {{ images[currentImageIndex].loaded ? 'Yes' : 'No' }}, Transition: {{ isTransitioning ? 'Yes' : 'No' }})
    </div>
    <!-- Fallback message if images fail to load -->
    <div v-if="!images.length || images.every(img => !img.loaded)" class="fixed inset-0 z-0 flex items-center justify-center text-white text-lg bg-gray-900">
      No images loaded. Please check image URLs.
    </div>

    <!-- Hero Section -->
    <section class="relative bg-transparent pt-24 pb-12 sm:pt-32 sm:pb-16 z-40">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="max-w-4xl mx-auto text-center">
          <h1 class="text-4xl sm:text-5xl md:text-6xl font-bold leading-tight mb-6 text-shadow-md">
            Our <span class="bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent">Impact</span> Stories
          </h1>
          <p class="text-lg sm:text-xl text-blue-100 mb-8 max-w-3xl mx-auto">
            Discover how your support transforms lives. Read about the communities we've helped and the difference we're making together.
          </p>
        </div>
      </div>
    </section>

    <!-- Impact Story Section -->
    <section class="py-16 sm:py-24 bg-transparent z-40">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12">
          <!-- Story Content -->
          <div class="relative z-40">
            <h2 class="text-3xl font-bold text-white mb-6 text-shadow-md" id="story-heading">Water for Life: A Village Transformed</h2>
            <p class="text-gray-300 mb-6 leading-relaxed">
              In a remote village in Kenya, access to clean water was a daily struggle. Families walked miles to fetch contaminated water, leading to illness and lost opportunities, especially for children. Thanks to your generous donations, we partnered with local leaders to build a sustainable well, providing safe drinking water to over 500 people.
            </p>
            <div class="space-y-6">
              <div>
                <h3 class="text-xl font-semibold text-yellow-400 mb-2">Before</h3>
                <p class="text-gray-400">
                  Before the well, the community faced waterborne diseases, with children missing school to collect water. Women and girls spent hours daily on this task, limiting their education and economic opportunities.
                </p>
              </div>
              <div>
                <h3 class="text-xl font-semibold text-yellow-400 mb-2">After</h3>
                <p class="text-gray-400">
                  With the new well, clean water is now just steps away. Children attend school regularly, and women have time to start small businesses, boosting the local economy and health outcomes.
                </p>
              </div>
            </div>
          </div>

          <!-- Impact Metrics -->
          <div class="relative z-40 bg-white/5 backdrop-blur-sm border border-gray-700/30 rounded-xl p-6">
            <h3 class="text-2xl font-bold text-white mb-6 text-shadow-md">Impact at a Glance</h3>
            <div class="space-y-4">
              <div class="flex items-center">
                <svg class="w-6 h-6 text-yellow-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <div>
                  <p class="text-lg font-semibold text-white">People Served</p>
                  <p class="text-2xl text-yellow-400">512</p>
                </div>
              </div>
              <div class="flex items-center">
                <svg class="w-6 h-6 text-yellow-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>
                  <p class="text-lg font-semibold text-white">Funds Raised</p>
                  <p class="text-2xl text-yellow-400">$12,500</p>
                </div>
              </div>
              <div class="flex items-center">
                <svg class="w-6 h-6 text-yellow-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>
                  <p class="text-lg font-semibold text-white">Wells Built</p>
                  <p class="text-2xl text-yellow-400">1</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="py-16 sm:py-24 bg-transparent z-40">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="max-w-4xl mx-auto text-center">
          <h2 class="text-3xl sm:text-4xl font-bold text-white mb-6 text-shadow-md">
            Be Part of the Change
          </h2>
          <p class="text-lg text-blue-100 mb-10 max-w-3xl mx-auto">
            Your contribution can bring hope and clean water to more communities. Join us today!
          </p>
          <div class="flex flex-col sm:flex-row justify-center gap-4">
            <router-link 
              to="/donate" 
              class="inline-block px-8 py-4 bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-bold rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg"
              aria-label="Donate Now"
            >
              Donate Now
            </router-link>
            <router-link 
              to="/volunteer" 
              class="inline-block px-8 py-4 bg-transparent border-2 border-yellow-400 hover:bg-yellow-400 hover:text-gray-900 text-yellow-400 font-medium rounded-lg transition-all duration-200"
              aria-label="Become a Volunteer"
            >
              Become a Volunteer
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

// Slideshow images from ContactPage.vue
const images = ref([
  { src: 'https://images.pexels.com/photos/6646917/pexels-photo-6646917.jpeg', loaded: false }, // Volunteers distributing aid
  { src: 'https://images.pexels.com/photos/6646987/pexels-photo-6646987.jpeg', loaded: false }, // Humanitarian aid delivery
  { src: 'https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg', loaded: false }, // Community support and aid
]);

const imagesLoaded = ref(false);
const currentImageIndex = ref(0);
const isTransitioning = ref(false);

const changeImage = () => {
  console.log('Switching to image:', images.value[currentImageIndex.value + 1]?.src || images.value[0].src);
  isTransitioning.value = true;
  currentImageIndex.value = (currentImageIndex.value + 1) % images.value.length;
  setTimeout(() => { isTransitioning.value = false; }, 800); // Match transition duration
};

onMounted(() => {
  console.log('Impact story page mounted');
  let loadedCount = 0;
  images.value.forEach((image, index) => {
    const img = new Image();
    img.src = image.src;
    img.onload = () => {
      images.value[index].loaded = true;
      console.log(`Image loaded: ${image.src}`);
      loadedCount++;
      if (loadedCount === images.value.length) imagesLoaded.value = true;
    };
    img.onerror = () => {
      console.error(`Failed to load image: ${image.src}`);
      images.value[index].loaded = false;
      loadedCount++;
      if (loadedCount === images.value.length) imagesLoaded.value = true;
    };
  });
  console.log('Attempting to load images:', images.value.map(img => img.src));
  const intervalId = setInterval(changeImage, 5000);
  onUnmounted(() => clearInterval(intervalId));
});
</script>

<style scoped>
.impact-story-page {
  scroll-behavior: smooth;
}

/* Smooth crossfade transition for images with persistent visibility */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.8s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-move {
  transition: all 0.8s ease-in-out;
}

.fade-enter-active,
.fade-leave-active,
.fade-leave-to {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* Enhanced focus styles for accessibility */
a:focus,
button:focus {
  outline: 2px solid #facc15; /* Tailwind yellow-400 */
  outline-offset: 2px;
}

/* Enhanced transitions */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

/* Hover effects for buttons and links */
button:hover:not(:disabled),
a:hover:not(.cursor-pointer) {
  transform: translateY(-2px);
}

/* Ensure readability */
.bg-gray-700\/50 {
  background-color: rgba(55, 65, 81, 0.5); /* Tailwind gray-700 with 50% opacity for specific elements */
}

/* Text shadow for better contrast */
.text-shadow-md {
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

/* Optimize slideshow rendering */
.will-change-opacity {
  will-change: opacity;
}

/* Remove grey fallback background */
.z-40 {
  position: relative;
  background-color: transparent; /* Ensure full transparency */
}
</style>