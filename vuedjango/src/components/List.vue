<template>
    <div>
        <ListDefault :elements-list="elements" />
    </div>
</template>

<script>
import ListDefault from "../partials/_ListDefault";
export default {
    // para consumir la api de django automaticamente una vez creado el componente usamos created()
    components:{
        ListDefault
    },
    created(){
        this.findAll();
    },
    data() {
        return {
            elements: []
        };
    },
    methods:{
         findAll: function(){
             fetch("http://127.0.0.1:8000/api/element/?format=json")
             .then(res => res.json())
             .then(res => (this.elements = res));
         }
    }
};
</script>

<style>
    .box{
        border: 5px solid #CCC;
        margin: 5px 0 0 0;
    }
</style>