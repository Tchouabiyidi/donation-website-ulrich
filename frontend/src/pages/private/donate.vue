<template>
  <div class="min-h-screen text-white relative">
    <!-- Background image slideshow with fixed position and darkening overlay -->
    
    <div class="fixed inset-0 z-0">
      <div class="absolute inset-0 bg-black opacity-40"></div>
      <transition-group name="fade" tag="div" class="relative w-full h-full">
       
      </transition-group>
    </div>
    

    <!-- Hero Section -->
    <section class="relative bg-transparent pt-24 pb-12 sm:pt-32 sm:pb-16 z-40">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="max-w-3xl mx-auto text-center">
          <h1 class="text-4xl sm:text-5xl md:text-6xl font-bold leading-tight mb-6 text-shadow-md">
            Support with a <span class="text-yellow-400">Donation</span>
          </h1>
          <p class="text-lg sm:text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Your contribution brings hope and change to communities in need. Make a difference today!
          </p>
        </div>
      </div>
    </section>

    <!-- Donation Form -->
    <section class="py-16 sm:py-24 bg-transparent z-40">
      <div class="container mx-auto px-4 sm:px-6">
        <div class="max-w-xl mx-auto">
          <div class="relative z-40 min-h-[400px]">
            <h2 class="text-3xl font-bold text-white mb-8 text-shadow-md" id="donation-form-heading">Make a Donation (Franc CFA)</h2>
            <form @submit.prevent="submitForm" class="space-y-6" aria-labelledby="donation-form-heading">
              <!-- Donation Amount (F CFA) -->
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2" for="amount">Donation Amount (F CFA) *</label>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-2">
                  <button
                    v-for="option in amountOptions"
                    :key="option"
                    type="button"
                    @click="form.amount = option"
                    class="px-4 py-2 rounded-lg bg-gray-700/50 hover:bg-gray-600/50 focus:ring-2 focus:ring-yellow-400 focus:outline-none transition-all"
                    :class="{ 'bg-yellow-400 text-gray-900 font-semibold': form.amount === option }"
                  >
                    {{ formatCfa(option) }}
                  </button>
                </div>
                <input
                  v-model="form.amount"
                  id="amount"
                  type="number"
                  required
                  min="100"
                  step="1"
                  class="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-white placeholder-gray-400"
                  placeholder="Enter amount in F CFA"
                  :aria-invalid="formErrors.amount ? 'true' : 'false'"
                  @input="clearError('amount')"
                />
                <p v-if="formErrors.amount" class="text-red-400 text-sm mt-1">{{ formErrors.amount }}</p>
              </div>

              <!-- Payment Method (Mobile Money) -->
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2" for="paymentMethod">Payment Method *</label>
                <select
                  v-model="form.paymentMethod"
                  id="paymentMethod"
                  required
                  class="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-white appearance-none"
                  :aria-invalid="formErrors.paymentMethod ? 'true' : 'false'"
                  @change="clearError('paymentMethod')"
                >
                  <option value="" disabled selected>Select a method</option>
                  <option value="orange_money">Orange Money</option>
                  <option value="mobile_money">Mobile Money</option>
                </select>
                <p v-if="formErrors.paymentMethod" class="text-red-400 text-sm mt-1">{{ formErrors.paymentMethod }}</p>
              </div>

              <!-- Donor Information -->
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2" for="name">Full Name *</label>
                <input
                  v-model="form.name"
                  id="name"
                  type="text"
                  required
                  class="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-white placeholder-gray-400"
                  placeholder="Enter your full name"
                  :aria-invalid="formErrors.name ? 'true' : 'false'"
                  @input="clearError('name')"
                />
                <p v-if="formErrors.name" class="text-red-400 text-sm mt-1">{{ formErrors.name }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2" for="email">Email *</label>
                <input
                  v-model="form.email"
                  id="email"
                  type="email"
                  required
                  class="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-white placeholder-gray-400"
                  placeholder="your.email@example.com"
                  :aria-invalid="formErrors.email ? 'true' : 'false'"
                  @input="clearError('email')"
                />
                <p v-if="formErrors.email" class="text-red-400 text-sm mt-1">{{ formErrors.email }}</p>
              </div>

              <!-- Phone Number for Mobile Money -->
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2" for="phone">Phone Number *</label>
                <input
                  v-model="form.phone"
                  id="phone"
                  type="tel"
                  required
                  class="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-white placeholder-gray-400"
                  placeholder="e.g., 0700000000"
                  :aria-invalid="formErrors.phone ? 'true' : 'false'"
                  @input="clearError('phone')"
                />
                <p v-if="formErrors.phone" class="text-red-400 text-sm mt-1">{{ formErrors.phone }}</p>
              </div>

              <!-- Optional Message -->
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2" for="message">Message (Optional)</label>
                <textarea
                  v-model="form.message"
                  id="message"
                  rows="3"
                  class="w-full px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-white placeholder-gray-400"
                  placeholder="Add a note with your donation"
                ></textarea>
              </div>

              <!-- Submit Button -->
              <div>
                <button
                  type="submit"
                  :disabled="isSubmitting"
                  class="w-full px-6 py-3 bg-yellow-400 hover:bg-yellow-500 disabled:opacity-50 disabled:cursor-not-allowed text-gray-900 font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg"
                >
                  <span v-if="!isSubmitting">Donate Now</span>
                  <span v-else class="flex items-center justify-center">
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-gray-900" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...
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
                  <p class="text-green-400 font-medium">Donation successful! Thank you for your support!</p>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue';

// Slideshow images from ContactPage.vue
// const images = ref([
//   { src: 'https://images.pexels.com/photos/6646917/pexels-photo-6646917.jpeg', loaded: false },
//   { src: 'https://images.pexels.com/photos/6646987/pexels-photo-6646987.jpeg', loaded: false },
//   { src: 'https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg', loaded: false },
// ]);

const imagesLoaded = ref(false);
const currentImageIndex = ref(0);

const changeImage = () => {
  currentImageIndex.value = (currentImageIndex.value + 1) % images.value.length;
};

onMounted(() => {
  let loadedCount = 0;
  images.value.forEach((image, index) => {
    const img = new Image();
    img.src = image.src;
    img.onload = () => {
      images.value[index].loaded = true;
      loadedCount++;
      if (loadedCount === images.value.length) imagesLoaded.value = true;
    };
    img.onerror = () => {
      images.value[index].loaded = false;
      loadedCount++;
      if (loadedCount === images.value.length) imagesLoaded.value = true;
    };
  });
  const intervalId = setInterval(changeImage, 5000);
  onUnmounted(() => clearInterval(intervalId));
});

// Form data and validation
const form = reactive({
  amount: '',
  paymentMethod: '',
  name: '',
  email: '',
  phone: '',
  message: '',
});

const amountOptions = [1000, 2000, 5000, 10000];

const formErrors = reactive({
  amount: '',
  paymentMethod: '',
  name: '',
  email: '',
  phone: '',
});

const isSubmitting = ref(false);
const showSuccess = ref(false);

const validateForm = () => {
  let isValid = true;
  formErrors.amount = Number(form.amount) >= 100 ? '' : 'Please enter an amount of at least 100 F CFA';
  formErrors.paymentMethod = form.paymentMethod ? '' : 'Please select a payment method';
  formErrors.name = form.name.trim() ? '' : 'Name is required';
  formErrors.email = form.email.trim() && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email) ? '' : 'Valid email is required';
  // Simple phone validation: 8-14 digits (adjust per country format)
  const digits = String(form.phone || '').replace(/\D/g, '');
  formErrors.phone = digits.length >= 8 && digits.length <= 14 ? '' : 'Enter a valid phone number (8-14 digits)';
  return !Object.values(formErrors).some(error => error);
};

const clearError = (field) => {
  formErrors[field] = '';
};

const submitForm = async () => {
  if (!validateForm()) return;

  isSubmitting.value = true;
  try {
    await new Promise(resolve => setTimeout(resolve, 2000));
    showSuccess.value = true;
    showSuccess.value = true;
    resetForm();
    setTimeout(() => showSuccess.value = false, 5000);
  } catch (error) {
    console.error('Error submitting donation:', error);
  } finally {
    isSubmitting.value = false;
  }
};

const resetForm = () => {
  Object.keys(form).forEach(key => form[key] = '');
  Object.keys(formErrors).forEach(key => formErrors[key] = '');
};

function formatCfa(value) {
  try {
    return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'XOF', maximumFractionDigits: 0 }).format(value);
  } catch {
    return `${value} F CFA`;
  }
}
</script>

<style scoped>
.min-h-screen {
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

/* Hover effects for buttons */
button:hover:not(:disabled) {
  transform: translateY(-2px);
}

/* Ensure readability */
.bg-gray-700\/50 {
  background-color: rgba(55, 65, 81, 0.5);
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