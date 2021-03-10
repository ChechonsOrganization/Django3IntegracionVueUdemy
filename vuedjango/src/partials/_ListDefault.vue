<template>
    <div class="mt-3 mt-md-0">
        <div v-for="e in elementsList" v-bind:key="e.id" class="mt-2">
            <router-link class="card-link" :to=" '/detail/' + e.id ">
                <b-card 
                    :header="e.title"
                    border-variant="danger"
                    header-bg-variant="danger"
                    header-text-variant="white"
                >

                <b-card-text>
                    {{ e.description }}
                </b-card-text>

                </b-card>
            </router-link>
        </div>
    </div>
</template>


<script>
export default {
    props: ['elementsList'],
    data() {
        return {
            elements: []
        };
    },
    methods:{}
}
</script>

<style>
    a.card-link,
    a.card-link:hover {
        color: #222;
        text-decoration: none;
    }

    a.card-link:hover .card-body {
        background: #F8F9FA;
    }
</style>