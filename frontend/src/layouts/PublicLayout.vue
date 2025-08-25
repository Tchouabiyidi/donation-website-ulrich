<template>
  <div class="min-h-screen flex flex-col relative overflow-hidden bg-black">
    <!-- Main content with semi-transparent backgrounds for header/footer, transparent for body -->
    <public-header class="relative z-20 backdrop-blur-sm"></public-header>
    <Body class="flex-1 relative z-10"></Body>
    <public-footer class="relative z-20 backdrop-blur-sm"></public-footer>
  </div>
</template>

<script setup>
import PublicHeader from "../components/public/PublicHeader.vue";
import PublicFooter from "../components/public/PublicFooter.vue";
import Body from "../components/public/Body.vue";
</script>

<style scoped>
/* Ensure the layout has proper styling */
:deep(.min-h-screen) {
  margin: 0;
  padding: 0;
  height: 100%;
}
</style>