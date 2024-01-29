<template>
  <div>
    <input class="test" v-model="filterName" placeholder="Enter Name for Filter" />
    <button class="test2" @click="applyFilter">Apply Filter</button>
  </div>
</template>

<script>
import {ref} from "vue";

export default {
  props: ["modelValue"],
  emits: ["update:modelValue", "applyFilter"],
  setup(props, {emit}) {
    const filterName = ref(props.modelValue);

    const applyFilter = () => {
      emit("update:modelValue", filterName.value);
      emit("applyFilter", {name: filterName.value});
    };

    return {
      filterName,
      applyFilter,
    };
  },
};
</script>

<style>
.test{
margin-left: -1000px;
position: absolute;
z-index:2000;
}
.test2{
  margin-left: -800px;
  position: absolute;
  z-index:2000;
}
</style>
