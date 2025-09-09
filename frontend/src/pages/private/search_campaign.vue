<template>
  <div class="min-h-screen  text-white pt-20 ">
    <div class="container mx-auto px-4 py-8">
      <!-- Header Section -->
      <div class="text-center mb-10">
        <h1
          class="text-4xl font-bold mb-4 bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent">
          Find Campaigns to Support
        </h1>
        <p class="text-gray-400 max-w-2xl mx-auto">
          Discover meaningful causes and make a difference with your donation. Every contribution helps create positive
          change.
        </p>
      </div>

      <!-- Search and Filter Section -->
      <div class="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 mb-8 border border-gray-700">
        <div class="flex flex-col md:flex-row gap-4">
          <!-- Search Input -->
          <div class="flex-1 relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input v-model="searchQuery" type="text" placeholder="Search for campaigns, causes, or organizations..."
              class="w-full pl-10 pr-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 text-white placeholder-gray-400 transition-all" />
          </div>

          <!-- Filter Dropdown -->
          <div class="relative">
            <button @click="showFilters = !showFilters"
              class="flex items-center justify-between w-full md:w-48 px-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg hover:bg-gray-700 transition-colors -z-40">
              <span>Filter</span>
              <svg class="h-5 w-5 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <!-- Filter Dropdown Menu -->
            <div v-if="showFilters"
              class="absolute right-0 mt-2 w-48 bg-gray-800 border border-gray-700 rounded-lg shadow-xl z-10">
              <div class="p-4 space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-300 mb-1">Category</label>
                  <select v-model="filters.category"
                    class="w-full bg-gray-700 border border-gray-600 rounded-md px-3 py-2 text-white text-sm">
                    <option value="">All Categories</option>
                    <option v-for="category in categories" :key="category" :value="category">{{ category }}</option>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-300 mb-1">Status</label>
                  <select v-model="filters.status"
                    class="w-full bg-gray-700 border border-gray-600 rounded-md px-3 py-2 text-white text-sm">
                    <option value="">All Status</option>
                    <option value="active">Active</option>
                    <option value="upcoming">Upcoming</option>
                    <option value="completed">Completed</option>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-300 mb-1">Sort By</label>
                  <select v-model="filters.sortBy"
                    class="w-full bg-gray-700 border border-gray-600 rounded-md px-3 py-2 text-white text-sm">
                    <option value="newest">Newest</option>
                    <option value="popular">Most Popular</option>
                    <option value="ending">Ending Soon</option>
                    <option value="most-funded">Most Funded</option>
                  </select>
                </div>

                <button @click="applyFilters"
                  class="w-full bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 text-white py-2 rounded-md font-medium transition-all duration-200 transform hover:scale-105">
                  Apply Filters
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Active Filters -->
        <div v-if="hasActiveFilters" class="flex flex-wrap gap-2 mt-4">
          <span v-for="(value, key) in activeFilters" :key="key"
            class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-900/30 text-yellow-400">
            {{ value }}
            <button @click="removeFilter(key)" class="ml-1.5 rounded-full hover:bg-yellow-400 hover:text-yellow-900">
              <svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </span>
        </div>
      </div>

      <!-- Campaign Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        <div v-for="campaign in filteredCampaigns" :key="campaign.id"
          class="bg-gray-800/50 backdrop-blur-sm rounded-xl overflow-hidden border border-gray-700 hover:border-yellow-500/30 transition-all duration-300 hover:shadow-xl hover:scale-[1.02]">
          <!-- Campaign Image -->
          <div class="relative h-48 overflow-hidden">
            <img :src="campaign.image" :alt="campaign.title"
              class="w-full h-full object-cover transition-transform duration-500 hover:scale-110" />
            <div class="absolute top-4 left-4">
              <span class="px-3 py-1 rounded-full text-xs font-medium" :class="{
                'bg-green-900/70 text-green-300': campaign.status === 'active',
                'bg-blue-900/70 text-blue-300': campaign.status === 'upcoming',
                'bg-gray-900/70 text-gray-300': campaign.status === 'completed'
              }">
                {{ campaign.status }}
              </span>
            </div>
            <div class="absolute top-4 right-4">
              <button class="p-2 rounded-full bg-gray-900/70 text-gray-300 hover:text-yellow-400 transition-colors"
                @click="toggleFavorite(campaign.id)">
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"
                  :class="{ 'text-yellow-400 fill-yellow-400': campaign.isFavorite }">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Campaign Content -->
          <div class="p-6">
            <div class="flex items-center mb-3">
              <span class="text-xs font-medium px-2 py-1 rounded-md bg-yellow-900/30 text-yellow-400">
                {{ campaign.category }}
              </span>
              <span class="text-xs text-gray-400 ml-auto">
                {{ formatDate(campaign.endDate) }}
              </span>
            </div>

            <h3 class="text-xl font-bold mb-2 text-white hover:text-yellow-400 transition-colors cursor-pointer">
              {{ campaign.title }}
            </h3>
            <p class="text-gray-400 text-sm mb-4 line-clamp-2">
              {{ campaign.description }}
            </p>

            <!-- Progress Bar -->
            <div class="mb-4">
              <div class="flex justify-between text-sm mb-1">
                <span class="text-gray-300">Raised: {{ formatCurrency(campaign.raised) }}</span>
                <span class="text-gray-400">Goal: {{ formatCurrency(campaign.goal) }}</span>
              </div>
              <div class="w-full bg-gray-700 rounded-full h-2">
                <div class="bg-gradient-to-r from-yellow-500 to-orange-500 h-2 rounded-full"
                  :style="{ width: `${(campaign.raised / campaign.goal) * 100}%` }"></div>
              </div>
              <div class="text-xs text-gray-400 mt-1">
                {{ Math.round((campaign.raised / campaign.goal) * 100) }}% funded
              </div>
            </div>

            <!-- Donors -->
            <div class="flex items-center mb-4">
              <div class="flex -space-x-2">
                <div v-for="(donor, index) in campaign.donors" :key="index"
                  class="inline-block h-8 w-8 rounded-full border-2 border-gray-800 bg-gray-700"></div>
              </div>
              <span class="text-xs text-gray-400 ml-2">
                {{ campaign.donors.length }}+ supporters
              </span>
            </div>

            <!-- Action Button -->
            <router-link @click="donateToCampaign(campaign.id)"
            to="/admin/donate"
              class="w-full bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 text-white py-3 rounded-lg font-medium transition-all duration-200 transform hover:scale-105 shadow-lg"
              :disabled="campaign.status !== 'active'" :class="{
                'opacity-50 cursor-not-allowed': campaign.status !== 'active',
                'hover:scale-100': campaign.status !== 'active'
              }">
              {{ campaign.status === 'active' ? 'Donate Now' : campaign.status === 'upcoming' ? 'Notify Me' :
              'Completed' }}
            </router-link>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredCampaigns.length === 0" class="text-center py-16">
        <svg class="w-16 h-16 mx-auto text-gray-500 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 class="text-xl font-medium text-gray-300 mb-2">No campaigns found</h3>
        <p class="text-gray-500 mb-6">Try adjusting your search or filters to find what you're looking for.</p>
        <button @click="clearFilters"
          class="px-6 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors">
          Clear All Filters
        </button>
      </div>

      <!-- Pagination -->
      <div v-if="filteredCampaigns.length > 0" class="flex justify-center mt-8">
        <div class="flex items-center space-x-2">
          <button class="px-3 py-2 rounded-md bg-gray-800 text-gray-400 hover:text-white transition-colors"
            :disabled="currentPage === 1" :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }"
            @click="currentPage--">
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>

          <button v-for="page in totalPages" :key="page" @click="currentPage = page"
            class="px-4 py-2 rounded-md transition-colors" :class="{
              'bg-gradient-to-r from-yellow-500 to-orange-500 text-white': currentPage === page,
              'bg-gray-800 text-gray-400 hover:bg-gray-700': currentPage !== page
            }">
            {{ page }}
          </button>

          <button class="px-3 py-2 rounded-md bg-gray-800 text-gray-400 hover:text-white transition-colors"
            :disabled="currentPage === totalPages"
            :class="{ 'opacity-50 cursor-not-allowed': currentPage === totalPages }" @click="currentPage++">
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '../../lib/api'

// Campaigns fetched from backend (approved + active only)
const campaigns = ref([])
const loading = ref(false)
const error = ref('')

// Search and filter state
const searchQuery = ref('')
const showFilters = ref(false)
const currentPage = ref(1)
const itemsPerPage = 6

const filters = ref({
  category: '',
  status: '',
  sortBy: 'newest'
})

// Available categories
const categories = ref([
  'Education',
  'Healthcare',
  'Environment',
  'Animal Welfare',
  'Humanitarian',
  'Arts & Culture',
  'Community Development'
])

// Computed properties
const filteredCampaigns = computed(() => {
  let result = campaigns.value

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(campaign =>
      campaign.title.toLowerCase().includes(query) ||
      campaign.description.toLowerCase().includes(query) ||
      campaign.category.toLowerCase().includes(query)
    )
  }

  // Apply category filter
  if (filters.value.category) {
    result = result.filter(campaign => campaign.category === filters.value.category)
  }

  // Apply status filter
  if (filters.value.status) {
    result = result.filter(campaign => campaign.status === filters.value.status)
  }

  // Apply sorting
  switch (filters.value.sortBy) {
    case 'newest':
      result.sort((a, b) => new Date(b.endDate) - new Date(a.endDate))
      break
    case 'popular':
      result.sort((a, b) => b.donors.length - a.donors.length)
      break
    case 'ending':
      result.sort((a, b) => new Date(a.endDate) - new Date(b.endDate))
      break
    case 'most-funded':
      result.sort((a, b) => (b.raised / b.goal) - (a.raised / a.goal))
      break
  }

  // Apply pagination
  const startIndex = (currentPage.value - 1) * itemsPerPage
  return result.slice(startIndex, startIndex + itemsPerPage)
})

const totalPages = computed(() => {
  return Math.ceil(campaigns.value.length / itemsPerPage)
})

const hasActiveFilters = computed(() => {
  return filters.value.category || filters.value.status
})

const activeFilters = computed(() => {
  const active = {}
  if (filters.value.category) active.category = `Category: ${filters.value.category}`
  if (filters.value.status) active.status = `Status: ${filters.value.status}`
  return active
})

// Methods
const applyFilters = () => {
  showFilters.value = false
  currentPage.value = 1
}

const removeFilter = (filterKey) => {
  filters.value[filterKey] = ''
  currentPage.value = 1
}

const clearFilters = () => {
  filters.value = {
    category: '',
    status: '',
    sortBy: 'newest'
  }
  searchQuery.value = ''
  currentPage.value = 1
}

const toggleFavorite = (campaignId) => {
  const campaign = campaigns.value.find(c => c.id === campaignId)
  if (campaign) {
    campaign.isFavorite = !campaign.isFavorite
  }
}

const donateToCampaign = (campaignId) => {
  console.log(`Donating to campaign ${campaignId}`)
  // In a real app, this would navigate to the donation page
}

const formatCurrency = (amount) => {
  try {
    return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'XAF', maximumFractionDigits: 0 }).format(amount || 0)
  } catch {
    return `XAF ${Number(amount || 0).toLocaleString()}`
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

// Initialize
onMounted(async () => {
  await fetchApprovedCampaigns()
})

async function fetchApprovedCampaigns() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/campaigns/approved/')
    campaigns.value = (data || []).map((c) => ({
      id: c.id,
      title: c.title,
      description: c.description || '',
      category: 'General',
      status: 'active',
      goal: Number(c.target_amount || 0),
      raised: 0,
      image: 'https://generosityglobal.org/wp-content/uploads/2023/05/untitled-536-1-scaled.jpg',
      donors: [],
      endDate: c.end_date,
      isFavorite: false,
    }))
  } catch (e) {
    console.error('Failed to fetch approved campaigns', e?.response?.data || e)
    error.value = e?.response?.data?.detail || 'Failed to fetch campaigns.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  /* -webkit-line-clamp: 2; */
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Smooth transitions for all interactive elements */
button,
input,
select {
  transition: all 0.2s ease;
}

/* Hover effects for cards */
.hover-card {
  transition: all 0.3s ease;
}

.hover-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
}
</style>