<template>
  <div class="left-bar">
    <p><img class="profile-pic" src="../../public/profile.jpg" alt="none">Jolyne Doe</p>
    <Filter @applyFilter="handleFilter"></Filter>
    <table-lite
        :is-loading="table.isLoading"
        :columns="table.columns"
        :rows="table.filteredRows"
        :total="table.totalRecordCount"
        :sortable="table.sortable"
        :messages="table.messages"
        @do-search="doSearch"
        @is-finished="table.isLoading = false"
    ></table-lite>
    <uploadImage></uploadImage>
  </div>
</template>

<script>
import TableLite from "vue3-table-lite";
import Filter from "@/views/Filter.vue";
import UploadImage from "@/views/ImageUpload.vue";

export default {
  data() {
    return {
      table: {
        isLoading: false,
        columns: [],
        rows: [],
        filteredRows: [],
        totalRecordCount: 0,
        sortable: {
          order: "id",
          sort: "asc",
        },
      },
      api_data: null,
    };
  },
  methods: {
    converDatatoTableType(data) {
    },
    async getAPIData() {
    },
    async doSearch(offset, limit, order, sort) {
    },
    handleFilter(filterOptions) {
      const filterText = filterOptions.name.toLowerCase();
      this.table.filteredRows = this.table.rows.filter((row) => {
        return row.title.toLowerCase().includes(filterText);
      });
    },
  },
  async created() {
    this.api_data = await this.getAPIData();
    this.table.rows = this.converDatatoTableType(this.api_data);
    this.table.filteredRows = this.table.rows;
  },
  components: {
    UploadImage,
    TableLite,
    Filter,
  },
};
</script>

<style>
.vtl-card{
  background: white;
  width: 80vw;
  height: 100vh;
  color: #212529;
  border-collapse: collapse;
  padding: 0;
  margin-left: 30px;
  text-align: center;
}
p{
  margin-left: 384px;
  margin-top: 20px;
  width: 200px;
  font-size: large;
  color: black;
  border-bottom: solid 2px;
}
.vtl-row{ background-color: white; }
.vtl-thead-th input{ background-color: #fff; }
.vtl tr { background-color: white; }
.vtl-tbody-checkbox { color-scheme: auto; }
.vtl-paging { color: black; }
.vtl-paging-pagination-page-li { margin-top: 0px !important; }
.vtl select { -webkit-appearance: auto; }

.left-bar{
  height: 100vh;
  width: 250vh;
  background: rgba(158, 152, 172);
  position: absolute;
  right: 0;
}
.profile-pic{
  width: 50px;
  height: 50px;
  border-radius: 100%;
  border: solid 2px;
  margin-left: 5px;
}
.import-buttons {
  width: 300px;
  margin-left: 320px;
}
.import-buttons button{
  display: block;
  margin-bottom: 10px;
}
.btn{
  display: inline-block;
  text-align: center;
  float: left;
}
.view-button{
  margin-bottom: 10px;
  border-radius: 3px;
  background-color: white;
  text-decoration-color: black;
  text-align: center;
  color: black;
  font: inherit;
}
</style>