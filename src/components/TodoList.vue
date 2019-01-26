<template>
  <div class="todo">
    <div class="actions">
      <el-button type="primary" @click.native="ShowAll">所有</el-button>
      <el-button type="primary" @click.native="ShowUnfinished">未完成</el-button>
      <el-button type="primary" @click.native="ShowFinished">已完成</el-button>
      <el-button type="danger" @click.native="DeleteFinished">删除已完成</el-button>
    </div>
    <div class="input-area">
      <el-input v-model="todoInput" @keyup.enter.native="AddTodo" placeholder="按回车添加 todo"/>
    </div>
    <div class="todo-items">
      <ul v-if="showUnfinished">
        <todo-item
          v-for="(item, index) in todoList.unfinished"
          :key="index"
          :content="item"
          :index="index"
          type="success"
          @changeStatus="ChangeToFinished"
        ></todo-item>
      </ul>
      <ul v-if="showFinished">
        <todo-item
          v-for="(item, index) in todoList.finished"
          :key="index"
          :content="item"
          :index="index"
          type="danger"
          @changeStatus="ChangeToUnfinished"
        ></todo-item>
      </ul>
    </div>
  </div>
</template>

<script>
import TodoItem from "./TodoItem.vue";
const STORAGE_KEY = "sponge-memos";

function save(item) {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(item));
}

function fetch() {
  return JSON.parse(window.localStorage.getItem(STORAGE_KEY));
}

export default {
  components: {
    "todo-item": TodoItem
  },
  data() {
    return {
      showFinished: true,
      showUnfinished: true,
      todoInput: "",
      todoList: {
        unfinished: [],
        finished: []
      }
    };
  },
  methods: {
    AddTodo: function() {
      if (this.todoInput != "") {
        this.todoList.unfinished.push(this.todoInput);
        this.todoInput = "";
      }
    },
    ChangeToFinished: function(index) {
      this.todoList.finished.push(this.todoList.unfinished.splice(index, 1)[0]);
    },
    ChangeToUnfinished: function(index) {
      this.todoList.unfinished.push(this.todoList.finished.splice(index, 1)[0]);
    },
    ShowAll: function() {
      this.showFinished = true;
      this.showUnfinished = true;
    },
    ShowFinished: function() {
      this.showFinished = true;
      this.showUnfinished = false;
    },
    ShowUnfinished: function() {
      this.showFinished = false;
      this.showUnfinished = true;
    },
    DeleteFinished: function() {
      this.todoList.finished = [];
    }
  },
  watch: {
    todoList: {
      handler: function(newList) {
        save(newList);
      },
      deep: true
    }
  },
  mounted() {
    const todoList = fetch();
    if (todoList) {
      this.todoList = todoList;
    }
  }
};
</script>

<style scoped>
.todo {
  height: calc(75% - 10px);
  padding: 5px;
}
.actions {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
}
.actions button {
  padding: 5px;
  width: 100%;
}
.actions,
.input-area {
  margin-bottom: 4px;
}
.todo-items {
  max-height: calc(100% - 80px);
  overflow-y: auto;
}
ul {
  list-style: none;
  padding: 0;
}
</style>