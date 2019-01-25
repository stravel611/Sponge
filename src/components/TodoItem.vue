<template>
  <div @click="ChangeStatus">
    <el-tag :type="type" v-if="type == 'success'">{{content}}</el-tag>
    <el-tag :type="type" v-else>
      <del>{{content}}</del>
    </el-tag>
  </div>
</template>

<script>
export default {
  props: ["content", "index", "type"],
  methods: {
    ChangeStatus: function() {
      this.$emit("changeStatus", this.index);
    }
  }
};
</script>

<style scoped>
.el-tag {
  width: 100%;
  margin-bottom: 2px;
  cursor: pointer;
}
</style>
