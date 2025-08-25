<template>
  <div class="contact-page min-h-screen text-white relative">
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
          class="absolute inset-0 bg-cover bg-center will-change-opacity"
          :style="{ backgroundImage: `url(${image.src})` }"
        >
          <!-- Darkening overlay -->
          <div class="absolute inset-0 bg-black opacity-40"></div>
        </div>
      </transition-group>
    </div>
    <!-- Debug message to show current image and load status -->
    <div class="absolute top-4 left-4 z-40 text-white text-sm">
      Current Image: {{ images[currentImageIndex].src }} (Loaded: {{ images[currentImageIndex].loaded ? 'Yes' : 'No' }})
    </div>
    <!-- Fallback message if images fail to load -->
    <div v-if="!images.length || images.every(img => !img.loaded)" class="fixed inset-0 z-0 flex items-center justify-center text-white text-lg bg-gray-900">
      No images loaded. Please check image URLs.
    </div>

    <!-- Hero Section -->
    <section class="relative bg-transparent pt-24 pb-12 sm:pt-32 sm:pb-16 z-20">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="max-w-4xl mx-auto text-center">
          <h1 class="text-4xl sm:text-5xl md:text-6xl font-bold leading-tight mb-6  text-yellow-300 text-shadow-md">
            Get in <span class=" text-yellow-300 tbg-clip-text ">Touch</span>
          </h1>
          <p class="text-lg sm:text-xl text-blue-100 mb-8 max-w-3xl mx-auto">
            Have questions about our programs? Want to volunteer? Need help with donations? We're here to help and would love to hear from you.
          </p>
        </div>
      </div>
    </section>

    <!-- Contact Methods -->
    <section class="py-16 sm:py-24 bg-transparent z-20">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          <div 
            v-for="(method, index) in contactMethods"
            :key="index"
            class="bg-white/5 backdrop-blur-sm border border-gray-700/30 rounded-xl p-6 text-center hover:border-yellow-500/50 hover:bg-white/10 transition-all duration-300 group"
          >
            <div class="w-16 h-16 bg-gradient-to-br from-yellow-500 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
              <component :is="method.icon" class="w-8 h-8 text-white" aria-hidden="true" />
            </div>
            <h3 class="text-xl font-semibold text-white mb-3">{{ method.title }}</h3>
            <p class="text-gray-400 mb-4">{{ method.description }}</p>
            <div class="text-yellow-400 font-medium">
              <a 
                :href="method.link" 
                class="hover:text-yellow-300 transition-colors"
                :class="method.linkClass"
                :aria-label="method.title"
              >
                {{ method.contact }}
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Contact Form and Office Info -->
    <section class="py-16 sm:py-24 bg-transparent z-20">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
          
          <!-- Contact Form -->
          <div class="relative z-30 min-h-[400px]">
            <h2 class="text-3xl font-bold text-white mb-8 text-shadow-md" id="contact-form-heading">Send Us a Message</h2>
            
            <form @submit.prevent="submitForm" class="space-y-6" aria-labelledby="contact-form-heading">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-300 mb-2" for="firstName">First Name *</label>
                  <input
                    v-model="form.firstName"
                    id="firstName"
                    type="text"
                    required
                    class="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-white placeholder-gray-400"
                    placeholder="Enter your first name"
                    :aria-invalid="formErrors.firstName ? 'true' : 'false'"
                    @input="clearError('firstName')"
                  />
                  <p v-if="formErrors.firstName" class="text-red-400 text-sm mt-1">{{ formErrors.firstName }}</p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-300 mb-2" for="lastName">Last Name *</label>
                  <input
                    v-model="form.lastName"
                    id="lastName"
                    type="text"
                    required
                    class="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-white placeholder-gray-400"
                    placeholder="Enter your last name"
                    :aria-invalid="formErrors.lastName ? 'true' : 'false'"
                    @input="clearError('lastName')"
                  />
                  <p v-if="formErrors.lastName" class="text-red-400 text-sm mt-1">{{ formErrors.lastName }}</p>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2" for="email">Email Address *</label>
                <input
                  v-model="form.email"
                  id="email"
                  type="email"
                  required
                  class="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-white placeholder-gray-400"
                  placeholder="your.email@example.com"
                  :aria-invalid="formErrors.email ? 'true' : 'false'"
                  @input="clearError('email')"
                />
                <p v-if="formErrors.email" class="text-red-400 text-sm mt-1">{{ formErrors.email }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2" for="phone">Phone Number</label>
                <input
                  v-model="form.phone"
                  id="phone"
                  type="tel"
                  class="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-white placeholder-gray-400"
                  placeholder="+1 (555) 123-4567"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2" for="subject">Subject *</label>
                <select
                  v-model="form.subject"
                  id="subject"
                  required
                  class="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-white"
                  :aria-invalid="formErrors.subject ? 'true' : 'false'"
                  @change="clearError('subject')"
                >
                  <option value="">Select a subject</option>
                  <option value="general">General Inquiry</option>
                  <option value="donation">Donation Questions</option>
                  <option value="volunteer">Volunteer Opportunities</option>
                  <option value="partnership">Partnership Inquiry</option>
                  <option value="media">Media/Press</option>
                  <option value="support">Technical Support</option>
                  <option value="other">Other</option>
                </select>
                <p v-if="formErrors.subject" class="text-red-400 text-sm mt-1">{{ formErrors.subject }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2" for="message">Message *</label>
                <textarea
                  v-model="form.message"
                  id="message"
                  rows="6"
                  required
                  class="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-white placeholder-gray-400 resize-vertical"
                  placeholder="Tell us how we can help you..."
                  :aria-invalid="formErrors.message ? 'true' : 'false'"
                  @input="clearError('message')"
                ></textarea>
                <p v-if="formErrors.message" class="text-red-400 text-sm mt-1">{{ formErrors.message }}</p>
              </div>

              <div class="flex items-start space-x-3">
                <input
                  v-model="form.newsletter"
                  id="newsletter"
                  type="checkbox"
                  class="w-5 h-5 text-yellow-500 bg-gray-700 border-gray-600 rounded focus:ring-yellow-400 focus:ring-2"
                />
                <label for="newsletter" class="text-sm text-gray-300">
                  Subscribe to our newsletter to receive updates about our programs and impact stories.
                </label>
              </div>

              <div class="flex space-x-4">
                <button
                  type="submit"
                  :disabled="isSubmitting"
                  class="flex-1 px-6 py-3 bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg"
                >
                  <span v-if="!isSubmitting">Send Message</span>
                  <span v-else class="flex items-center justify-center">
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Sending...
                  </span>
                </button>
                <button
                  type="button"
                  @click="resetForm"
                  class="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-lg transition-all duration-200"
                >
                  Reset Form
                </button>
              </div>
            </form>

            <!-- Success Message -->
            <div 
              v-if="showSuccess"
              class="mt-6 p-4 bg-green-900/50 border border-green-700 rounded-lg"
            >
              <div class="flex items-center">
                <svg class="w-5 h-5 text-green-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p class="text-green-400 font-medium">Thank you for your message! We'll get back to you within 24 hours.</p>
              </div>
            </div>
          </div>

          <!-- Office Information -->
          <div class="relative z-30">
            <h2 class="text-3xl font-bold text-white mb-8 text-shadow-md">Visit Our Offices</h2>
            
            <div class="space-y-8">
              <div 
                v-for="(office, index) in offices"
                :key="index"
                class="bg-white/5 backdrop-blur-sm border border-gray-700/30 rounded-xl p-6 hover:border-yellow-500/50 hover:bg-white/10 transition-all duration-300"
              >
                <h3 class="text-xl font-semibold text-yellow-400 mb-4">{{ office.name }}</h3>
                <div class="space-y-3">
                  <div class="flex items-start space-x-3">
                    <svg class="w-5 h-5 text-yellow-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <div class="text-gray-300">
                      <p v-for="(line, i) in office.address" :key="i">{{ line }}</p>
                    </div>
                  </div>
                  
                  <div class="flex items-center space-x-3">
                    <svg class="w-5 h-5 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                    <a :href="`tel:${office.phone.replace(/\D/g, '')}`" class="text-gray-300 hover:text-white transition-colors">
                      {{ office.phone }}
                    </a>
                  </div>

                  <div class="flex items-center space-x-3">
                    <svg class="w-5 h-5 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <div class="text-gray-300">
                      <p class="font-medium">Office Hours:</p>
                      <p class="text-sm">{{ office.hours }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Emergency Contact -->
            <div class="mt-8 p-6 bg-red-900/30 border border-red-700/50 rounded-xl backdrop-blur-md">
              <h3 class="text-xl font-semibold text-red-400 mb-3 flex items-center text-shadow-md">
                <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                Emergency Contact
              </h3>
              <p class="text-gray-300 mb-2">For urgent humanitarian crises or emergency donations:</p>
              <p class="text-red-400 font-semibold text-lg">+1 (555) 911-HELP</p>
              <p class="text-gray-400 text-sm">Available 24/7 for crisis response</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="py-16 sm:py-24 bg-transparent z-20">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold text-white mb-4 text-shadow-md">
            Frequently Asked <span class="bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent">Questions</span>
          </h2>
          <p class="text-lg text-gray-400 max-w-2xl mx-auto">
            Quick answers to common questions. Can't find what you're looking for? Contact us directly.
          </p>
        </div>

        <div class="max-w-4xl mx-auto">
          <div class="space-y-4">
            <div 
              v-for="(faq, index) in faqs"
              :key="index"
              class="bg-white/5 backdrop-blur-sm border border-gray-700/30 rounded-xl overflow-hidden"
            >
              <button
                @click="toggleFaq(index)"
                class="w-full px-6 py-4 text-left flex justify-between items-center hover:bg-white/10 transition-colors duration-200"
                :aria-expanded="faq.isOpen"
                :aria-controls="`faq-content-${index}`"
              >
                <h3 class="text-lg font-semibold text-white">{{ faq.question }}</h3>
                <svg 
                  class="w-5 h-5 text-yellow-400 transform transition-transform duration-200"
                  :class="{ 'rotate-180': faq.isOpen }"
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <transition
                enter-active-class="transition-all duration-300 ease-out"
                enter-from-class="transform opacity-0 max-h-0"
                enter-to-class="transform opacity-100 max-h-96"
                leave-active-class="transition-all duration-300 ease-in"
                leave-from-class="transform opacity-100 max-h-96"
                leave-to-class="transform opacity-0 max-h-0"
              >
                <div v-show="faq.isOpen" :id="`faq-content-${index}`" class="px-6 pb-4">
                  <p class="text-gray-300 leading-relaxed">{{ faq.answer }}</p>
                </div>
              </transition>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="py-16 sm:py-24 bg-transparent z-20">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="max-w-4xl mx-auto text-center">
          <h2 class="text-3xl sm:text-4xl font-bold text-white mb-6 text-shadow-md">
            Ready to Make a Difference?
          </h2>
          <p class="text-lg text-blue-100 mb-10 max-w-3xl mx-auto">
            Don't wait to start changing lives. Your support can provide clean water, education, and healthcare to those who need it most.
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
import { ref, reactive, onMounted, onUnmounted } from 'vue';

// Slideshow images and logic
const images = ref([
  { src: 'https://images.pexels.com/photos/6646917/pexels-photo-6646917.jpeg', loaded: false }, // Volunteers distributing aid
  { src: 'https://images.pexels.com/photos/6646987/pexels-photo-6646987.jpeg', loaded: false }, // Humanitarian aid delivery
  { src: 'https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg', loaded: false }, // Community support and aid
]);

const imagesLoaded = ref(false);
const currentImageIndex = ref(0);

const changeImage = () => {
  console.log('Switching to image:', images.value[currentImageIndex.value + 1]?.src || images.value[0].src);
  currentImageIndex.value = (currentImageIndex.value + 1) % images.value.length;
};

onMounted(() => {
  console.log('Contact form mounted');
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

// Contact form
const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  subject: '',
  message: '',
  newsletter: false
});

const formErrors = reactive({
  firstName: '',
  lastName: '',
  email: '',
  subject: '',
  message: ''
});

const isSubmitting = ref(false);
const showSuccess = ref(false);

const validateForm = () => {
  let isValid = true;
  formErrors.firstName = form.firstName.trim() ? '' : 'First name is required';
  formErrors.lastName = form.lastName.trim() ? '' : 'Last name is required';
  formErrors.email = form.email.trim() && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email) ? '' : 'Valid email is required';
  formErrors.subject = form.subject ? '' : 'Subject is required';
  formErrors.message = form.message.trim() ? '' : 'Message is required';
  
  return !Object.values(formErrors).some(error => error);
};

const clearError = (field) => {
  formErrors[field] = '';
};

const submitForm = async () => {
  if (!validateForm()) return;
  
  isSubmitting.value = true;
  try {
    // Simulate form submission
    await new Promise(resolve => setTimeout(resolve, 2000));
    showSuccess.value = true;
    resetForm();
    setTimeout(() => showSuccess.value = false, 5000);
  } catch (error) {
    console.error('Error submitting form:', error);
  } finally {
    isSubmitting.value = false;
  }
};

const resetForm = () => {
  Object.keys(form).forEach(key => {
    if (typeof form[key] === 'boolean') form[key] = false;
    else form[key] = '';
  });
  Object.keys(formErrors).forEach(key => formErrors[key] = '');
};

// Contact method icons
const phoneIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
  </svg>`
};

const emailIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
  </svg>`
};

const chatIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
  </svg>`
};

const socialIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
  </svg>`
};

const contactMethods = ref([
  {
    title: 'Call Us',
    description: 'Speak directly with our team',
    contact: '+1 (234) 567-8900',
    link: 'tel:+12345678900',
    icon: phoneIcon,
    linkClass: ''
  },
  {
    title: 'Email Us',
    description: 'Send us a detailed message',
    contact: 'info@hopefoundation.org',
    link: 'mailto:info@hopefoundation.org',
    icon: emailIcon,
    linkClass: ''
  },
  {
    title: 'Live Chat',
    description: 'Get instant help online',
    contact: 'Chat Now',
    link: '#',
    icon: chatIcon,
    linkClass: 'cursor-pointer'
  },
  {
    title: 'Social Media',
    description: 'Follow us for updates',
    contact: '@HopeFoundation',
    link: '#',
    icon: socialIcon,
    linkClass: ''
  }
]);

const offices = ref([
  {
    name: 'Headquarters - New York',
    address: [
      '123 Hope Street',
      'New York, NY 10001',
      'United States'
    ],
    phone: '+1 (234) 567-8900',
    hours: 'Mon-Fri: 9:00 AM - 6:00 PM EST'
  },
  {
    name: 'West Coast Office - California',
    address: [
      '456 Mission Boulevard',
      'San Francisco, CA 94103',
      'United States'
    ],
    phone: '+1 (415) 555-0123',
    hours: 'Mon-Fri: 9:00 AM - 6:00 PM PST'
  },
  {
    name: 'International Office - London',
    address: [
      '789 Charity Lane',
      'London, SW1A 1AA',
      'United Kingdom'
    ],
    phone: '+44 20 7123 4567',
    hours: 'Mon-Fri: 9:00 AM - 5:00 PM GMT'
  }
]);

const faqs = ref([
  {
    question: 'How can I make a donation?',
    answer: 'You can donate online through our secure donation form, by phone at +1 (234) 567-8900, or by mail. We accept credit cards, PayPal, bank transfers, and checks. All donations are tax-deductible.',
    isOpen: false
  },
  {
    question: 'Is my donation tax-deductible?',
    answer: 'Yes! Hope Foundation is a registered 501(c)(3) non-profit organization. All donations are tax-deductible to the full extent allowed by law. You\'ll receive a tax receipt via email immediately after your donation.',
    isOpen: false
  },
  {
    question: 'How do you use donated funds?',
    answer: '95% of all donations go directly to our programs. Only 5% is used for administrative costs. We provide detailed annual reports showing exactly how funds are allocated across our water, education, and healthcare initiatives.',
    isOpen: false
  },
  {
    question: 'Can I volunteer with Hope Foundation?',
    answer: 'Absolutely! We offer both local and international volunteer opportunities. You can help with fundraising events, administrative tasks, or join our field missions. Visit our volunteer page or contact us to learn about current opportunities.',
    isOpen: false
  },
  {
    question: 'How can I track the impact of my donation?',
    answer: 'We provide regular updates through our newsletter, impact reports, and personal donor portal. You can see photos, videos, and stories from the communities your donation has helped, along with specific metrics on lives improved.',
    isOpen: false
  },
  {
    question: 'Do you work in my local area?',
    answer: 'While our international programs focus on developing countries, we also have local community outreach programs in major US cities. Contact us to learn about volunteer and partnership opportunities in your area.',
    isOpen: false
  }
]);

const toggleFaq = (index) => {
  faqs.value[index].isOpen = !faqs.value[index].isOpen;
};
</script>

<style scoped>
.contact-page {
  scroll-behavior: smooth;
}

/* Smooth crossfade transition for images */
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
input:focus, 
select:focus, 
textarea:focus, 
button:focus {
  outline: 2px solid #facc15; /* Tailwind yellow-400 */
  outline-offset: 2px;
}

/* Custom scrollbar for textarea */
textarea::-webkit-scrollbar {
  width: 8px;
}

textarea::-webkit-scrollbar-track {
  background: #1f2937; /* Tailwind gray-800 */
  border-radius: 4px;
}

textarea::-webkit-scrollbar-thumb {
  background: #4b5563; /* Tailwind gray-600 */
  border-radius: 4px;
}

/* Enhanced transitions */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

/* Hover effects for buttons */
button:hover:not(:disabled),
a:hover:not(.cursor-pointer) {
  transform: translateY(-2px);
}

/* Ensure form elements are readable */
.bg-gray-700\/50 {
  background-color: rgba(55, 65, 81, 0.5); /* Tailwind gray-700 with 50% opacity */
}

/* Text shadow for better contrast */
.text-shadow-md {
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

/* Optimize slideshow rendering */
.will-change-opacity {
  will-change: opacity;
}
</style>