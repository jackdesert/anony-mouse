var page = new Vue(
    {
        el: '#container',
        data: {composeVisible: false},
        methods: {
            compose: function(event) {
                this.composeVisible = true
            },
        }

    }
)

