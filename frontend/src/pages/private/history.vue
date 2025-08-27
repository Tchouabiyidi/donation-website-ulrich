<template>
  <div class="min-h-screen  text-gray-900 relative">
    <!-- Header Section -->
    <header class=" text-white py-6 px-4 sm:px-6">
      <div class="container mx-auto max-w-7xl">
        <h1 class="text-3xl sm:text-4xl font-bold text-yellow-400">Donation History</h1>
        <p class="text-sm text-gray-300 mt-1">View and manage your past contributions</p>
      </div>
    </header>

    <!-- Main Content -->
    <main class="py-10 px-4 sm:px-6">
      <div class="container mx-auto max-w-7xl">
        <!-- Filter Section -->
        <div class="mb-6 flex flex-col sm:flex-row justify-between items-center">
          <div class="mb-4 sm:mb-0">
            <label for="statusFilter" class="block text-sm font-medium text-gray-200 mr-2">Filter by Status:</label>
            <select
              v-model="filterStatus"
              id="statusFilter"
              class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400 focus:border-transparent text-gray-900"
              aria-label="Filter donations by status"
            >
              <option value="">All</option>
              <option value="Completed">Completed</option>
              <option value="Pending">Pending</option>
            </select>
          </div>
          <button
            @click="clearFilters"
            class="px-4 py-2 bg-yellow-400 hover:bg-yellow-500 text-gray-900 font-semibold rounded-lg transition-all duration-200 transform hover:scale-105"
          >
            Clear Filters
          </button>
        </div>

        <!-- Donation History Table -->
        <div class=" rounded-lg shadow-lg overflow-hidden">
          <table class="w-full text-white">
            <thead>
              <tr class="bg-gray-900">
                <th class="py-3 px-4 text-left text-sm font-semibold text-yellow-400">Date</th>
                <th class="py-3 px-4 text-left text-sm font-semibold text-yellow-400">Campaign</th>
                <th class="py-3 px-4 text-left text-sm font-semibold text-yellow-400">Amount</th>
                <th class="py-3 px-4 text-left text-sm font-semibold text-yellow-400">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(donation, index) in filteredDonations" :key="index" class="border-b border-gray-700 hover:bg-gray-700/50 transition-colors">
                <td class="py-3 px-4">{{ donation.date }}</td>
                <td class="py-3 px-4">{{ donation.campaign }}</td>
                <td class="py-3 px-4">{{ formatCurrency(donation.amount) }}</td>
                <td class="py-3 px-4">
                  <span :class="{
                    'text-green-400': donation.status === 'Completed',
                    'text-yellow-400': donation.status === 'Pending'
                  }">
                    {{ donation.status }}
                  </span>
                </td>
              </tr>
              <tr v-if="filteredDonations.length === 0" class="text-center py-4">
                <td colspan="4">No donations found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// Sample donation data
const donations = ref([
  { date: '2025-08-20', campaign: 'Water for Life', amount: 50.00, status: 'Completed' },
  { date: '2025-08-18', campaign: 'School Supplies Drive', amount: 25.00, status: 'Completed' },
  { date: '2025-08-15', campaign: 'Medical Aid', amount: 100.00, status: 'Pending' },
  { date: '2025-08-10', campaign: 'Food Relief', amount: 75.00, status: 'Completed' },
]);

// Filter state
const filterStatus = ref('');

// Computed filtered donations
const filteredDonations = computed(() => {
  if (!filterStatus.value) return donations.value;
  return donations.value.filter(d => d.status === filterStatus.value);
});

// Clear filters
const clearFilters = () => {
  filterStatus.value = '';
};

// Currency: XAF with no decimals
function formatCurrency(value) {
  try {
    return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'XAF', maximumFractionDigits: 0 }).format(value || 0)
  } catch {
    return `XAF ${Number(value || 0).toLocaleString()}`
  }
}
</script>

<style scoped>
/* Enhanced focus styles for accessibility */
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
button:hover {
  transform: translateY(-2px);
}

/* Table styling */
table {
  border-collapse: separate;
  border-spacing: 0;
}

th {
  position: sticky;
  top: 0;
  z-index: 10;
}

tr:last-child {
  border-bottom: none;
}

td, th {
  vertical-align: middle;
}
</style>