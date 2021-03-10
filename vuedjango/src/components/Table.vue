<template>
    <div class="container">
        <b-table striped hover :items="elements" :fields="fields"></b-table>
    </div>
</template>

<script>
export default {
    // para consumir la api de django automaticamente una vez creado el componente usamos created()
    created(){
        this.findAll();
    },
    data() {
        return {
            elements: [],
            fields:[
                {
                    key:'id',
                    sortable: true
                },
                {
                    key:'title',
                    sortable: false,
                    variant: 'info'
                },
                {
                    key:'url_clean',
                    label: 'Url limpia',
                    sortable: true,
                    variant:'danger'
                },
                {
                    key:'description',
                    sortable: true,
                    variant:'warning'
                },
                {
                    key:'category',
                    sortable: true
                },
                {
                    key:'type',
                    sortable: true
                }
            ]
        };
    },
    methods:{
         findAll: function(){
             fetch('http://127.0.0.1:8000/api/element/?format=json')
             .then(res => res.json())
             .then(res => (this.elements = res));
         }
    },
}
</script>

<style>
    .box{
        border: 5px solid #CCC;
        margin: 5px 0 0 0;
    }
</style>