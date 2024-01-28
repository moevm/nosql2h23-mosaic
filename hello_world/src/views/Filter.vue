<template>
  <div>
    <input v-model="filterName" placeholder="Enter Name for Filter" />

    <button @click="applyFilter">Apply Filter</button>
  </div>
</template>

<script>
import {ref} from "vue";

export default {
  props: ["modelValue"],
  emits: ["update:modelValue"],
  setup(props, {emit}) {
    const filterName = ref(props.modelValue);

    const applyFilter = () => {
      emit("update:modelValue", filterName.value);
    };

    return {
      filterName,
      applyFilter,
    };
  },
};
</script>
