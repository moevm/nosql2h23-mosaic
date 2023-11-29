<template>
  <div>
    <img :src="image" alt="Uploaded Image" />
  </div>
</template>

<script>
export default {
  name: "EditImage",
  data() {
    return {
      image: null,
    };
  },
  created() {
    // Получение параметра image из URL при загрузке страницы
    this.image = this.$route.query.image;
  },
};
</script>

<style scoped>

</style>
