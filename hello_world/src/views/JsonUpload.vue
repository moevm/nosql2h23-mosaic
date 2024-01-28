<template>
  <div class="d-flex flex-row align-items-center" style="height: 100%;">
    <div class="card d-flex" style="width: 100%">
      <div class="card-body">
        <button class="btn btn-primary btn-block mt-4" @click="openUploadDialog">
          Загрузить данные профиля
          <input type="file" accept="application/JSON, application/json" ref="fileInput" @change="onFileChange" style="display: none"/>
        </button>
        <div v-if="uploading" class="upload-overlay">
          <span>Загрузка...</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import router from "@/router/router";
import {useField} from "vee-validate";

export default {
  name: "uploadJson",
  props: ["result", "sizes"],
  data() {
    return {
      files: [],
      image: null,
      uploading: false,
      fileSelected: false,
    };
  },
  methods: {
    onFileChange(e) {
      const files = e.target.files || e.dataTransfer.files;
      if (files.length) {
        this.fileSelected = true;
      }
    },
    openUploadDialog() {
      if (this.fileSelected) {
      } else {

        this.$refs.fileInput.click();
      }
    },
  },
// const picture = useField('picture')
// const title = useField('title')
// const upload = async(title, picture) => {
//   let data = new FormData();
//   let that = this;
//   data.append("title", title);
//   data.append("token", localStorage.getItem('token'));
//
//   await axios
//       .post(`http://localhost:5001/api/add_picture`, data)
//       .then(async (res) => {
//         await router.push({ path: "/home"});
//       })
//

}
</script>

<style scoped>
.btn{
  width: 300px;
}
</style>
