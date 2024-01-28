<script>
import { defineComponent, reactive } from "vue";
import TableLite from "vue3-table-lite";
import uploadImage from "../views/ImageUpload.vue";
import UploadImage from "@/views/ImageUpload.vue";
import router from "../router/router";
import axios from "axios";
import Filter from "@/views/Filter.vue";

localStorage.setItem('token', '0');
function converDatatoTableType(data){
  console.log(data);
  let result = [];

  for (let i = 0; i < data["titles"].length; i++){
    var image = new Image();
    image.src = data["pictures"][i];
    image.width = 200
    image.height = 100

    result.push({
      title: data["titles"][i],
      preview: image.outerHTML,
      colors: data["colors"][i],
      block_size: data["blockSizes"][i],
      progress: data["progresses"][i],
      creation_date: data["timestamps"][i]
    });
  }
  return result;
}


const getAPIData = async () => {
    const tokenLS = localStorage.getItem('token')
    if(!tokenLS) return

    let token = new FormData;
    token.append('token', tokenLS);

    let api_data = await axios
        .post(`http://localhost:5001/api/user_profile`, token)
        .catch(() => {
        })
        .then(async (res) => {
          console.log(res.data);
          return res.data;
        })

    return api_data;
  }

  let api_data = await getAPIData();
  console.log(api_data)

export default defineComponent({
    name: "App",
    components: {UploadImage, TableLite, Filter},
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
              display: (row) => {
                return (
                    row.preview
                )
              }
            },
            {
              label: "Colors",
              field: "colors",
              width: "15%",
              sortable: true,
            },
            {
              label: "Block size",
              field: "block_size",
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

        const doSearch = (offset, limit, order, sort) => {
          table.isLoading = true;
          setTimeout(() => {
            table.isReSearch = offset == undefined ? true : false;
            if (offset >= 10 || limit >= 20) {
              limit = 20;
            }
            if (sort == "asc") {
              table.rows = converDatatoTableType(api_data);
            } else {
              table.rows = converDatatoTableType(api_data);
            }
            table.totalRecordCount = 20;
            table.sortable.order = order;
            table.sortable.sort = sort;
          }, 600);
        };

        doSearch(0, api_data, "id", "asc");
        return {table, doSearch};
    },
  });
</script>

<template>
  <div class="left-bar">
  <p><img class="profile-pic" src="../../public/profile.jpg" alt="none">Jolyne Doe</p>
    <div class="import-buttons" style="display: flex; flex-direction: column;">
      <button class="btn" @click="">
        Скачать данные профиля
      </button>
      <button class="btn" @click="">
        Загрузить данные профиля
      </button>
      <router-link tag="button" class="view-button" to="/view">Посмотреть готовую мозаику</router-link>
      <router-link tag="button" class="view-button" to="/filter">Использовать фильтр</router-link>
      <uploadImage></uploadImage>
    </div>
  </div>
  <Filter @applyFilter="handleFilter"></Filter>
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

