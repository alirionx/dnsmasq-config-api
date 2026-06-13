<template>

  <div class="blender">
    <div class="card shadow w-100" style="max-width: 600px;">
      <div class="card-body">
        <h5 class="card-title mb-4">{{type}} Host Record</h5>
        <form @submit.prevent="submit">
          <div class="mb-3" v-if="this.idx !== null">
            <label class="form-label">ID</label>
            <input type="text" class="form-control" :value="record.id"  disabled />
          </div>
          <div class="mb-3">
            <label class="form-label" :class="{ 'is-invalid': !hostNamesValid }">Hostnames</label>
            <div v-for="(hn, hnidx) in record.hostnames" class="d-flex gap-2 mb-2">
              <input type="text" class="form-control" v-model="record.hostnames[hnidx]" />
              <button type="button" class="btn btn-sm btn-outline-danger" @click="remove_hostname(hnidx)">
                <i class="bi bi-dash-square"></i>
              </button>
            </div>
            <div class="d-flex justify-content-end" >
              <button type="button" class="btn btn-sm btn-outline-primary" @click="add_hostname">
                <i class="bi bi-plus-square"></i>
              </button>
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">IPv4 Address</label>
            <input 
              type="text" 
              class="form-control" 
              :class="{ 'is-invalid': !ipValid }"
              v-model="record.ipv4_address" />
          </div>
          <div class="mb-3">
            <label class="form-label">IPv6 Address</label>
            <input 
              type="text" 
              class="form-control" 
              :class="{ 'is-invalid': !ipValid }"
              @click="this.ipValid = true"
              v-model="record.ipv6_address" />
          </div>
          <div class="d-flex gap-4 mt-4">
            <button type="submit" class="btn btn-primary">Submit</button>
            <button type="button" class="btn btn-secondary" @click="reset">Cancel</button>
          </div>
      
        </form>
      </div>
    </div>
  </div>     
</template>



<script>
import { useHostRecordsStore } from '@/stores/host-records'

export default {
  // ----------------------------------------
  props:{
    idx: Number,
    reset: Function
  },
  // ----------------------------------------
  data() {
    return {
      hostRecordsStore: useHostRecordsStore(),
      type: "",
      record: {
        hostnames: [],
        ipv4_address: "",
        ipv6_address: ""
      },
      hostNamesValid: true,
      ipValid: true,
    };
  },

  // ----------------------------------------
  methods: {

    remove_hostname(hnidx){
      this.record.hostnames.splice(hnidx, 1)
    },

    add_hostname(){
      if(this.record.hostnames.at(-1) == ""){
        return
      }
      this.hostNamesValid = true;
      this.record.hostnames.push("")
    },

    submit(){
      if(this.record.hostnames.length===0){
        this.hostNamesValid = false;
        return
      }
      if(this.record.hostnames.at(-1) == ""){
        this.hostNamesValid = false;
        return
      }
      if(!this.record.ipv4_address && !this.record.ipv4_address){
        this.ipValid = false;
        return
      }

      if(this.record.ipv4_address == ""){
        this.record.ipv4_address = null
      }
      if(this.record.ipv6_address == ""){
        this.record.ipv6_address = null
      }

      if(this.idx == null){
        this.hostRecordsStore.addHostRecord(this.record)
      }
      else{
        this.hostRecordsStore.updateHostRecord(this.idx, this.record)
      }  
      
      this.reset()
    }

  },
  
  // ----------------------------------------
  mounted() {
    if(this.idx == null){
      this.type = "Add"
    }
    else{
      this.type = "Edit"
      this.record = JSON.parse(JSON.stringify(this.hostRecordsStore.records[this.idx]))
    }
  }
};

</script>



<style scoped>
.modal-body p { margin-bottom: .5rem }

.btn-primary, .btn-secondary{
  min-width: 100px;
}
</style>