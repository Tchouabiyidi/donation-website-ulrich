<template>
  <div class="registration-page min-h-screen text-white relative">
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
            Join the <span class="bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent">Hope</span> Community
          </h1>
          <p class="text-lg sm:text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Register to become a volunteer, donor, or supporter and help us make a difference. Fill out the form below to get started.
          </p>
        </div>
      </div>
    </section>

    <!-- Registration Form -->
    <section class="py-16 sm:py-24 bg-transparent z-20">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="max-w-xl mx-auto">
          <div class="relative z-30 min-h-[500px]">
            <h2 class="text-3xl font-bold text-white mb-8 text-shadow-md" id="registration-form-heading">Create Your Account</h2>
            
            <form @submit.prevent="submitForm" class="space-y-6" aria-labelledby="registration-form-heading">
              <!-- Error Message -->
              <div v-if="generalError" class="p-4 bg-red-900/50 border border-red-700 rounded-lg">
                <div class="flex items-start space-x-2">
                  <svg class="w-5 h-5 text-red-400 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M12 5a7 7 0 100 14 7 7 0 000-14z" />
                  </svg>
                  <p class="text-red-300 text-sm">{{ generalError }}</p>
                </div>
              </div>
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
                  placeholder="you@example.cm"
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
                  placeholder="+237 650 000 000"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2" for="address">Address (Optional)</label>
                <input
                  v-model="form.address"
                  id="address"
                  type="text"
                  class="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-white placeholder-gray-400"
                  placeholder="Enter your address"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2" for="password">Password *</label>
                <input
                  v-model="form.password"
                  id="password"
                  type="password"
                  required
                  class="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-white placeholder-gray-400"
                  placeholder="Create a password"
                  :aria-invalid="formErrors.password ? 'true' : 'false'"
                  @input="clearError('password')"
                />
                <p v-if="formErrors.password" class="text-red-400 text-sm mt-1">{{ formErrors.password }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2" for="confirmPassword">Confirm Password *</label>
                <input
                  v-model="form.confirmPassword"
                  id="confirmPassword"
                  type="password"
                  required
                  class="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-white placeholder-gray-400"
                  placeholder="Confirm your password"
                  :aria-invalid="formErrors.confirmPassword ? 'true' : 'false'"
                  @input="clearError('confirmPassword')"
                />
                <p v-if="formErrors.confirmPassword" class="text-red-400 text-sm mt-1">{{ formErrors.confirmPassword }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2" for="role">Role (Optional)</label>
                <select
                  v-model="form.role"
                  id="role"
                  class="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-white"
                >
                  <option value="">Select a role</option>
                  <option value="campaign_manager">Campaign organizer</option>
                  <option value="donor">Donor</option>
                </select>
              </div>

              <div class="flex items-start space-x-3">
                <input
                  v-model="form.newsletter"
                  id="newsletter"
                  type="checkbox"
                  class="w-5 h-5 text-yellow-500 bg-gray-700 border-gray-600 rounded focus:ring-yellow-400 focus:ring-2"
                />
                <label for="newsletter" class="text-sm text-gray-300">
                  Subscribe to our newsletter for updates on programs and impact stories.
                </label>
              </div>

              <div class="flex space-x-4">
                <button
                  type="submit"
                  :disabled="isSubmitting"
                  class="flex-1 px-6 py-3 bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg"
                >
                  <span v-if="!isSubmitting">Register</span>
                  <span v-else class="flex items-center justify-center">
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Registering...
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
              <p class="mt-6 text-center text-gray-400">
              Already have an account? <router-link to="/login" class="text-yellow-400 hover:text-yellow-300">Login here</router-link>.
            </p>
               
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
                <p class="text-green-400 font-medium">Registration successful! Please check your email to verify your account.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue';
import { useUserStore } from '../../stores/user'

// Slideshow images and logic (reusing ContactPage images for consistency)
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
  console.log('Registration form mounted');
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

// Registration form
const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  address: '',
  password: '',
  confirmPassword: '',
  role: '',
  newsletter: false
});

const formErrors = reactive({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: ''
});

const isSubmitting = ref(false);
const showSuccess = ref(false);
const generalError = ref('');

const validateForm = () => {
  let isValid = true;
  formErrors.firstName = form.firstName.trim() ? '' : 'First name is required';
  formErrors.lastName = form.lastName.trim() ? '' : 'Last name is required';
  formErrors.email = form.email.trim() && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email) ? '' : 'Valid email is required';
  formErrors.password = form.password.length >= 8 ? '' : 'Password must be at least 8 characters';
  formErrors.confirmPassword = form.password === form.confirmPassword ? '' : 'Passwords do not match';
  
  return !Object.values(formErrors).some(error => error);
};

const clearError = (field) => {
  formErrors[field] = '';
};

const userStore = useUserStore()

const submitForm = async () => {
  if (!validateForm()) return;

  isSubmitting.value = true;
  generalError.value = ''
  try {
    const payload = {
      email: form.email,
      password: form.password,
      confirm_password: form.confirmPassword,
      first_name: form.firstName,
      last_name: form.lastName,
      phone: form.phone || '',
      accept_terms: true, // set to true; add a checkbox if you want user to opt-in
      newsletter: !!form.newsletter,
    }
    // Only include role when valid; backend allows donor or campaign_manager
    if (['donor', 'campaign_manager'].includes(form.role)) {
      payload.role = form.role
    }
    await userStore.register(payload)
    showSuccess.value = true;
    resetForm();
    setTimeout(() => (showSuccess.value = false), 5000);
  } catch (error) {
    console.error('Error submitting registration:', error?.response?.data || error);
    const raw = error?.response?.data
    const data = (raw && typeof raw === 'object' && raw.errors) ? raw.errors : raw
    let msg = userStore.error || error.message || 'Registration failed'
    if (data && typeof data === 'object') {
      try {
        // Map field-specific errors
        if (data.email) formErrors.email = Array.isArray(data.email) ? data.email.join(' ') : String(data.email)
        if (data.password) formErrors.password = Array.isArray(data.password) ? data.password.join(' ') : String(data.password)
        if (data.confirm_password) formErrors.confirmPassword = Array.isArray(data.confirm_password) ? data.confirm_password.join(' ') : String(data.confirm_password)
        if (data.first_name) formErrors.firstName = Array.isArray(data.first_name) ? data.first_name.join(' ') : String(data.first_name)
        if (data.last_name) formErrors.lastName = Array.isArray(data.last_name) ? data.last_name.join(' ') : String(data.last_name)
        // Aggregate a user-friendly message prioritizing email/password if present
        const firstFieldMsg = data.email?.[0] || data.password?.[0] || data.confirm_password?.[0] || data.first_name?.[0] || data.last_name?.[0]
        const nonField = data.non_field_errors ? (Array.isArray(data.non_field_errors) ? data.non_field_errors.join(' ') : String(data.non_field_errors)) : ''
        msg = firstFieldMsg || nonField || 'Registration failed'
      } catch { msg = JSON.stringify(data) }
    } else if (typeof data === 'string') {
      msg = data
    }
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
.registration-page {
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

/* Custom scrollbar for textarea (if added later) */
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