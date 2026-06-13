import { defineStore } from 'pinia'
import axios from 'axios'

export const useHostRecordsStore = defineStore('hostRecords', {
  state: () => ({
    records: [],

    systemMessage:{
      isActive: false,
      type: null,
      message: "",
      callback: ()=>{}
    }
  }),
  actions: {
    resetSystemMessage(){
      this.systemMessage = {
        isActive: false,
        type: null,
        message: "",
        callback: ()=>{}
      }
    },

    fetchHostRecords() {
      axios.get('/api/dns/host-records')
      .then(response => {
        this.records = Array.isArray(response.data) ? response.data : []
      })
      .catch(error => {
        this.systemMessage = {
          isActive: true,
          type: "information",
          message: `fetchHostRecords: ${error} | ${JSON.stringify(error.response.data, null, 2)}`
        }
      })
      .finally(() => {
        console.log('fetchHostRecords executed');
      });
    
    },

    addHostRecord(item){
      axios.post(`/api/dns/host-record`, item)
      .then(response => {
        this.records.push(response.data);
      })
      .catch(error => {
        this.systemMessage = {
          isActive: true,
          type: "information",
          message: `addHostRecord: ${error} | ${JSON.stringify(error.response.data, null, 2)}`
        }
      })
      .finally(() => {
        console.log('addHostRecord executed');
      });
    },

    updateHostRecord(idx, item){
      // console.log(item)
      axios.put(`/api/dns/host-record/${this.records[idx].id}`, item)
      .then(response => {
        this.records[idx] = item;
      })
      .catch(error => {
        this.systemMessage = {
          isActive: true,
          type: "information",
          message: `updateHostRecord: ${error} | ${JSON.stringify(error.response.data, null, 2)}`
        }
      })
      .finally(() => {
        console.log('updateHostRecord executed');
      });
    },

    callDelete(idx){
      this.systemMessage = {
        isActive: true,
        type: "confirmation",
        message: `Do you really want to delete host record: ${JSON.stringify(this.records[idx])}`,
        callback: ()=>{ this.deleteHostRecord(idx) }
      }
    },

    deleteHostRecord(idx){
      axios.delete(`/api/dns/host-record/${this.records[idx].id}`)
      .then(response => {
        this.records.splice(idx, 1);
      })
      .catch(error => {
        this.systemMessage = {
          isActive: true,
          type: "information",
          message: `deleteHostRecord: ${error} | ${JSON.stringify(error.response.data)}`
        }
      })
      .finally(() => {
        this.resetSystemMessage()
        console.log('deleteHostRecord executed');
      });
    },

    systemdAction(action){
      axios.post(`/api/dns/systemd?action=${action}`)
      .then(response => {
      })
      .catch(error => {
        this.systemMessage = {
          isActive: true,
          type: "information",
          message: `systemdAction: ${error} | ${JSON.stringify(error.response.data)}`
        }
      })
      .finally(() => {
        console.log('systemdAction executed');
      });
    }

  },

})
