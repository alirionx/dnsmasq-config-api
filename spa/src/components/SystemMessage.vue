<script setup>
import { storeToRefs } from 'pinia'
import { useHostRecordsStore } from '@/stores/host-records'

const hostRecordsStore = useHostRecordsStore()
const { systemMessage } = storeToRefs(hostRecordsStore)
</script>


<template>
  <div class="blender">
    <div class="card shadow w-100" style="max-width: 600px;">
      <div class="card-body">
        <h5 class="card-title mb-4">System Message</h5>
          <p class="card-text">{{systemMessage.message}}</p>
          <div class="d-flex gap-4 mt-4" v-if="systemMessage.type == 'information'">
            <button 
              type="button" 
              class="btn btn-primary"
              @click="hostRecordsStore.resetSystemMessage">Ok</button>
          </div>
          <div class="d-flex gap-4 mt-4" v-if="systemMessage.type == 'confirmation'">
            <button 
              type="button" 
              class="btn btn-primary"
              @click="systemMessage.callback">Ok</button>
            <button 
              type="button" 
              class="btn btn-secondary" 
              @click="hostRecordsStore.resetSystemMessage">Cancel</button>
          </div>
      </div>
    </div>
  </div>     
</template>


<style scoped>
.btn{
  min-width: 100px;
}
</style>