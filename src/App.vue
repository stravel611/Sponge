<template>
  <div id="app">
    <div id="nav">
      <el-menu
        class="el-menu-demo"
        mode="horizontal"
        background-color="#5ca4ca"
        text-color="#FFF"
        active-text-color="#fcf798"
      >
        <el-menu-item index="1">存在感</el-menu-item>
        <el-menu-item index="2">很强</el-menu-item>
        <el-menu-item index="3">但</el-menu-item>
        <el-menu-item index="4">并没有</el-menu-item>
        <el-menu-item index="5">什么</el-menu-item>
        <el-menu-item index="6">用处</el-menu-item>
        <el-menu-item index="7">的</el-menu-item>
        <el-menu-item index="8">顶部导航条</el-menu-item>
      </el-menu>
    </div>
    <div id="main-page">
      <div class="grid-content sidebar-l">
        <sponge-sidebar></sponge-sidebar>
      </div>
      <div class="grid-content page-content">
        <router-view></router-view>
      </div>
      <div class="grid-content sidebar-r">
        <sponge-status></sponge-status>
        <sponge-memo></sponge-memo>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from "./components/Sidebar";
import Status from "./components/Status";
import Memo from "./components/Memo";

export default {
  components: {
    "sponge-sidebar": Sidebar,
    "sponge-status": Status,
    "sponge-memo": Memo
  },
  data() {
    return {};
  },
  mounted() {
    this.$store.dispatch("fetchProceeding");
    this.$store.dispatch("fetchCategory");
  }
};
</script>


<style>
* {
  margin: 0;
  padding: 0;
}
a {
  text-decoration: none;
}
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
#main-page {
  display: flex;
  flex-direction: row;
}
.el-menu--horizontal {
  min-width: 1750px;
  z-index: 100;
  border-bottom: 0 !important;
  box-shadow: 0 1px 3px rgba(26, 26, 26, 0.1);
}
.sidebar-l {
  height: calc(100vh - 60px);
  width: calc(15vw - 1px);
  min-width: 199px;
  border-right: solid 1px #e6e6e6;
}
.sidebar-r {
  height: calc(100vh - 60px);
  width: calc(85vw - 1250px);
  min-width: 300px;
  border-left: solid 1px #e6e6e6;
}
.page-content {
  min-height: calc(100vh - 60px);
  height: calc(100vh - 60px);
  width: 1250px;
  min-width: 1250px;
}
</style>
