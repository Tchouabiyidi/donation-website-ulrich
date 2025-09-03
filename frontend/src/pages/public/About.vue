<template>
  <div class="about-page min-h-screen bg-black text-white relative">
    <!-- Background image slideshow with fixed position and darkening overlay -->
    <div v-if="!imagesLoaded" class="fixed inset-0 z-0 flex items-center justify-center bg-gray-900">
      <svg class="animate-spin h-8 w-8 text-yellow-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
    <div class="fixed inset-0 z-0">
      <transition-group name="fade" tag="div" class="relative w-full h-full">
        <div
          v-for="(image, index) in images"
          :key="image.src"
          v-show="currentImageIndex === index"
          class="absolute inset-0 bg-cover bg-center"
          :style="{ backgroundImage: `url(${image.src})` }"
        >
          <!-- Darkening overlay -->
          <div class="absolute inset-0 bg-black opacity-40"></div>
        </div>
      </transition-group>
    </div>
   

    <!-- Hero Section -->
    <section class="relative bg-transparent pt-24 pb-12 sm:pt-32 sm:pb-16 z-10">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="max-w-4xl mx-auto text-center">
          <h1 class="text-4xl sm:text-5xl md:text-6xl font-bold leading-tight mb-6">
            About <span class="bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent">Care Cameroon</span>
          </h1>
          <p class="text-lg sm:text-xl text-blue-100 mb-8 max-w-3xl mx-auto">
            For over 15 years, we've been dedicated to creating lasting change in communities around the world through sustainable programs that address the most pressing humanitarian needs.
          </p>
          <div class="flex justify-center">
            <div class="bg-white/10 backdrop-blur-sm rounded-full px-6 py-3 border border-yellow-400/30">
              <span class="text-yellow-400 font-semibold">Est. 2009 • 501(c)(3) Non-Profit</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Mission, Vision, Values -->
    <section class="py-16 sm:py-24 bg-transparent z-10">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div 
            v-for="(pillar, index) in organizationPillars"
            :key="index"
            class="bg-white/5 backdrop-blur-sm border border-gray-700/30 rounded-xl p-8 text-center hover:border-yellow-500/50 hover:bg-white/10 transition-all duration-300 group"
          >
            <div class="w-16 h-16 bg-gradient-to-br from-yellow-500 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
              <component :is="pillar.icon" class="w-8 h-8 text-white" aria-hidden="true" />
            </div>
            <h3 class="text-2xl font-bold text-white mb-4">{{ pillar.title }}</h3>
            <p class="text-gray-400 leading-relaxed">{{ pillar.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Our Story -->
    <section class="py-16 sm:py-24 bg-transparent z-10">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="flex flex-col lg:flex-row items-center gap-12">
          <div class="lg:w-1/2">
            <h2 class="text-3xl sm:text-4xl font-bold text-white mb-6">
              Our <span class="bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent">Story</span>
            </h2>
            <div class="space-y-6 text-gray-300">
              <p class="text-lg leading-relaxed">
                Care Cameroon was born from a simple yet powerful belief: every person deserves access to clean water, quality education, and basic healthcare. What started as a small group of volunteers in 2009 has grown into a global movement touching lives across four continents.
              </p>
              <p class="leading-relaxed">
                Our founder, Dr. Sarah Martinez, witnessed firsthand the devastating impact of water scarcity during a medical mission in rural Guatemala. That experience ignited a passion that would eventually mobilize thousands of supporters and transform entire communities.
              </p>
              <p class="leading-relaxed">
                Today, we've expanded our reach to include comprehensive education programs, emergency relief efforts, and sustainable community development projects. Every program we launch is designed with one goal in mind: creating lasting, positive change that empowers communities to thrive independently.
              </p>
            </div>
            <div class="mt-8">
              <router-link 
                to="/impact" 
                class="inline-flex items-center px-6 py-3 bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-semibold rounded-lg transition-all duration-200 transform hover:scale-105"
                aria-label="See Our Impact"
              >
                See Our Impact
                <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </router-link>
            </div>
          </div>
          <div class="lg:w-1/2">
            <div class="grid grid-cols-2 gap-4">
              <div class="bg-gradient-to-br from-yellow-400 to-orange-500 p-1 rounded-lg">
                <div class="bg-gray-800/80 backdrop-blur-sm rounded-lg p-6 h-full">
                  <div class="text-3xl font-bold text-yellow-400 mb-2">2009</div>
                  <div class="text-white font-semibold mb-1">Founded</div>
                  <div class="text-gray-400 text-sm">Started with a mission trip to Guatemala</div>
                </div>
              </div>
              <div class="bg-gradient-to-br from-blue-400 to-purple-500 p-1 rounded-lg">
                <div class="bg-gray-800/80 backdrop-blur-sm rounded-lg p-6 h-full">
                  <div class="text-3xl font-bold text-blue-400 mb-2">50+</div>
                  <div class="text-white font-semibold mb-1">Countries</div>
                  <div class="text-gray-400 text-sm">Global reach across four continents</div>
                </div>
              </div>
              <div class="bg-gradient-to-br from-green-400 to-teal-500 p-1 rounded-lg">
                <div class="bg-gray-800/80 backdrop-blur-sm rounded-lg p-6 h-full">
                  <div class="text-3xl font-bold text-green-400 mb-2">25K+</div>
                  <div class="text-white font-semibold mb-1">Lives Changed</div>
                  <div class="text-gray-400 text-sm">Direct beneficiaries of our programs</div>
                </div>
              </div>
              <div class="bg-gradient-to-br from-purple-400 to-pink-500 p-1 rounded-lg">
                <div class="bg-gray-800/80 backdrop-blur-sm rounded-lg p-6 h-full">
                  <div class="text-3xl font-bold text-purple-400 mb-2">500+</div>
                  <div class="text-white font-semibold mb-1">Volunteers</div>
                  <div class="text-gray-400 text-sm">Active volunteers worldwide</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Leadership Team -->
    <section class="py-16 sm:py-24 bg-transparent z-10">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold text-white mb-4">
            Leadership <span class="bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent">Team</span>
          </h2>
          <p class="text-lg text-gray-400 max-w-2xl mx-auto">
            Meet the passionate individuals who guide our mission and ensure every donation creates maximum impact.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div 
            v-for="(member, index) in teamMembers"
            :key="index"
            class="bg-white/5 backdrop-blur-sm border border-gray-700/30 rounded-xl p-6 text-center hover:border-yellow-500/50 hover:bg-white/10 transition-all duration-300 group"
          >
            <div class="w-24 h-24 bg-gradient-to-br from-gray-600 to-gray-800 rounded-full mx-auto mb-4 flex items-center justify-center group-hover:scale-105 transition-transform duration-300">
              <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-white mb-2">{{ member.name }}</h3>
            <div class="text-yellow-400 font-medium mb-3">{{ member.position }}</div>
            <p class="text-gray-400 text-sm mb-4">{{ member.bio }}</p>
            <div class="flex justify-center space-x-3">
              <a 
                v-for="social in member.social"
                :key="social.platform"
                :href="social.url"
                class="w-8 h-8 bg-gray-700 hover:bg-yellow-500 rounded-full flex items-center justify-center transition-colors duration-200"
                :aria-label="`${member.name}'s ${social.platform} profile`"
              >
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path v-if="social.platform === 'linkedin'" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                  <path v-else d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Awards & Recognition -->
    <section class="py-16 sm:py-24 bg-transparent z-10">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold text-white mb-4">
            Awards & <span class="bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent">Recognition</span>
          </h2>
          <p class="text-lg text-gray-400 max-w-2xl mx-auto">
            Our commitment to transparency and impact has been recognized by leading charity evaluators and humanitarian organizations.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div 
            v-for="(award, index) in awards"
            :key="index"
            class="bg-white/5 backdrop-blur-sm border border-gray-700/30 rounded-xl p-6 text-center hover:border-yellow-500/50 hover:bg-white/10 transition-all duration-300"
          >
            <div class="w-12 h-12 bg-gradient-to-br from-yellow-500 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-white mb-2">{{ award.title }}</h3>
            <p class="text-yellow-400 font-medium mb-1">{{ award.organization }}</p>
            <p class="text-gray-400 text-sm">{{ award.year }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="py-16 sm:py-24 bg-transparent z-10">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="max-w-4xl mx-auto text-center">
          <h2 class="text-3xl sm:text-4xl font-bold text-white mb-6">
            Ready to Join Our Mission?
          </h2>
          <p class="text-lg text-blue-100 mb-10 max-w-3xl mx-auto">
            Every great change starts with someone who cares. Whether through donations, volunteering, or spreading awareness, you can be part of our story of hope and transformation.
          </p>
          <div class="flex flex-col sm:flex-row justify-center gap-4">
            <router-link 
              to="/donate" 
              class="inline-block px-8 py-4 bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-bold rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg"
              aria-label="Make a Donation"
            >
              Make a Donation
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

// Slideshow images and logic
const images = ref([
  { src: 'https://images.pexels.com/photos/6646856/pexels-photo-6646856.jpeg', loaded: false }, // Community aid distribution
  { src: 'https://images.pexels.com/photos/6646878/pexels-photo-6646878.jpeg', loaded: false }, // Humanitarian support
  { src: 'https://images.pexels.com/photos/3184292/pexels-photo-3184292.jpeg', loaded: false }, // Relief efforts
]);

const imagesLoaded = ref(false);
const currentImageIndex = ref(0);

const changeImage = () => {
  console.log('Switching to image:', images.value[currentImageIndex.value + 1]?.src || images.value[0].src);
  currentImageIndex.value = (currentImageIndex.value + 1) % images.value.length;
};

onMounted(() => {
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

// Organization pillars icons
const missionIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
  </svg>`
};

const visionIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
  </svg>`
};

const valuesIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
  </svg>`
};

const organizationPillars = ref([
  {
    title: "Mission",
    description: "To provide sustainable solutions for clean water, education, and healthcare access to underserved communities worldwide, empowering them to build brighter futures.",
    icon: missionIcon
  },
  {
    title: "Vision", 
    description: "A world where every person has equal access to life's basic necessities and the opportunity to reach their full potential, regardless of where they are born.",
    icon: visionIcon
  },
  {
    title: "Values",
    description: "Transparency, sustainability, respect for local communities, accountability, and unwavering commitment to creating lasting positive change.",
    icon: valuesIcon
  }
]);

const teamMembers = ref([
  {
    name: "Dr. Sarah Martinez",
    position: "Founder & CEO",
    bio: "A medical doctor with 20+ years in global health. Sarah's passion for humanitarian work led to the founding of Care Cameroon.",
    social: [
      { platform: "linkedin", url: "#" },
      { platform: "twitter", url: "#" }
    ]
  },
  {
    name: "Michael Chen",
    position: "Director of Operations",
    bio: "Former UN program coordinator with expertise in logistics and sustainable development across Africa and Asia.",
    social: [
      { platform: "linkedin", url: "#" }
    ]
  },
  {
    name: "Dr. Amara Okafor",
    position: "Head of Programs",
    bio: "Public health specialist with a focus on water sanitation and community health education in rural areas.",
    social: [
      { platform: "linkedin", url: "#" },
      { platform: "twitter", url: "#" }
    ]
  },
  {
    name: "James Rodriguez",
    position: "Finance Director",
    bio: "CPA with 15+ years in non-profit financial management, ensuring maximum impact from every donation.",
    social: [
      { platform: "linkedin", url: "#" }
    ]
  },
  {
    name: "Lisa Thompson",
    position: "Communications Director",
    bio: "Former journalist specializing in humanitarian storytelling and donor engagement strategies.",
    social: [
      { platform: "linkedin", url: "#" },
      { platform: "twitter", url: "#" }
    ]
  },
  {
    name: "Dr. Hassan Al-Rashid",
    position: "Education Program Lead",
    bio: "Education policy expert with experience developing curriculum for underserved communities in the Middle East.",
    social: [
      { platform: "linkedin", url: "#" }
    ]
  }
]);

const awards = ref([
  {
    title: "4-Star Rating",
    organization: "Charity Navigator",
    year: "2023"
  },
  {
    title: "Gold Seal",
    organization: "GuideStar",
    year: "2023"
  },
  {
    title: "Top-Rated Nonprofit",
    organization: "GreatNonprofits",
    year: "2022"
  },
  {
    title: "Excellence Award",
    organization: "Global Impact Alliance",
    year: "2021"
  },
  {
    title: "Innovation in Healthcare",
    organization: "World Health Forum",
    year: "2020"
  },
  {
    title: "Water Project Award",
    organization: "UN Water Initiative",
    year: "2019"
  },
  {
    title: "Education Impact",
    organization: "Global Education Fund",
    year: "2018"
  },
  {
    title: "Transparency Leader",
    organization: "Nonprofit Quarterly",
    year: "2017"
  }
]);
</script>

<style scoped>
.about-page {
  scroll-behavior: smooth;
}

/* Smooth crossfade transition for images */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-move {
  transition: all 1s ease-in-out;
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

/* Custom animations for enhanced user experience */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.group:hover {
  animation: fadeInUp 0.3s ease-out forwards;
}

/* Enhanced focus styles for accessibility */
a:focus,
button:focus {
  outline: 2px solid #facc15; /* Tailwind yellow-400 */
  outline-offset: 2px;
}

/* Hover effects for buttons */
button:hover:not(:disabled),
a:hover:not(.cursor-pointer) {
  transform: translateY(-2px);
}

/* Ensure content spacing */
section {
  position: relative;
}
</style>