<template>
  <el-menu
    id="sidebar-menu"
    default-active="1"
    :default-openeds="default_opens"
    active-text-color="#5ca4ca">
    <el-menu-item index="1">
      <i class="el-icon-date"></i>
      <span slot="title">
        <router-link to="/">概览</router-link>
      </span>
    </el-menu-item>
    <el-submenu index="2">
      <template slot="title">
        <i class="el-icon-menu"></i>
        <span>分类</span>
      </template>
      <el-menu-item v-for="category in categories" :key="category.id" :index="'2-' + category.id">
        <router-link :to="{name: 'category', params: {categoryId: category.id}}">{{ category.name }}</router-link>
        <!-- <router-link :to="'/category/' + item.id">{{ item.name }}</router-link> -->
      </el-menu-item>
    </el-submenu>
    <el-menu-item index="3">
      <i class="el-icon-setting"></i>
      <span slot="title">
        <router-link to="/management">管理</router-link>
      </span>
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  data() {
    return {
      default_opens: ["2"]
    }
  },
  computed: {
    categories() {
      return this.$store.state.categories;
    }
  }
}
</script>

<style scoped>
#sidebar-menu {
  border-right: 0 !important;
}
</style>


