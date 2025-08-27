<template>
  <div class="login-page min-h-screen text-white relative">
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
    

    <!-- Hero Section -->
    <section class="relative bg-transparent pt-24 pb-12 sm:pt-32 sm:pb-16 z-20">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="max-w-3xl mx-auto text-center">
          <h1 class="text-4xl sm:text-5xl md:text-6xl font-bold leading-tight mb-6 text-shadow-md">
            Welcome Back to <span class="bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent">Hope</span>
          </h1>
          <p class="text-lg sm:text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Log in to access your account, manage donations, or join our community efforts. Enter your credentials below.
          </p>
        </div>
      </div>
    </section>

    <!-- Login Form -->
    <section class="py-16 sm:py-24 bg-transparent z-20">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="max-w-xl mx-auto">
          <div class="relative z-30 min-h-[400px]">
            <h2 class="text-3xl font-bold text-white mb-8 text-shadow-md" id="login-form-heading">Sign In</h2>
            
            <form @submit.prevent="submitForm" class="space-y-6" aria-labelledby="login-form-heading">
              <!-- Error Message -->
              <div v-if="generalError" class="p-4 bg-red-900/50 border border-red-700 rounded-lg">
                <div class="flex items-start space-x-2">
                  <svg class="w-5 h-5 text-red-400 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M12 5a7 7 0 100 14 7 7 0 000-14z" />
                  </svg>
                  <p class="text-red-300 text-sm">{{ generalError }}</p>
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
                  placeholder="you@example.cm"
                  :aria-invalid="formErrors.email ? 'true' : 'false'"
                  @input="clearError('email')"
                />
                <p v-if="formErrors.email" class="text-red-400 text-sm mt-1">{{ formErrors.email }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2" for="password">Password *</label>
                <input
                  v-model="form.password"
                  id="password"
                  type="password"
                  required
                  class="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-white placeholder-gray-400"
                  placeholder="Enter your password"
                  :aria-invalid="formErrors.password ? 'true' : 'false'"
                  @input="clearError('password')"
                />
                <p v-if="formErrors.password" class="text-red-400 text-sm mt-1">{{ formErrors.password }}</p>
              </div>

              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <input
                    v-model="form.remember"
                    id="remember"
                    type="checkbox"
                    class="w-5 h-5 text-yellow-500 bg-gray-700 border-gray-600 rounded focus:ring-yellow-400 focus:ring-2"
                  />
                  <label for="remember" class="text-sm text-gray-300">
                    Remember me
                  </label>
                </div>
                <a href="#" class="text-sm text-yellow-400 hover:text-yellow-300 transition-colors">Forgot Password?</a>
              </div>

              <div>
                <button
                  type="submit"
                  :disabled="isSubmitting"
                  class="w-full px-6 py-3 bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg"
                >
                  <span v-if="!isSubmitting">Log In</span>
                  <span v-else class="flex items-center justify-center">
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Logging In...
                  </span>
                </button>
              </div>

              <!-- Success Message -->
              <div 
                v-if="showSuccess"
                class="mt-6 p-4 bg-green-900/50 border border-green-700 rounded-lg"
              >
                <div class="flex items-center">
                  <svg class="w-5 h-5 text-green-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p class="text-green-400 font-medium">Login successful! Redirecting...</p>
                </div>
              </div>
            </form>

            <p class="mt-6 text-center text-gray-400">
              Don't have an account? <router-link to="/signup" class="text-yellow-400 hover:text-yellow-300">Register here</router-link>.
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'

// Slideshow images with Black people in African backgrounds
const images = ref([
  { src: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80', loaded: false }, // Maasai woman
  { src: 'https://images.pexels.com/photos/247851/pexels-photo-247851.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', loaded: false }, // Group in traditional attire
  { src: 'https://images.unsplash.com/photo-1503614472-8d36e1c1d7f6?auto=format&fit=crop&q=80', loaded: false }, // Rural African village scene
]);

const imagesLoaded = ref(false);
const currentImageIndex = ref(0);

const changeImage = () => {
  console.log('Switching to image:', images.value[currentImageIndex.value + 1]?.src || images.value[0].src);
  currentImageIndex.value = (currentImageIndex.value + 1) % images.value.length;
};

onMounted(() => {
  console.log('Login form mounted');
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

// Login form
const form = reactive({
  email: '',
  password: '',
  remember: false
});

const formErrors = reactive({
  email: '',
  password: ''
});

const isSubmitting = ref(false);
const showSuccess = ref(false);
const generalError = ref('');
const router = useRouter()
const userStore = useUserStore()

const validateForm = () => {
  let isValid = true;
  formErrors.email = form.email.trim() && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email) ? '' : 'Valid email is required';
  formErrors.password = form.password.length >= 8 ? '' : 'Password must be at least 8 characters';
  
  return !Object.values(formErrors).some(error => error);
};

const clearError = (field) => {
  formErrors[field] = '';
};

const submitForm = async () => {
  if (!validateForm()) return;
  generalError.value = ''
  isSubmitting.value = true;
  try {
    await userStore.login({ email: form.email.trim(), password: form.password });
    showSuccess.value = true;
    // Role-based redirect after short delay for UX
    setTimeout(() => {
      const role = userStore.user?.role
      let target = '/admin'
      if (role === 'superadmin') target = '/admin/accounts'
      else if (role === 'campaign_manager') target = '/admin/campaigns/manage'
      else if (role === 'donor') target = '/admin/campaigns/search'
      router.push(target)
    }, 500)
  } catch (e) {
    console.error('Login failed:', e?.response?.data || e)
    const data = e?.response?.data
    let msg = userStore.error || e.message || 'Login failed'
    if (data && typeof data === 'object') {
      try { msg = Object.values(data).flat().join(' ') } catch { msg = JSON.stringify(data) }
    } else if (typeof data === 'string') {
      msg = data
    }
    // surface minimal error near fields
    formErrors.email = ''
    formErrors.password = msg
    generalError.value = msg
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
</script>

<style scoped>
.login-page {
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