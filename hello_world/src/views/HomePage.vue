<script>
import { defineComponent, reactive } from "vue";
import TableLite from "vue3-table-lite";

// Fake Data for 'asc' sortable
const sampleData1 = (offst, limit) => {
  offst = offst + 1;
  let data = [];
  for (let i = offst; i <= limit; i++) {
    data.push({
      title: i,
      preview: "TEST" + i,
    });
  }
  return data;
};

// Fake Data for 'desc' sortable
const sampleData2 = (offst, limit) => {
  let data = [];
  for (let i = limit; i > offst; i--) {
    data.push({
      title: i,
      preview: "TEST" + i,
    });
  }
  return data;
};

export default defineComponent({
  name: "App",
  components: { TableLite },
  setup() {
    // Table config
    const table = reactive({
      isLoading: false,
      columns: [
        {
          label: "Title",
          field: "title",
          width: "3%",
          sortable: true,
          isKey: true,
        },
        {
          label: "Preview",
          field: "preview",
          width: "10%",
          sortable: true,
        },
        {
          label: "Colors",
          field: "colors",
          width: "15%",
          sortable: true,
        },
        {
          label: "Shapes",
          field: "shapes",
          width: "15%",
          sortable: true,
        },
        {
          label: "Progress",
          field: "progress",
          width: "15%",
          sortable: true,
        },
        {
          label: "Creation date",
          field: "creation_date",
          width: "15%",
          sortable: true,
        },
        {
          label: "Last change",
          field: "last_change",
          width: "15%",
          sortable: true,
        },
      ],
      rows: [],
      totalRecordCount: 0,
      sortable: {
        order: "id",
        sort: "asc",
      },
    });

    /**
     * Search Event
     */
    const doSearch = (offset, limit, order, sort) => {
      table.isLoading = true;
      setTimeout(() => {
        table.isReSearch = offset == undefined ? true : false;
        if (offset >= 10 || limit >= 20) {
          limit = 20;
        }
        if (sort == "asc") {
          table.rows = sampleData1(offset, limit);
        } else {
          table.rows = sampleData2(offset, limit);
        }
        table.totalRecordCount = 20;
        table.sortable.order = order;
        table.sortable.sort = sort;
      }, 600);
    };

    // First get data
    doSearch(0, 10, "id", "asc");

    return {
      table,
      doSearch,
    };
  },
});
</script>

<template>
  <div class="left-bar">

  </div>
  <table-lite
      :is-loading="table.isLoading"
      :columns="table.columns"
      :rows="table.rows"
      :total="table.totalRecordCount"
      :sortable="table.sortable"
      :messages="table.messages"
      @do-search="doSearch"
      @is-finished="table.isLoading = false"
  ></table-lite>
</template>

<style>
.vtl-card{
  background: white;
  width: 89vw;
  height: 100vh;
  color: #212529;
  border-collapse: collapse;
  padding: 0;
  margin-left: 30px;
  text-align: center;
}
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
</style>

