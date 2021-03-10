<template>
  <div id="app">
    <Header/>
    <div class="container">
      <div class="row">
        <div class="col-md-4">
          <Categories/>
          <br/>
          <Types/>
        </div>
        <div class="col-md-8">
          <router-view></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// MOVIMOS LAS DEMAS RUTAS HACIA MAIN
import Header from './components/Header.vue';
import Categories from './components/Categories.vue';
import Types from './components/Types.vue';

export default {
  name: 'App',
  components: {
    Header,
    Categories,
    Types
  }
}
</script>
