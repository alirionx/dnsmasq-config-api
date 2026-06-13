<script setup>
import { RouterLink, RouterView } from 'vue-router'
import SystemMessage from './components/SystemMessage.vue'

import { useHostRecordsStore } from '@/stores/host-records'
const hostRecordsStore = useHostRecordsStore()

</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
    <div class="container-fluid">
      <div class="navbar-brand">DNSMASQ Config WebUI</div>
      <div class="collapse navbar-collapse" id="navbarNav">
        <div class="navbar-nav">
          <RouterLink class="nav-link" to="/">Home</RouterLink>
          <RouterLink class="nav-link" to="/host-records">Host Records</RouterLink>
          <RouterLink class="nav-link" to="/dhcp-ranges">DHCP Ranges</RouterLink>
        </div>
      </div>
    </div>
  </nav>
  <main>
    <RouterView />
    <SystemMessage v-if="hostRecordsStore.systemMessage.isActive"/>
  </main>
</template>

<style scoped>
main {
  padding-top: 70px;
}
.navbar-brand{
  padding: 0px 40px 0px 20px;
}
.nav-link{
  min-width: 140px;
  text-align: center;
}
</style>
