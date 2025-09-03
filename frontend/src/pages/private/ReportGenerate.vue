<template>
  <div class="min-h-screen  text-white pt-20 px-6">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-extrabold tracking-tight">Generate Reports</h1>
        <p class="text-gray-400 mt-1">Build financial and impact reports for your campaigns.</p>
      </div>

      <!-- Controls -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Filters Card -->
        <div class="lg:col-span-2">
          <div class="bg-gray-900/60 border border-gray-800 rounded-xl p-5">
            <h2 class="text-lg font-semibold mb-4">Filters</h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Date Range -->
              <div class="space-y-2">
                <label class="text-sm text-gray-300">Start Date</label>
                <input type="date" v-model="filters.start" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200 focus:outline-none focus:ring-2 focus:ring-yellow-500/60" />
              </div>
              <div class="space-y-2">
                <label class="text-sm text-gray-300">End Date</label>
                <input type="date" v-model="filters.end" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200 focus:outline-none focus:ring-2 focus:ring-yellow-500/60" />
              </div>

              <!-- Campaign -->
              <div class="space-y-2">
                <label class="text-sm text-gray-300">Campaign</label>
                <select v-model="filters.campaignId" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200 focus:outline-none focus:ring-2 focus:ring-yellow-500/60">
                  <option :value="null">All campaigns</option>
                  <option v-for="c in campaigns" :key="c.id" :value="c.id">{{ c.name }}</option>
                </select>
              </div>

              <!-- Report Type -->
              <div class="space-y-2">
                <label class="text-sm text-gray-300">Report Type</label>
                <div class="flex flex-wrap gap-3 bg-gray-800 border border-gray-700 rounded-lg px-3 py-3">
                  <label class="inline-flex items-center gap-2 text-sm text-gray-300">
                    <input type="checkbox" v-model="reportTypes.financial" class="accent-yellow-500" />
                    Financial
                  </label>
                  <label class="inline-flex items-center gap-2 text-sm text-gray-300">
                    <input type="checkbox" v-model="reportTypes.donations" class="accent-yellow-500" />
                    Donations
                  </label>
                  <label class="inline-flex items-center gap-2 text-sm text-gray-300">
                    <input type="checkbox" v-model="reportTypes.impact" class="accent-yellow-500" />
                    Impact
                  </label>
                </div>
              </div>
            </div>

            <!-- Actions -->
            <div class="mt-5 flex items-center gap-3">
              <button @click="generate" class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-yellow-400 to-orange-500 text-black font-semibold shadow hover:opacity-95 active:opacity-90">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                Generate
              </button>
              <button @click="resetFilters" class="px-4 py-2 rounded-lg border border-gray-700 text-gray-300 hover:bg-gray-800">Reset</button>
            </div>
          </div>
        </div>

        <!-- Quick Summary Card -->
        <div>
          <div class="bg-gray-900/60 border border-gray-800 rounded-xl p-5 h-full">
            <h2 class="text-lg font-semibold mb-4">Summary</h2>
            <div class="grid grid-cols-2 gap-4">
              <div class="p-3 rounded-lg bg-gray-800 border border-gray-700">
                <p class="text-xs text-gray-400">Total Donations</p>
                <p class="text-xl font-bold">{{ summary.totalDonations | currency }}</p>
              </div>
              <div class="p-3 rounded-lg bg-gray-800 border border-gray-700">
                <p class="text-xs text-gray-400">Transactions</p>
                <p class="text-xl font-bold">{{ summary.transactions }}</p>
              </div>
              <div class="p-3 rounded-lg bg-gray-800 border border-gray-700">
                <p class="text-xs text-gray-400">Avg. Donation</p>
                <p class="text-xl font-bold">{{ summary.avgDonation | currency }}</p>
              </div>
              <div class="p-3 rounded-lg bg-gray-800 border border-gray-700">
                <p class="text-xs text-gray-400">Campaigns</p>
                <p class="text-xl font-bold">{{ summary.campaignCount }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Results / Preview -->
      <div class="mt-6 bg-gray-900/60 border border-gray-800 rounded-xl">
        <div class="flex items-center justify-between px-5 py-4 border-b border-gray-800">
          <h2 class="text-lg font-semibold">Report Preview</h2>
          <div class="flex items-center gap-2">
            <button @click="exportCSV" class="px-3 py-1.5 rounded-lg bg-gray-800 border border-gray-700 text-gray-300 hover:bg-gray-700">Export CSV</button>
            <button @click="exportPDF" class="px-3 py-1.5 rounded-lg bg-gray-800 border border-gray-700 text-gray-300 hover:bg-gray-700">Export PDF</button>
          </div>
        </div>

        <div class="p-5 overflow-x-auto">
          <div v-if="loading" class="text-gray-400">Generating report…</div>
          <div v-else-if="!previewRows.length" class="text-gray-500">No data. Adjust filters and click Generate.</div>

          <table v-else class="min-w-full text-sm">
            <thead>
              <tr class="text-left text-gray-300">
                <th class="py-2 pr-4">Date</th>
                <th class="py-2 pr-4">Campaign</th>
                <th class="py-2 pr-4">Donor</th>
                <th class="py-2 pr-4">Amount</th>
                <th class="py-2 pr-4">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in previewRows" :key="row.id" class="border-t border-gray-800 hover:bg-gray-800/40">
                <td class="py-2 pr-4 text-gray-300">{{ row.date }}</td>
                <td class="py-2 pr-4">{{ row.campaign }}</td>
                <td class="py-2 pr-4">{{ row.donor }}</td>
                <td class="py-2 pr-4 font-semibold">{{ row.amount | currency }}</td>
                <td class="py-2 pr-4">
                  <span class="px-2 py-0.5 text-xs rounded-full"
                        :class="row.status === 'Completed' ? 'bg-green-900/40 text-green-300 border border-green-800' : 'bg-yellow-900/40 text-yellow-300 border border-yellow-800'">
                    {{ row.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'

// Mock campaigns and transactions
const campaigns = [
  { id: 1, name: 'Clean Water Initiative' },
  { id: 2, name: 'School Supplies Drive' },
  { id: 3, name: 'Medical Aid Fund' },
]

const allRows = ref([
  { id: 1, date: '2025-08-01', campaignId: 1, campaign: 'Clean Water Initiative', donor: 'tchoua biyidi', amount: 1000, status: 'Completed' },
  { id: 2, date: '2025-08-03', campaignId: 2, campaign: 'School Supplies Drive', donor: 'tekam urich', amount: 2000, status: 'Pending' },
  { id: 3, date: '2025-08-05', campaignId: 3, campaign: 'Medical Aid Fund', donor: 'takeng yvan', amount: 500, status: 'Completed' },
  { id: 4, date: '2025-08-05', campaignId: 1, campaign: 'Clean Water Initiative', donor: 'pharel', amount: 3000, status: 'Completed' },
])

const filters = reactive({
  start: '',
  end: '',
  campaignId: null,
})

const reportTypes = reactive({ financial: true, donations: true, impact: false })
const loading = ref(false)

const previewRows = ref([])

const summary = computed(() => {
  const rows = previewRows.value
  const transactions = rows.length
  const total = rows.reduce((s, r) => s + r.amount, 0)
  const avg = transactions ? total / transactions : 0
  const campaignIds = new Set(rows.map(r => r.campaignId))
  return {
    totalDonations: total,
    transactions,
    avgDonation: avg,
    campaignCount: campaignIds.size,
  }
})

function generate() {
  loading.value = true
  setTimeout(() => {
    // Filter by dates and campaign
    const start = filters.start ? new Date(filters.start) : null
    const end = filters.end ? new Date(filters.end) : null
    const filtered = allRows.value.filter(r => {
      const d = new Date(r.date)
      const inStart = start ? d >= start : true
      const inEnd = end ? d <= end : true
      const inCampaign = filters.campaignId ? r.campaignId === filters.campaignId : true
      return inStart && inEnd && inCampaign
    })

    // Simulate reportTypes toggles by including/excluding pending rows, etc.
    let rows = filtered
    if (!reportTypes.donations) rows = []

    previewRows.value = rows
    loading.value = false
  }, 400)
}

function resetFilters() {
  filters.start = ''
  filters.end = ''
  filters.campaignId = null
  reportTypes.financial = true
  reportTypes.donations = true
  reportTypes.impact = false
  previewRows.value = []
}

function exportCSV() {
  // Simple CSV export stub
  if (!previewRows.value.length) return
  const header = ['Date', 'Campaign', 'Donor', 'Amount', 'Status']
  const rows = previewRows.value.map(r => [r.date, r.campaign, r.donor, r.amount, r.status])
  const csv = [header, ...rows].map(r => r.join(',')).join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'report.csv'
  a.click()
  URL.revokeObjectURL(url)
}

async function exportPDF() {
  if (!previewRows.value.length) return

  try {
    // Dynamic local imports ensure this works in production bundles
    const { jsPDF } = await import('jspdf')
    const autoTable = (await import('jspdf-autotable')).default

    const doc = new jsPDF('p', 'pt', 'a4')

    // Header
    const title = 'Donation Report'
    doc.setFont('helvetica', 'bold')
    doc.setFontSize(16)
    doc.text(title, 40, 40)

    // Subheader: generated at and filters
    doc.setFont('helvetica', 'normal')
    doc.setFontSize(10)
    const generatedAt = new Date().toLocaleString()
    const filterLines = [
      `Generated: ${generatedAt}`,
      `Date Range: ${filters.start || '—'} to ${filters.end || '—'}`,
      `Campaign: ${filters.campaignId ? (campaigns.find(c => c.id === filters.campaignId)?.name || filters.campaignId) : 'All campaigns'}`
    ]
    let cursorY = 60
    filterLines.forEach(line => {
      doc.text(line, 40, cursorY)
      cursorY += 14
    })

    // Summary block
    const sum = summary.value
    const sumLines = [
      `Total Donations: ${currency(sum.totalDonations)}`,
      `Transactions: ${sum.transactions}`,
      `Avg. Donation: ${currency(sum.avgDonation)}`,
      `Campaigns: ${sum.campaignCount}`
    ]
    cursorY += 6
    doc.setFont('helvetica', 'bold')
    doc.text('Summary', 40, cursorY)
    doc.setFont('helvetica', 'normal')
    cursorY += 14
    sumLines.forEach(line => {
      doc.text(line, 40, cursorY)
      cursorY += 14
    })

    // Table
    const columns = [
      { header: 'Date', dataKey: 'date' },
      { header: 'Campaign', dataKey: 'campaign' },
      { header: 'Donor', dataKey: 'donor' },
      { header: 'Amount', dataKey: 'amount' },
      { header: 'Status', dataKey: 'status' }
    ]
    const rows = previewRows.value.map(r => ({
      date: r.date,
      campaign: r.campaign,
      donor: r.donor,
      amount: currency(r.amount),
      status: r.status
    }))

    const startY = cursorY + 10
    // Use ESM API: call the imported autoTable helper
    autoTable(doc, {
      startY,
      headStyles: { fillColor: [30, 30, 30], textColor: 255 },
      styles: { font: 'helvetica', fontSize: 9 },
      theme: 'grid',
      columns,
      body: rows,
      margin: { left: 40, right: 40 }
    })

    doc.save('donation-report.pdf')
  } catch (e) {
    console.error('PDF export error:', e)
    alert('Failed to generate PDF report. See console for details.')
  }
}

// Currency formatter filter-like helper
function currency(value) {
  try {
    return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'XAF', maximumFractionDigits: 0 }).format(value || 0)
  } catch {
    return `XAF ${Number(value || 0).toLocaleString()}`
  }
}
</script>

<script>
// Provide a simple filter syntax in templates
export default {
  filters: {
    currency(val) {
      try {
        return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'XAF', maximumFractionDigits: 0 }).format(val || 0)
      } catch {
        return `XAF ${Number(val || 0).toLocaleString()}`
      }
    }
  }
}
</script>

<style scoped>
/* Subtle divider matching dark theme */
table thead th { border-bottom: 1px solid rgba(75,85,99,0.5); }
</style>