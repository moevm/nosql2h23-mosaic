<script setup>
import { defineComponent, reactive } from "vue";
import UploadImage from "@/views/ImageUpload.vue";
import image from "@/views/ImageEdit.vue";

</script>

<template>
  <div class="left-bar">
    <p class="profile-name"><img class="profile-pic" src="../../public/profile.jpg" alt="none">Jolyne Doe</p>
  </div>
  <div class="main_window">
    <p class="tutorial-title">Tutorial Mode</p>
    <img class="tutorial-image" :src="image" alt="Uploaded Image">
    <p class="part-title">Part</p>
    <div class="d-flex justify-space-around">
      <v-color-picker
          class="ma"
          :swatches="swatches"
          show-swatches
      ></v-color-picker>
    </div>
    <router-link tag="button" class="back_button" to="/home">Back</router-link>
  </div>
</template>

<style scoped>
.left-bar{
  height: 100vh;
  width: 250px;
  background: rgba(158, 152, 172);
  position: absolute;
  left: 0;
  top: 0;
}
.profile-pic{
  width: 50px;
  height: 50px;
  border-radius: 100%;
  border: solid 2px;
  margin-left: 5px;
  position: absolute;
  left: 0;
}
.profile-name{
  margin-left: 55px;
}
.main_window{
  width: 1500px;
  height: 100vh;
  margin-left: 120px;
  background-color: white;
}
.tutorial-title{
  margin-left: 100px;
  margin-top: 50px;
  width: 200px;
  font-size: xx-large;
  color: black;
  border-bottom: none;
}
.back_button{
  background-color: rgba(41, 52, 112, 0.93);
  //margin-top: 500px;
  margin-left: 40px;
  color: white;
  width: 100px;
  display: block;
  border-radius: 5px;
  text-align: center;
}
.tutorial-image{
  margin-left: 20px;
  color: black;
}
.part-title{
  margin-left: 500px;
  margin-top: 30px;
  width: 200px;
  font-size: xx-large;
  color: black;
  border-bottom: none;
}
</style>