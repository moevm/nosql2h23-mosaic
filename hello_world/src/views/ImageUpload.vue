<template>
  <div class="d-flex flex-row align-items-center" style="height: 100%;">
    <div class="card d-flex" style="width: 100%">
      <div class="card-body">
        <button class="btn btn-primary btn-block mt-4" @click="openUploadDialog">
          Загрузить
          <input type="file" accept="image/jpeg, image/gif, image/png" ref="fileInput" @change="onFileChange" style="display: none"/>
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
  name: "uploadImage",
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
        this.createImage(files[0]);
        upload(files[0].name, this.image);
      }
    },
    createImage(file) {
      const reader = new FileReader();
      const vm = this;
      reader.onload = function (e) {
        vm.image = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    openUploadDialog() {
      if (this.fileSelected) {
      } else {

        this.$refs.fileInput.click();
      }
    },
  },
};
const picture = useField('picture')
const title = useField('title')
const upload = async(title, picture) => {
  let data = new FormData();
  let that = this;

  console.log(picture);
  console.log(title);

  data.append("picture", "picture");
  data.append("title", title);
  data.append("token", localStorage.getItem('token'));

  console.log(data);

  await axios
      .post(`http://localhost:5001/api/add_picture`, data)
      .then(async (res) => {
        await router.push({ path: "/home"});
      })


}
</script>

<style scoped>
.card-body {
  margin-left: -600px;
  margin-top: 600px;
  position: relative;
  z-index: 1;
}
.upload-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
}
</style>
