var page = new Vue(
    {
        el: '#container',
        data: {composeVisible: false,
               message: ''},
        methods: {
            compose: function(event) {
                this.composeVisible = true
            },
            stopCompose: function(event) {
                this.composeVisible = false
            },
            sendMessage: function(event) {
                // See http://youmightnotneedjquery.com

                const request = new XMLHttpRequest()
                const data = {'message': this.message}

                request.open('POST', '/message/send', true)
                request.setRequestHeader('Content-Type', 'application/json')


                request.onload = function() {
                    if (request.status >= 200 && request.status < 400) {
                        // Success!
                        var resp = request.responseText;
                        console.log('SUCCESS')
                    } else {
                        // We reached our target server, but it returned an error
                        console.log('ERROR')

                    }
                }

                request.onerror = function() {
                    // There was a connection error of some sort
                        console.log('BIGERROR')
                }

                request.send(JSON.stringify(data))

            }
        }

    }
)


// Show things that were hidded during load
document.querySelectorAll('.hide-on-load').forEach(function(item, index, array){
    item.classList.remove('hide-on-load')
})
