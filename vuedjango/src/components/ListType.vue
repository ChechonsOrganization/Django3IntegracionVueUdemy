<template>
    <div>
        <ListDefault :elements-list="elements" />
    </div>
</template>

<script>
import ListDefault from '../partials/_ListDefault';

export default {
    name: 'list-type',
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
             fetch("http://127.0.0.1:8000/api/type/" + this.$route.params.id + "/elements/?format=json")
             .then(res => res.json())
             .then(res => (this.elements = res));
         }
    },
    watch: {
        "$route.params.id": function(){
            this.findAll();
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