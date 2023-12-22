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
        this.createImage(files[0]);
        this.fileSelected = true;
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
        this.upload();
      } else {
        this.$refs.fileInput.click();
      }
    },
    upload() {
      let data = new FormData();
      let that = this;

      data.append("file", this.image);
      data.append("sizes", this.sizes);
      data.append("root", "uploads/test");

      // Здесь вы можете использовать axios для отправки данных на сервер и получения ответа
      // axios.post('/api/photo/upload-base64', data)
      //     .then(function(res) {
      //       let result_input = document.querySelector('input[name=' + that.result + ']');
      //       let data = res['data'];
      //       result_input.value = data['path'];
      that.$router.push({ path: "/edit", query: { image: that.image } });
      //     });
    },
  },
};
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
