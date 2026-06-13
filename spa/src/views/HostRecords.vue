<template>
  <div class="view-frame py-4" >
    <div class="card shadow-sm">
      <div class="card-body">
        <h3 class="mb-4">Host Records</h3>
        <div class="table-responsive">
          <table class="table table-striped table-bordered align-middle mb-0">
            <thead class="table-dark">
              <tr>
                <th v-for="column in columns" :key="column.key">{{ column.name }}</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(record, ridx) in hostRecordsStore.records" :key="record.id">
                <td v-for="column in columns" :key="column.key">
                  <template v-if="Array.isArray(record[column.key])">
                    <div v-for="(entry, eidx) in record[column.key]" :key="eidx">
                      - {{ entry }}
                    </div>
                  </template>
                  <template v-else>
                    {{ record[column.key] }}
                  </template>
                </td>
                <td>
                  <button 
                    @click="activeAddEdit=true; idxAddEdit=ridx"
                    type="button" 
                    class="btn btn-sm btn-outline-primary">
                    <i class="bi bi-pencil-square"></i>
                  </button>
                  <button 
                    @click="hostRecordsStore.callDelete(ridx)"
                    type="button" 
                    class="btn btn-sm btn-outline-danger">
                    <i class="bi bi-trash3"></i>
                  </button>
                </td>
              </tr>
              <tr>
                <td :colspan="columns.length" />
                <td>
                  <button 
                    @click="activeAddEdit=true"
                    type="button" 
                    class="btn btn-sm btn-primary ">
                    <i class="bi bi-plus-square"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="mt-4 d-flex align-items-center gap-3">
          <select class="form-select-sm w-auto" style="min-width: 160px;" v-model="systemdAction">
            <option value="enable">enable</option>
            <option value="disable">disable</option>
            <option value="start">start</option>
            <option value="stop">stop</option>
            <option value="reload">reload</option>
            <option value="restart">restart</option>
          </select>
          <button 
            class="btn btn-sm btn-primary"   
            style="min-width: 160px;"
            type="button"      
            @click="hostRecordsStore.systemdAction(systemdAction)"
          >{{systemdAction}} - DNSMasq</button>
        </div>

      </div>
    </div>

    <AddEditHostRecord v-if="activeAddEdit" :idx="idxAddEdit" :reset="reset" />

  </div>
</template>

<script>
import { useHostRecordsStore } from '@/stores/host-records'
import AddEditHostRecord from '../components/AddEditHostRecord.vue'

export default {
  // ----------------------------------------
  components:{
    AddEditHostRecord
  },

  // ----------------------------------------
  data() {
    return {
      hostRecordsStore: useHostRecordsStore(),
      columns: [
        {
          key: "hostnames",
          name: "Hostnames"
        },
        {
          key: "ipv4_address",
          name: "IPv4 Address"
        },
        {
          key: "ipv6_address",
          name: "IPv6 Address"
        },
        {
          key: "id",
          name: "Id"
        }
      ],
      activeAddEdit: null,
      idxAddEdit: null,
      systemdAction: "restart"
    }
  },

  // ----------------------------------------
  methods: {
    reset(){
      this.activeAddEdit = null;
      this.idxAddEdit = null;
    }

  },

  // ----------------------------------------
  mounted() {
    if (this.hostRecordsStore.records.length === 0) {
      this.hostRecordsStore.fetchHostRecords()
    }
  }

  // ----------------------------------------
}
</script>


<style scoped>
table td{
  vertical-align: top;
}
table th:last-child, table td:last-child{
  text-align: center;
  max-width: 120px;
  white-space: nowrap;
}

table .btn-sm{
  margin: -4px 4px -4px 4px;
}

</style>